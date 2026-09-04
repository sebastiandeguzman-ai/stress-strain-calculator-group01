def run_new_test(materials_db: dict, test_history: list):
    """Executes a single mechanical test run and appends results."""
    print("\nAvailable Materials:")
    for key, mat in materials_db.items():
        print(f"- {key.capitalize()} ({mat.properties.yield_strength} MPa Yield)")
    print("- Custom Material")

    mat_choice = input("Select Material: ").strip().lower()

    if mat_choice in materials_db:
        selected_mat = materials_db[mat_choice]
    elif mat_choice in ["custom", "custom material"]:
        name = input("Enter material name: ").strip()
        density = get_positive_float("Enter density (kg/m³): ")
        yield_strength = get_positive_float("Enter yield strength (MPa): ")
        youngs_modulus = get_positive_float("Enter Young's modulus (GPa): ")
        selected_mat = Material(name, MaterialProperties(density, yield_strength, youngs_modulus))
    else:
        print("Invalid material choice. Returning to main menu.")
        return

    force = get_positive_float("Enter applied force (N): ")
    area = get_positive_float("Enter cross-sectional area (m²): ")
    orig_len = get_positive_float("Enter original length (m): ")
    change_len = get_positive_float("Enter change in length (m): ")

    try:
        test = StressStrainTest(selected_mat, force, area, orig_len, change_len)
        test_history.append(test)
        print("\n" + "-" * 35)
        print("TEST RESULT RECORDED")
        print(test)
        print(f"Factor of Safety: {test.factor_of_safety:.2f}")
        print("-" * 35)
    except Exception as e:
        print(f"Error running test: {e}")


