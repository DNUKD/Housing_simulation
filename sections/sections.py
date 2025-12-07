import streamlit as st
from view.ui_blocks import ui_title, ui_metric
import plotly.graph_objects as go

# Helper func for anim
def anim_value(animated, key, raw):
    val = animated.get(key, raw)
    if val == 0:
        return raw
    return val

# --------- Cols and diagram

# A) Housing Affordability
def render_housing_affordability(col, data, animated, currency):
    with col:
        raw_income = float(data["total_income"])
        raw_budget = float(data["housing_budget"])

        income = anim_value(animated, "income", raw_income)
        budget = int(anim_value(animated, "housing_budget", raw_budget))

        percent = round((budget / income * 100), 1) if income else 0

        ui_title("Housing Affordability")

        ui_metric(label="Usage rate", value=f"{percent}%", tooltip="Income safely spendable on housing.")
        ui_metric(label="Housing budget", value=f"{budget:,} {currency}")


# B) Income
def render_income(col, data, animated, currency):
    with col:
        raw_total = float(data["total_income"])
        raw_min = float(data["min_survival_required"])

        total = int(anim_value(animated, "income", raw_total))
        minimum = int(anim_value(animated, "min_survival", raw_min))

        ui_title("Income")

        ui_metric("Household Income", f"{total:,} {currency}")
        ui_metric("Minimum living standard", f"{minimum:,} {currency}")


# C) Rent
def render_rent(col, data, animated, currency):
    with col:
        raw_rent = float(data["real_rent"])
        raw_budget = float(data["housing_budget"])

        rent = int(anim_value(animated, "rent", raw_rent))
        budget = int(anim_value(animated, "housing_budget", raw_budget))

        remaining = float(data.get("remaining_after_survival_and_rent", 0))

        # Status messeage if
        if remaining < 0:
            color = "#ff4d4f"
            msg = "Housing is not affordable."
        elif rent > budget:
            color = "#ff9800"
            msg = "The rent exceeds the budget."
        else:
            color = "#ffffff"
            msg = ""

        ui_title("Rent")
        ui_metric(
            "Monthly rent (market price)",
            f"{rent:,} {currency}",
            tooltip="Market-adjusted apartment pricing",
            color=color,
            warning=msg,
            warning_color=color
        )


# D) Floor Area
def render_floor_area(col, data, animated, currency):
    with col:
        raw_aff = float(data["affordable_area"])
        raw_healthy = float(data["healthy_area"])

        aff = anim_value(animated, "aff_area", raw_aff)
        healthy = anim_value(animated, "healthy_area", raw_healthy)
        crowd = aff / healthy if healthy > 0 else 0

        ui_title("Floor Area")

        ui_metric("Apartment floor area", f"{aff:.2f} m²")
        ui_metric(
            "Crowding index",
            f"{crowd:.2f}",
            tooltip="Usable_area / healthy_area\n"
                    "Below 0.8 → Overcrowded\n"
                    "0.8–1.0 → Tight\n"
                    "1.0+ → Normal"
        )


# Houshold Chart
def render_household_chart(col, data, currency):
    with col:

        YAXIS_DTICK = {
            "Ft": 50000,
            "€": 250,
            "NOK": 5000,
        }

        MAX_MEMBERS = 6

        # Clone the list cause of empty role
        members = data["members"].copy()

        # Set dummy members
        while len(members) < MAX_MEMBERS:
            members.append({"role": "empty", "income": 0, "cost": 0})

        role_map = {
            "adult_worker": "Adult",
            "adult_unemployed": "Adult",
            "retired": "Senior",
            "child": "Child",
        }

        # Potly needs index
        x_keys = [
            role_map.get(m["role"], "Empty") + f"#{i + 1}"
            for i, m in enumerate(members)
        ]

        # Lables
        tick_labels = [
            role_map.get(m["role"], "")
            for m in members
        ]

        # List comprehension
        costs = [m["cost"] for m in members]

        # Data from FAST API
        total_income = data["total_income"]
        total_rent = data["real_rent"]

        # If null then
        if total_rent <= 0 or total_income <= 0:
            housing = [0 for _ in members]
        else:
            # Income-based split
            raw_housing = [
                (m["income"] / total_income) * total_rent
                for m in members
            ]

            CURRENCY_ROUND = {
                "Ft": 1000,
                "€": 50,
                "NOK": 500,
            }
            round_step = CURRENCY_ROUND.get(currency, 1000)

            # Share rounding
            rounded_housing = [round(x / round_step) * round_step for x in raw_housing]

            # Remaining handling
            difference = total_rent - sum(rounded_housing)

            # Giving it to one pers
            for i in reversed(range(len(members))):
                if members[i]["income"] > 0:
                    rounded_housing[i] += difference
                    break
            else:
                rounded_housing[-1] += difference

            # Final housing list
            housing = rounded_housing

        # Leftover (spendable)
        remaining = [
            max(m["income"] - costs[i] - housing[i], 0)
            for i, m in enumerate(members)
        ]

        fig_height = 420
        fig = go.Figure()

        fig.add_trace(go.Bar(name="Expense",x=x_keys,y=costs,
            hovertemplate="Expense: %{y:,.0f} " + currency + "<extra></extra>",
        marker_color="rgb(176,176,176)"
        ))

        fig.add_trace(go.Bar(name="Housing",x=x_keys,y=housing,
            hovertemplate="Housing: %{y:,.0f} " + currency + "<extra></extra>",
        marker_color="rgb(255,142,69)"
        ))

        fig.add_trace(go.Bar(name="Remaining Income",x=x_keys,y=remaining,
            hovertemplate="Remaining: %{y:,.0f} " + currency + "<extra></extra>",
        marker_color="rgb(46,204,113)"
        ))

        fig.update_traces(width=0.45)

        fig.update_layout(
            barmode="stack",
            plot_bgcolor="#0e1117",
            paper_bgcolor="#0e1117",
            font=dict(color="white"),
            height=fig_height,
            margin=dict(l=30, r=30, t=30, b=30),
            xaxis=dict(title="Family Members",tickangle=0,tickmode='array',tickvals=x_keys,ticktext=tick_labels,),
            yaxis=dict(title=f"Monthly Expenses ({currency})",dtick=YAXIS_DTICK.get(currency, 50000),gridcolor="rgba(255,255,255,0.15)"),
        legend=dict(bgcolor="#0e1117",bordercolor="#333",borderwidth=1,x=1.0,y=1.0,)
        )

        st.plotly_chart(fig, use_container_width=True)


# E) Market Price
def render_market_price(col, region_lookup, data, currency):
    with col:
        raw_base_price = float(region_lookup[0]["rent_persqm"])
        raw_adjustment = float(data.get("market_adjustment", 0.0))

        adjusted_price = raw_base_price * (1 + raw_adjustment)
        percentage = int(raw_adjustment * 100)

        base_price = int(raw_base_price)

        ui_title("Market Price")

        ui_metric("Average price per m²", f"{base_price:,} {currency}/m²")

        value_html = (
            f"{int(adjusted_price):,} {currency} "
            f"<span class='price-delta'>▲ {percentage}%</span>"
        )

        ui_metric("Adjusted price per m²", value_html, tooltip="Region-based price surcharge per m²")




