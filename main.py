import csv
import json
import sys
from dataclasses import asdict, dataclass

# Define minimal internal structure inside main.py to prevent top-level module code execution
@dataclass
class MaterialProperties:
    density: float
    yield_strength: float
    typical_youngs_modulus: float

class Material:
    def __init__(self, name: str, properties: MaterialProperties):
        self.name = name
        self.properties = properties

class StressStrainTest:
    def __init__(self, material: Material, force: float, area: float, original_length: float, change_in_length: float):
        self.material = material
        self.force = force
        self.area = area
        self.original_length = original_length
        self.change_in_length = change_in_length

    @property
    def stress(self) -> float:
        return self.force / self.area

    @property
    def strain(self) -> float:
        return self.change_in_length / self.original_length

    def will_fail(self) -> bool:
        return self.stress >= self.material.properties.yield_strength

    def to_dict(dict_self) -> dict:
        """Serialize test object for JSON conversion."""
        return {
            "material": {
                "name": dict_self.material.name,
                "properties": asdict(dict_self.material.properties)
            },
            "force": dict_self.force,
            "area": dict_self.area,
            "original_length": dict_self.original_length,
            "change_in_length": dict_self.change_in_length
        }

    @classmethod
    def from_dict(cls, data: dict) -> "StressStrainTest":
        """Reconstruct a StressStrainTest instance from dictionary data."""
        mat_props = MaterialProperties(**data["material"]["properties"])
        material = Material(data["material"]["name"], mat_props)
        return cls(
            material=material,
            force=data["force"],
            area=data["area"],
            original_length=data["original_length"],
            change_in_length=data["change_in_length"]
        )

def get_predefined_materials():
    return {
        "steel": Material("Steel", MaterialProperties(7850, 250000000, 200000000000)),
        "aluminum": Material("Aluminum", MaterialProperties(2700, 95000000, 69000000000)),
        "titanium": Material("Titanium", MaterialProperties(4500, 880000000, 114000000000)),
        "nylon": Material("Nylon", MaterialProperties(1150, 70000000, 2800000000)),
        "composite": Material("Composite", MaterialProperties(1600, 600000000, 70000000000)),
    }

def get_positive_float(prompt: str) -> float:
    while True:
        try:
            val = float(input(prompt).replace(",", "").strip())
            if val <= 0:
                print("Error: Input must be strictly greater than 0.")
                continue
            return val
        except ValueError:
            print("Error: Invalid numeric input. Please enter a valid number.")

def display_menu():
    print("\n" + "=" * 45)
    print(" STRESS & STRAIN ANALYSIS SYSTEM")
    print("=" * 45)
    print("1. Run New Mechanical Test")
    print("2. View Session Calculation History")
    print("3. Save Results (JSON)")
    print("4. Load Saved Results (JSON)")
    print("5. Export Test Data (CSV)")
    print("6. Exit")
    print("-" * 45)

def run_new_test(materials_db: dict, test_history: list):
    print("\nAvailable Materials:")
    for key in materials_db:
        print(f"- {key.capitalize()}")
    print("- Custom Material")

    mat_choice = input("Select Material: ").strip().lower()

    if mat_choice in materials_db:
        selected_mat = materials_db[mat_choice]
    elif mat_choice in ["custom", "custom material"]:
        name = input("Enter material name: ").strip()
        density = get_positive_float("Enter density (kg/m³): ")
        yield_strength = get_positive_float("Enter yield strength (Pa): ")
        youngs_modulus = get_positive_float("Enter Young's modulus (Pa): ")
        selected_mat = Material(name, MaterialProperties(density, yield_strength, youngs_modulus))
    else:
        print("Invalid material choice. Returning to main menu.")
        return

    force = get_positive_float("Enter applied force (N): ")
    area = get_positive_float("Enter cross-sectional area (m²): ")
    orig_len = get_positive_float("Enter original length (m): ")
    change_len = get_positive_float("Enter change in length (m): ")

    test = StressStrainTest(selected_mat, force, area, orig_len, change_len)
    test_history.append(test)

    print("\n" + "-" * 35)
    print(f"Result for {selected_mat.name}:")
    print(f"Stress = {test.stress:,.0f} Pa")
    print(f"Strain = {test.strain}")
    print(f"Status: {'FAILED' if test.will_fail() else 'PASSED'}")
    print("-" * 35)

def save_results_json(test_history: list):
    if not test_history:
        print("\nNo history available to save.")
        return

    filename = input("Enter output JSON filename (default: results.json): ").strip()
    if not filename:
        filename = "results.json"
    if not filename.endswith(".json"):
        filename += ".json"

    try:
        data = [t.to_dict() for t in test_history]
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
        print(f"\nSuccessfully saved {len(test_history)} test record(s) to '{filename}'.")
    except OSError as e:
        print(f"\nError saving file: {e}")

def load_results_json(test_history: list):
    filename = input("Enter JSON filename to load (default: results.json): ").strip()
    if not filename:
        filename = "results.json"

    try:
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)

        loaded_tests = [StressStrainTest.from_dict(item) for item in data]
        test_history.extend(loaded_tests)
        print(f"\nSuccessfully loaded {len(loaded_tests)} test record(s) from '{filename}'.")
    except FileNotFoundError:
        print(f"\nError: File '{filename}' not found.")
    except (json.JSONDecodeError, KeyError, TypeError) as e:
        print(f"\nError: Failed to parse file format ({e}).")
    except OSError as e:
        print(f"\nError reading file: {e}")

def export_test_data_csv(test_history: list):
    if not test_history:
        print("\nNo history available to export.")
        return

    filename = input("Enter output CSV filename (default: results.csv): ").strip()
    if not filename:
        filename = "results.csv"
    if not filename.endswith(".csv"):
        filename += ".csv"

    headers = [
        "Material Name", "Density (kg/m3)", "Yield Strength (Pa)", 
        "Youngs Modulus (Pa)", "Force (N)", "Area (m2)", 
        "Original Length (m)", "Change in Length (m)", 
        "Stress (Pa)", "Strain", "Status"
    ]

    try:
        with open(filename, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(headers)

            for t in test_history:
                writer.writerow([
                    t.material.name,
                    t.material.properties.density,
                    t.material.properties.yield_strength,
                    t.material.properties.typical_youngs_modulus,
                    t.force,
                    t.area,
                    t.original_length,
                    t.change_in_length,
                    t.stress,
                    t.strain,
                    "FAILED" if t.will_fail() else "PASSED"
                ])
        print(f"\nSuccessfully exported {len(test_history)} record(s) to '{filename}'.")
    except OSError as e:
        print(f"\nError exporting to CSV: {e}")

def main():
    materials_db = get_predefined_materials()
    test_history = []

    while True:
        display_menu()
        choice = input("Enter choice (1-6): ").strip()

        if choice == "1":
            run_new_test(materials_db, test_history)
        elif choice == "2":
            if not test_history:
                print("\nNo test results recorded yet.")
            else:
                print(f"\n=== CALCULATION HISTORY ({len(test_history)} tests) ===")
                for idx, t in enumerate(test_history, start=1):
                    print(f"Test #{idx}: {t.material.name} | Stress: {t.stress:,.0f} Pa | Strain: {t.strain}")
        elif choice == "3":
            save_results_json(test_history)
        elif choice == "4":
            load_results_json(test_history)
        elif choice == "5":
            export_test_data_csv(test_history)
        elif choice == "6":
            print("\nExiting program. Goodbye!")
            sys.exit(0)
        else:
            print("Invalid choice. Please enter a number from 1 to 6.")

if __name__ == "__main__":
    main()