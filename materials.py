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

def create_analysis_record(material_name: str, stress: float, strain: float, modulus: float, fos: float) -> dict:
    return {
        "material": material_name,
        "stress_pa": stress,
        "strain": strain,
        "youngs_modulus_pa": modulus,
        "factor_of_safety": fos
    }


def add_to_history(history: list[dict], record: dict) -> None:
    history.append(record)


def get_history(history: list[dict]) -> list[dict]:
    return history

def compute_all_properties(force: float, area: float, orig_len: float, dl: float, yield_strength: float) -> dict:
    stress = calculate_stress(force, area)
    strain = calculate_strain(dl, orig_len)
    modulus = calculate_youngs_modulus(stress, strain)
    fos = calculate_factor_of_safety(yield_strength, stress)
    
    return {
        "stress": stress,
        "strain": strain,
        "modulus": modulus,
        "fos": fos
    }

from dataclasses import dataclass

@dataclass
class Material:
    name: str
    yield_strength: float

    def get_yield_strength_mpa(self) -> float:
        return self.yield_strength / 1e6

    def is_safe(self, applied_stress: float) -> bool:
        return applied_stress < self.yield_strength

from dataclasses import dataclass

@dataclass
class StressStrainTest:
    material: Material
    force: float
    area: float
    original_length: float
    change_in_length: float

    @property
    def stress(self) -> float:
        return self.force / self.area

    @property
    def strain(self) -> float:
        return self.change_in_length / self.original_length

    @property
    def youngs_modulus(self) -> float:
        return self.stress / self.strain if self.strain > 0 else 0.0

    @property
    def factor_of_safety(self) -> float:
        return self.material.yield_strength / self.stress