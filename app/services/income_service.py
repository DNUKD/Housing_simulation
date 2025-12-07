import random

# Differency set
INCOME_VARIATION = 0.50
COST_VARIATION = 0.50

# Survival cost
SURVIVAL_COST = {
    "HU": {"adult": 120_000, "child": 60_000},
    "DE": {"adult": 600, "child": 300},
    "FR": {"adult": 650, "child": 320},
    "NL": {"adult": 680, "child": 340},
    "NO": {"adult": 9000, "child": 4500},
}

# Scaling for random
def random_scale(base: float, variation: float) -> float:
    low = 1 - variation
    high = 1 + variation
    return base * random.uniform(low, high)

# Income and cost for one person
def compute_randomized_income_and_cost(role: str, country_code: str, wage_row):
    base_income = wage_row.median_income

    if role == "child":
        base_cost = SURVIVAL_COST[country_code]["child"]
    else:
        base_cost = SURVIVAL_COST[country_code]["adult"]

    income = random_scale(base_income, INCOME_VARIATION)
    cost = random_scale(base_cost, COST_VARIATION)

    return income, cost
