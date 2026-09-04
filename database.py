from dataclasses import dataclass
from typing import List

def procedural_main():
    test_history = []
    unique_materials = set()
    UNITS = ("N", "m²", "m", "Pa")
   
    materials_indx = {
        "steel": {"yield_strength": 250000000, "youngs_modulus": 200000000000},
        "plastic": {"yield_strength": 70000000, "youngs_modulus": 2800000000},
        "composite": {"yield_strength": 600000000, "youngs_modulus": 70000000000}
    }

    while True:
        print("\nAvailable materials in database: steel, plastic, composite")

        material_inp = input("Enter material name (or 'quit' to exit): ").strip().lower()
        if material_inp == 'quit':
            break
        if material_inp not in materials_indx:
            print("Error: Material not found in database")
            continue
            
        try:
            force = float(input(f"Enter force ({UNITS[0]}): "))
            area = float(input(f"Enter area ({UNITS[1]}): "))
            original_length = float(input(f"Enter original length ({UNITS[2]}): "))
            change_in_length = float(input(f"Enter change in length ({UNITS[2]}): "))
            
            if force <= 0 or area <= 0 or original_length <= 0 or change_in_length <= 0:
                print("Error: All dimensions and forces must be positive numbers!")
                continue

            stress = force / area
            strain = change_in_length / original_length

            mat_ = materials_indx[material_inp]
            yield_stren = mat_["yield_strength"]
            ym_ = mat_["youngs_modulus"]

            safety_factor = yield_stren / stress
            if safety_factor >= 1.0:
                safety_status = f"SAFE (SF: {round(safety_factor, 2)})"
            else:
                safety_status = f"UNSAFE (SF: {round(safety_factor, 2)})"

            index_ = {
                "material": material_inp.capitalize(),
                "force": force,
                "area": area,
                "original length": original_length,
                "change in length": change_in_length,
                "stress": stress,
                "strain": strain,
                "Young's modulus": ym_,
                "safety result": safety_status,
                "safety_factor_raw": safety_factor
            }
            test_history.append(index_)
            unique_materials.add(material_inp.capitalize())

            print(f"\nResult for {index_['material']}___")
            print(f"Stress          : {round(stress, 2)} {UNITS[3]}")
            print(f"Strain          : {round(strain, 6)}")
            print(f"Safety Result   : {safety_status}")

        except ValueError:
            print("Error: Invalid input. Please enter numeric values.")
        except ZeroDivisionError:
            print("Error: Area and original length cannot be zero!")

    print("\n___ SESSION SUMMARY ___")
    print("Total calculations:", len(test_history))
    print("Unique materials tested:", unique_materials)

    if len(test_history) > 0:
        print("\nDetailed Calculation History")
        for idx, item in enumerate(test_history, start=1):
            print(f"Test #{idx}: {item['material']} | Stress: {round(item['stress'], 2)} {UNITS[3]} | Result: {item['safety result']}")

        highest_stress = max(item["stress"] for item in test_history)
        lowest_sf = min(item["safety_factor_raw"] for item in test_history)
        avg_strain = sum(item["strain"] for item in test_history) / len(test_history)

        print("\nSession Statistics___")
        print(f"Highest Stress       : {round(highest_stress, 2)} {UNITS[3]}")
        print(f"Lowest Safety Factor : {round(lowest_sf, 2)}")
        print(f"Average Strain       : {round(avg_strain, 6)}")

        print("\nMaterial Test Counts:")
        mat_counts = {}
        for item in test_history:
            mat = item["material"]
            mat_counts[mat] = mat_counts.get(mat, 0) + 1

        for mat, count in mat_counts.items():
            print(f"  - {mat}: {count} test(s)")
    else:
        print("No test calculations were recorded during this session.")

    print("___")


# task 6

@dataclass
class MaterialProperties:
    density: float
    yield_strength: float
    typical_youngs_modulus: float

class Material:
    def __init__(self, name: str, properties: MaterialProperties):
        self.name = name
        self.properties = properties

    def can_withstand_stress(self, stress: float) -> bool:
        return stress < self.properties.yield_strength

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
        return not self.material.can_withstand_stress(self.stress)

def oop_main():
    materials_db = {
        "steel": Material("Steel", MaterialProperties(7850, 250000000, 200000000000)),
        "plastic": Material("Plastic", MaterialProperties(1150, 70000000, 2800000000)),
        "composite": Material("Composite", MaterialProperties(1600, 600000000, 70000000000)),
    }
    
    test_history: List[StressStrainTest] = []

    while True:
        print("\nAvailable materials in database: steel, plastic, composite")
        material_inp = input("Enter material name (or 'quit'): ").strip().lower()
        if material_inp == 'quit':
            break

        if material_inp not in materials_db:
            print("Error: Material not found.")
            continue

        try:
            selected_material = materials_db[material_inp]
            force = float(input("Enter force (N): "))
            area = float(input("Enter area (m²): "))
            orig_len = float(input("Enter original length (m): "))
            change_len = float(input("Enter change in length (m): "))

            if force <= 0 or area <= 0 or orig_len <= 0 or change_len <= 0:
                print("Error: All inputs must be positive numbers!")
                continue

            test = StressStrainTest(selected_material, force, area, orig_len, change_len)
            test_history.append(test)

            print(f"\nResult for {test.material.name}:")
            print(f"Stress: {test.stress:.2f} Pa")
            print(f"Status: {'FAILED' if test.will_fail() else 'PASSED'}")
            
        except ValueError:
            print("Error: Invalid numeric input.")
        except ZeroDivisionError:
            print("Error: Area and original length cannot be zero.")

if __name__ == "__main__":
    procedural_main()
