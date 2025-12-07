import pytest
from app.services.area_service import compute_healthy_area

@pytest.mark.parametrize("roles, expected", [
    (["adult_worker"], 30),
    (["adult_worker", "child"], 45),
    (["adult_worker", "adult_worker", "child"], 60),
    (["child", "child", "child", "adult_worker"], 75),
])
def test_compute_healthy_area(roles, expected):
    assert compute_healthy_area(roles) == expected
