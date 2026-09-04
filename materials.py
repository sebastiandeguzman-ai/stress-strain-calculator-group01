from dataclasses import dataclass
from properties import MaterialProperties


class Material:
    """Base class representing a general material."""

    def __init__(self, name: str, properties: MaterialProperties):
        self.name = name
        self.properties = properties

    def __str__(self) -> str:
        return f"{self.name} (Density: {self.properties.density} kg/m³)"

    def can_withstand_stress(self, stress_pa: float) -> bool:
        """Check if material can withstand a given stress without yielding."""
        if stress_pa < 0:
            raise ValueError("Stress cannot be negative.")
        return stress_pa < self.properties.yield_strength

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Material):
            return NotImplemented
        return self.name == other.name and self.properties == other.properties

class Metal(Material):
    """Subclass representing metallic materials."""

    def __init__(self, name: str, properties: MaterialProperties, is_ferrous: bool = False):
        super().__init__(name, properties)
        self.is_ferrous = is_ferrous

    def __str__(self) -> str:
        metal_type = "Ferrous" if self.is_ferrous else "Non-ferrous"
        return f"{self.name} ({metal_type} metal, Density: {self.properties.density} kg/m³)"

class Plastic(Material):
    """Subclass representing polymer/plastic materials."""

    def __init__(self, name: str, properties: MaterialProperties, is_flexible: bool = False):
        super().__init__(name, properties)
        self.is_flexible = is_flexible

    def __str__(self) -> str:
        plastic_type = "Flexible" if self.is_flexible else "Rigid"
        return f"{self.name} ({plastic_type} plastic, Density: {self.properties.density} kg/m³)"

class Composite(Material):
    """Subclass representing composite materials."""

    def __init__(self, name: str, properties: MaterialProperties, is_reinforced: bool = True):
        super().__init__(name, properties)
        self.is_reinforced = is_reinforced

    def __str__(self) -> str:
        composite_type = "Reinforced" if self.is_reinforced else "Non-reinforced"
        return f"{self.name} ({composite_type} composite, Density: {self.properties.density} kg/m³)"


def validate_input(force: float, area: float, original_length: float, change_in_length: float) -> bool:
    """Validate that all engineering inputs are positive non-zero numbers."""
    if not all(
        isinstance(v, (int, float)) and not isinstance(v, bool)
        for v in (force, area, original_length, change_in_length)
    ):
        raise TypeError("All numeric inputs must be floats or integers.")

    if force <= 0:
        raise ValueError("Force must be greater than zero.")
    if area <= 0:
        raise ValueError("Area must be greater than zero.")
    if original_length <= 0:
        raise ValueError("Original length must be greater than zero.")
    if change_in_length <= 0:
        raise ValueError("Change in length must be greater than zero.")

    return True


def calculate_stress(force: float, area: float) -> float:
    """Calculate tensile/compressive stress in Pascals (N/m²)."""
    if area == 0:
        raise ZeroDivisionError("Area cannot be zero.")
    return force / area

def calculate_strain(original_length: float, change_in_length: float) -> float:
    """Calculate dimensionless strain (change in length / original length)."""
    if original_length == 0:
        raise ZeroDivisionError("Original length cannot be zero.")
    return change_in_length / original_length

def calculate_youngs_modulus(stress: float, strain: float) -> float:
    """Calculate Young's Modulus in Pascals (stress / strain)."""
    if strain == 0:
        raise ZeroDivisionError("Strain cannot be zero when calculating Young's modulus.")
    return stress / strain

def calculate_factor_of_safety(yield_strength: float, working_stress: float) -> float:
    """Calculate factor of safety (yield strength / working stress)."""
    if working_stress == 0:
        raise ZeroDivisionError("Working stress cannot be zero.")
    return yield_strength / working_stress

def main_calculator(material: Material, force: float, area: float, original_length: float, change_in_length: float) -> dict:
    """Orchestrate input validation, mechanical calculations, and record creation."""
    try:
        validate_input(force, area, original_length, change_in_length)

        stress = calculate_stress(force, area)
        strain = calculate_strain(original_length, change_in_length)
        youngs_modulus = calculate_youngs_modulus(stress, strain)

        yield_strength = getattr(
            material, "yield_strength", None
        ) or getattr(getattr(material, "properties", None), "yield_strength", None)

        factor_of_safety = None
        is_safe = None

        if yield_strength is not None and yield_strength > 0:
            factor_of_safety = calculate_factor_of_safety(yield_strength, stress)
            is_safe = material.can_withstand_stress(stress) if hasattr(material, "can_withstand_stress") else (stress < yield_strength)

        return {
            "material": getattr(material, "name", str(material)),
            "force_n": force,
            "area_m2": area,
            "original_length_m": original_length,
            "change_in_length_m": change_in_length,
            "stress_pa": stress,
            "strain": strain,
            "youngs_modulus_pa": youngs_modulus,
            "factor_of_safety": factor_of_safety,
            "is_safe": is_safe,
        }

    except (ValueError, TypeError, ZeroDivisionError) as e:
        print(f"Calculation Error: {e}")
        return {"error": str(e)}