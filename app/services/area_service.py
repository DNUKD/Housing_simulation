# Recommended healthy living area based on hh size
def compute_healthy_area(roles):
    size = len(roles)

    if size == 1:
        return 30
    if size == 2:
        return 45
    if size == 3:
        return 60
    if size == 4:
        return 75
    if size == 5:
        return 90

    # For larger families linear expansion
    return 20 * size


# Minimum acceptable living area based on member comp.
def compute_min_area(roles):
    adults = sum(1 for r in roles if r in ["adult_worker", "adult_unemployed", "retired"])
    kids = sum(1 for r in roles if r == "child")

    if adults == 1:
        base = 25
    elif adults == 2:
        base = 30
    elif adults == 3:
        base = 40
    else:
        base = 50

    # Children add additional area requirements
    extra = kids * 10
    return base + extra


# Crowding stat
def determine_crowding_status(usable_area, healthy_area):
    if usable_area < healthy_area * 0.8:
        return "overcrowded"
    elif usable_area < healthy_area:
        return "tight"
    else:
        return "ok"
