# Regional price adjust
def calculate_market_adjustment(region_type: str) -> float:
    if region_type == "capital":
        return 0.25
    if region_type == "city":
        return 0.10
    return 0.00


# Final rent with extra sqm surcharge
def compute_real_rent(area: float, price_per_sqm: float) -> float:
    base_rent = area * price_per_sqm

    if area < 30:
        return base_rent * 1.05
    elif area < 50:
        return base_rent * 1.03
    else:
        return base_rent
