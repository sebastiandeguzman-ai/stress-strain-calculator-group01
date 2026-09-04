def main():
	materials = {
    "steel": {
        "Yield Strength": 250,
        "Young's Modulus": 200
    },
    "aluminum": {
        "Yield Strength": 95,
        "Young's Modulus": 69
    },
    "titanium": {
        "Yield Strength": 880,
        "Young's Modulus": 116
    }
}
	while True:
        try:
            material = select_material(materials)
            
            input_handling(force, area, original_len, change_len)
            break

        except ValueError as e:
            print(f"Invalid input: {e}")
            print("Please enter a valid number.")

    perform_safety_analysis(stress_mpa, material)

    again = input("Run again? (y/n): ")
    if again.lower() == "y":
        main()
    else:
        print("Goodbye!")

def select_material(materials):
    """Handles material selection from predefined options or custom input."""

    # TODO: Create a loop so the user can select a valid material
    while True:

        # TODO: Display the available materials
        print("\nAvailable Materials:")

        # TODO: Display each material from the materials dictionary
        for mat_name in materials.keys():
            print(f"- {mat_name.capitalize()}")

        # TODO: Add an option for a custom material
        print("- Custom Material")

        # TODO: Get the user's material choice
        material_choice = input(
            "Enter your material choice: "
        ).lower().strip()

        # TODO: Check if the user's choice is one of the built-in materials
        if material_choice in materials:

            # TODO: Display the selected material
            print(f"Selected material: {material_choice.capitalize()}")

            # TODO: Return the properties of the selected material
            return materials[material_choice]

        # TODO: Handle custom material selection
        elif material_choice == "custom":

            # TODO: Use try-except to handle non-numeric values
            try:

                # TODO: Ask for the custom material's yield strength
                custom_yield_strength = float(
                    input("Enter the Custom Yield Strength (MPa): ")
                )

                # TODO: Ask for the custom material's Young's modulus
                custom_young_modulus = float(
                    input("Enter the Custom Young's Modulus (GPa): ")
                )

                # TODO: Validate that the custom properties are positive
                if custom_yield_strength <= 0:
                    raise ValueError(
                        "Yield strength must be greater than 0."
                    )

                if custom_young_modulus <= 0:
                    raise ValueError(
                        "Young's modulus must be greater than 0."
                    )

                # TODO: Display confirmation of the selected custom material
                print("Selected custom material properties.")

                # TODO: Return the custom material properties
                return {
                    "Yield Strength": custom_yield_strength,
                    "Young's Modulus": custom_young_modulus
                }

            # TODO: Handle invalid numeric input
            except ValueError as e:
                print(f"Invalid input: {e}")

        # TODO: Handle invalid material choices
        else:
            print(
                "Invalid material choice. "
                "Please select from the list or 'Custom Material'."
            )
def input_handling(force, area, original_len, change_len):
    """Validates the user input values."""

    # TODO: Check if the force is a valid value
    # Force can be positive or negative depending on loading direction

    # TODO: Check if the cross-sectional area is greater than zero
    if area <= 0:
        raise ValueError(
            "Cross-sectional area must be greater than 0."
        )

    # TODO: Check if the original length is greater than zero
    if original_len <= 0:
        raise ValueError(
            "Original length must be greater than 0."
        )

    # TODO: Check if change in length is valid
    # Negative change in length is allowed because it represents compression

def perform_safety_analysis(stress_mpa, selected_material_properties):
    """Performs safety analysis based on stress and material yield strength."""

    # TODO: Compare the calculated stress with the material's yield strength
    # TODO: Calculate the factor of safety
    # TODO: Determine whether the material is safe or likely to fail

    safety_margin_factor = 0.9

    if stress_mpa > 0:

        # TODO: Calculate factor of safety
        factor_of_safety = (
            selected_material_properties["Yield Strength"] / stress_mpa
        )

        # TODO: Determine if the stress is safely below the yield strength
        if stress_mpa < selected_material_properties["Yield Strength"] * safety_margin_factor:
            print(
                f"SAFE - Factor of Safety: {factor_of_safety:.2f}"
            )

        # TODO: Handle stress that is close to the yield strength
        elif stress_mpa < selected_material_properties["Yield Strength"]:
            print(
                f"CAUTION - Factor of Safety: {factor_of_safety:.2f}"
            )

        # TODO: Warn the user if stress exceeds the yield strength
        else:
            print(
                f"UNSAFE - Factor of Safety: {factor_of_safety:.2f}"
            )

    # TODO: Handle zero or compressive stress
    else:
        print("SAFE - No tensile stress, or negligible stress.")

class Utils:
  def __init__(self):
    self.force = float(input("Enter applied force(in Newtons): ").replace(",", ""))
    self.area = float(input("Enter cross-sectional area(in square meters): ").replace(",", ""))
    self.original_len = float(input("Enter length(in m): ").replace(",", ""))
    self.change_len = float(input("Enter change in length(in m): ").replace(",", ""))

  def calculate_stress_strain(self):
    stress = self.force / self.area
    strain = self.change_len / self.original_len

    print("=== RESULTS ===")
    # TODO: Print each input value with appropriate formatting
    print(f"Applied Force: {self.force:.2f} N")
    print(f"Cross-Sectional Area: {self.area:.2f} m^2")
    print(f"Original Length: {self.original_len:.2f} m")
    print(f"Change in Length: {self.change_len:.2f} m")

    # TODO: Display the calculated results
    print("Stress & Strain results")
    # TODO: Print stress with 2 decimal places and units (Pa)
    print(f"Stress: {stress:.2f} Pa")
    # TODO: Print strain with 6 decimal places
    print(f"Strain: {strain:.6f}")
    stress = force / area
    strain = change_len / original_len

    print("=== RESULTS ===")
    # TODO: Print each input value with appropriate formatting
    print(f"Applied Force: {force:.2f} N")
    print(f"Cross-Sectional Area: {area:.2f} m^2")
    print(f"Original Length: {original_len:.2f} m")
    print(f"Change in Length: {change_len:.2f} m")

    # TODO: Display the calculated results
    print("Stress & Strain results")
    # TODO: Print stress with 2 decimal places and units (Pa)
    print(f"Stress: {stress:.2f} Pa")
    # TODO: Print strain with 6 decimal places
    print(f"Strain: {strain:.6f}")

  def conversion (stress):
    stress_mpa = stress / 1_000_000
    print(f"Stress in MPa: {stress_mpa:.2f} MPa")
