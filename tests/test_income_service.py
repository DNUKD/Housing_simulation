from app.services.income_service import compute_randomized_income_and_cost
from types import SimpleNamespace

def test_compute_randomized_income_and_cost():
    wage_row = SimpleNamespace(median_income=300000)
    income, cost = compute_randomized_income_and_cost("adult_worker", "HU", wage_row)

    assert income > 0
    assert cost > 0
    assert isinstance(income, float)
    assert isinstance(cost, float)
