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

def display_menu():
    """Displays the main application user interface menu."""
    print("\n" + "=" * 45)
    print(" STRESS & STRAIN ANALYSIS SYSTEM")
    print("=" * 45)
    print("1. Run New Mechanical Test")
    print("2. Generate Simulated Test Data")
    print("3. View Session Calculation History")
    print("4. Save Results (JSON)")
    print("5. Load Saved Results (JSON)")
    print("6. Export Test Data (CSV)")
    print("7. Exit")
    print("-" * 45)


def get_positive_float(prompt: str) -> float:
    """Validates user numerical inputs to prevent non-numeric or zero/negative entry errors."""
    while True:
        try:
            val = float(input(prompt).replace(",", ""))
            if val <= 0:
                print("Error: Input must be strictly greater than 0.")
                continue
            return val
        except ValueError:
            print("Error: Please enter a valid numerical value.")

def handle_history_and_export(choice: str, test_history: list):
    """Processes session history listing and CSV data export options."""
    if choice == "3":
        if not test_history:
            print("\nNo test results recorded yet.")
        else:
            print(f"\n=== CALCULATION HISTORY ({len(test_history)} tests) ===")
            for idx, t in enumerate(test_history, start=1):
                print(f"{idx}. {t}")

    elif choice == "6":
        export_results_csv(test_history)
        print("\nData successfully exported to data/results.csv")


