from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.country import Country
from app.models.region import Region
from app.models.simulation import Simulation
from app.models.wage_stats import WageStats
from app.services.area_service import (compute_healthy_area,compute_min_area,determine_crowding_status,)
from app.services.rental_service import (calculate_market_adjustment,compute_real_rent,)
from app.services.income_service import (compute_randomized_income_and_cost,)
from app.services.animation_service import set_target


CURRENCY_MAP = {
    "HU": "Ft",
    "DE": "€",
    "FR": "€",
    "NL": "€",
    "NO": "NOK",
}

# CONST Housing budget
HOUSING_RATIO_MAP = {
    1: 0.30,
    2: 0.30,
    3: 0.35,
    4: 0.40,
    5: 0.45,
}


# Main simulation logic
def run_simulation_logic(country_id: int, region_id: int, family_roles: list, db: Session):
    """
    Runs the full simulation using all service components.
    Performs validation, income/cost calculation, rent evaluation,
    crowding analysis, DB storage, and anim value updates
    """

    # ---------- Input validation ----------
    active_adults = sum(1 for r in family_roles if r in ["adult_worker", "retired"])
    if active_adults == 0:
        raise HTTPException(
            status_code=400,
            detail="Legalább 1 keresőképes felnőttnek lennie kell a családban."
        )

    family_size = len(family_roles)
    housing_ratio = HOUSING_RATIO_MAP.get(family_size, 0.50)

    # ---------- Database lookups ----------
    region = db.query(Region).filter_by(id=region_id).first()
    if not region:
        raise HTTPException(404, "Region not found")

    country = db.query(Country).filter_by(id=country_id).first()
    if not country:
        raise HTTPException(404, "Country not found")

    currency = CURRENCY_MAP.get(country.code, "Ft")

    rent_native = region.rent_persqm
    market_adjustment = calculate_market_adjustment(region.type)
    adjusted_rent_native = rent_native * (1 + market_adjustment)

    total_income = 0.0
    total_cost = 0.0
    members = []

    # ---------- Income & survival cost per member ----------
    for role in family_roles:
        wage_row = db.query(WageStats).filter_by(
            role=role,
            country_id=country_id,
            region_id=region_id
        ).first()

        if not wage_row:
            raise HTTPException(500, f"Missing wage stat for role {role}")

        income, cost = compute_randomized_income_and_cost(role, country.code, wage_row)

        total_income += income
        total_cost += cost

        members.append({
            "role": role,
            "income": income,
            "cost": cost,
            "housing": income * housing_ratio
        })

    remaining_after_survival = total_income - total_cost

    # ---------- Crisis scenario  ----------
    if remaining_after_survival <= 0:
        min_area = compute_min_area(family_roles)
        crisis_rent = compute_real_rent(min_area, adjusted_rent_native)

        return {
            "status": "housing_crisis",
            "total_income": total_income,
            "housing_budget": 0,
            "affordable_area": 0,
            "healthy_area": compute_healthy_area(family_roles),
            "crowding_status": "crisis",

            "min_survival_required": total_cost,
            "remaining_income_after_survival": remaining_after_survival,
            "remaining_after_survival_and_rent": remaining_after_survival,

            "recommended_area": min_area,
            "real_rent": round(crisis_rent, -2),

            "rent_per_sqm": rent_native,
            "market_adjustment": market_adjustment,
            "currency": currency,
            "members": members,
        }

    # ---------- Normal scenario ----------
    housing_budget = total_income * housing_ratio
    affordable_area = housing_budget / adjusted_rent_native if adjusted_rent_native > 0 else 0

    min_area = compute_min_area(family_roles)
    usable_area = max(affordable_area, min_area)
    healthy_area = compute_healthy_area(family_roles)

    crowding_status = determine_crowding_status(usable_area, healthy_area)
    real_rent = compute_real_rent(usable_area, adjusted_rent_native)

    # ---------- Save simulation result ----------
    sim = Simulation(
        country_id=country_id,
        region_id=region_id,
        total_income=total_income,
        affordable_area=usable_area,
        healthy_area=healthy_area,
        crowding_status=crowding_status,
    )

    db.add(sim)
    db.commit()
    db.refresh(sim)

    remaining_after_survival_and_rent = total_income - total_cost - real_rent

    # ---------- Crowding state sync ----------
    crowding_index = usable_area / healthy_area if healthy_area > 0 else 0

    # ---------- Animation targets ----------
    set_target("income", total_income)
    set_target("min_survival", total_cost)
    set_target("rent", round(real_rent, -2))
    set_target("aff_area", affordable_area)
    set_target("healthy_area", healthy_area)
    set_target("housing_budget", housing_budget)
    set_target("base_price", rent_native)
    set_target("adjusted_price", adjusted_rent_native)
    set_target("crowding_index", crowding_index)

    # ---------- Final response ----------
    return {
        "simulation_id": sim.id,
        "country_id": sim.country_id,
        "region_id": sim.region_id,
        "family_roles": family_roles,

        "total_income": total_income,
        "housing_budget": housing_budget,
        "affordable_area": usable_area,
        "healthy_area": healthy_area,
        "crowding_status": crowding_status,

        "min_survival_required": total_cost,
        "remaining_income_after_survival": remaining_after_survival,
        "remaining_after_survival_and_rent": remaining_after_survival_and_rent,

        "rent_per_sqm": rent_native,
        "adjusted_rent_per_sqm": adjusted_rent_native,
        "market_adjustment": market_adjustment,
        "real_rent": round(real_rent, -2),
        "currency": currency,
        "members": members,
    }
