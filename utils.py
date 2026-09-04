# Part 1: Basic Stress and Strain Calculator Template


def calculate_stress_and_strain(force, area, original_len, change_len):
    """Calculates stress, strain, and stress in MPa from inputs."""
    stress = force / area  # Stress in Pascals (Pa)
    strain = change_len / original_len  # Dimensionless strain
    stress_mpa = stress / 1_000_000  # Conversion to Megapascals (MPa)

    return stress, strain, stress_mpa


def select_material(materials):
    """Handles material selection from predefined options or custom input."""

    while True:
        print("\nAvailable Materials:")

        for mat_name in materials.keys():
            print(f"- {mat_name.capitalize()}")

        print("- Custom Material")

        material_choice = input(
            "Enter your material choice: "
        ).lower().strip()

        if material_choice in materials:
            print(f"Selected material: {material_choice.capitalize()}")
            return materials[material_choice]

        elif material_choice == "custom":
            try:
                custom_yield_strength = float(
                    input("Enter the Custom Yield Strength (MPa): ")
                )
                custom_young_modulus = float(
                    input("Enter the Custom Young's Modulus (GPa): ")
                )

                if custom_yield_strength <= 0:
                    raise ValueError(
                        "Yield strength must be greater than 0."
                    )

                if custom_young_modulus <= 0:
                    raise ValueError(
                        "Young's modulus must be greater than 0."
                    )

                print("Selected custom material properties.")

                return {
                    "Yield Strength": custom_yield_strength,
                    "Young's Modulus": custom_young_modulus,
                }

            except ValueError as e:
                print(f"Invalid input: {e}")

        else:
            print(
                "Invalid material choice. "
                "Please select from the list or 'Custom Material'."
            )


def input_handling(force, area, original_len, change_len):
    """Validates the user input values."""

    if area <= 0:
        raise ValueError(
            "Cross-sectional area must be greater than 0."
        )

    if original_len <= 0:
        raise ValueError(
            "Original length must be greater than 0."
        )


def perform_safety_analysis(stress_mpa, selected_material_properties):
    """Performs safety analysis based on stress and material yield strength."""

    safety_margin_factor = 0.9

    if stress_mpa > 0:
        factor_of_safety = (
            selected_material_properties["Yield Strength"] / stress_mpa
        )

        if stress_mpa < selected_material_properties["Yield Strength"] * safety_margin_factor:
            print(
                f"SAFE - Factor of Safety: {factor_of_safety:.2f}"
            )
        elif stress_mpa < selected_material_properties["Yield Strength"]:
            print(
                f"CAUTION - Factor of Safety: {factor_of_safety:.2f}"
            )
        else:
            print(
                f"CAUTION - Yield strength exceeded. Factor of Safety: {factor_of_safety:.2f}"
            )
    else:
        print("SAFE - No tensile stress, or negligible stress.")


def main():
    """Main function for the stress and strain calculator."""

    print("=== Stress and Strain Calculator ===")
    print()

    materials = {
        "steel": {
            "Yield Strength": 250,
            "Young's Modulus": 200,
        },
        "aluminum": {
            "Yield Strength": 95,
            "Young's Modulus": 69,
        },
        "titanium": {
            "Yield Strength": 880,
            "Young's Modulus": 116,
        },
    }

    while True:
        try:
            material = select_material(materials)
            force = float(input("Enter applied force(in Newtons): ").replace(",", ""))
            area = float(input("Enter cross-sectional area(in square meters): ").replace(",", ""))
            original_len = float(input("Enter length(in m): ").replace(",", ""))
            change_len = float(input("Enter change in length(in m): ").replace(",", ""))

            input_handling(force, area, original_len, change_len)
            break

        except ValueError as e:
            print(f"Invalid input: {e}")
            print("Please enter valid numeric values.\n")

    # Call the dedicated calculation and conversion function
    stress, strain, stress_mpa = calculate_stress_and_strain(
        force, area, original_len, change_len
    )

    print()
    print("=== RESULTS ===")
    print(f"Applied Force: {force:.2f} N")
    print(f"Cross-Sectional Area: {area:.2f} m^2")
    print(f"Original Length: {original_len:.2f} m")
    print(f"Change in Length: {change_len:.2f} m")

    print()
    print("Stress & Strain results")
    print(f"Stress: {stress:.2f} Pa")
    print(f"Strain: {strain:.6f}")
    print(f"Stress in MPa: {stress_mpa:.2f} MPa")
    print()

    if change_len > 0:
        print("Loading Type: Tension")
    elif change_len < 0:
        print("Loading Type: Compression")
    else:
        print("Loading Type: Neither (No change in length)")

    perform_safety_analysis(stress_mpa, material)

    print()
    again = input("Run again? (y/n): ")
    if again.lower().strip() == "y":
        main()
    else:
        print("Goodbye!")
        print()
        print("=== Analysis Complete ===")


if __name__ == "__main__":
    main()
