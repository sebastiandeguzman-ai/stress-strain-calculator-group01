def calculate_stress(force: float, area: float) -> float:
    return force / area


def calculate_strain(change_in_length: float, original_length: float) -> float:
    return change_in_length / original_length


def calculate_youngs_modulus(stress: float, strain: float) -> float:
    if strain == 0:
        return 0.0
    return stress / strain


def calculate_factor_of_safety(yield_strength: float, working_stress: float) -> float:
    return yield_strength / working_stress