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

def display_material_menu(materials: list[dict]) -> None:
    print("\n" + "=" * 40)
    print(" AVAILABLE MATERIAL LIBRARY ")
    print("=" * 40)
    for idx, mat in enumerate(materials, 1):
        ys_mpa = mat["yield_strength"] / 1e6
        print(f"{idx}. {mat['name']} (Yield Strength: {ys_mpa:.1f} MPa)")


def prompt_material_selection(materials: list[dict]) -> dict:
    display_material_menu(materials)
    while True:
        try:
            choice = int(input("\nSelect a material number: "))
            if 1 <= choice <= len(materials):
                return materials[choice - 1]
            print("Selection out of range. Try again.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def validate_positive_number(prompt_text: str, param_name: str) -> float:
    while True:
        try:
            val = float(input(prompt_text))
            if val <= 0:
                print(f"Error: {param_name} must be greater than zero.")
                continue
            return val
        except ValueError:
            print("Error: Invalid numeric input. Please try again.")