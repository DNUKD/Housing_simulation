from app.services.rental_service import compute_real_rent

def test_compute_real_rent_small_flat():
    # area < 30 → +5% surcharge
    result = compute_real_rent(25, 2000)
    assert result == 25 * 2000 * 1.05

def test_compute_real_rent_mid_flat():
    # 30 <= area < 50 → +3%
    result = compute_real_rent(40, 2000)
    assert result == 40 * 2000 * 1.03
