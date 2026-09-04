from dataclasses import dataclass
from typing import Optional, List

@dataclass
class MaterialProperties:
    density: float  # kg/m³
    yield_strength: float  # MPa
    typical_youngs_modulus: float  # GPa

    def __post_init__(self):
        if self.density <= 0:
            raise ValueError("Density must be positive")
        if self.yield_strength <= 0:
            raise ValueError("Yield strength must be positive")
        if self.typical_youngs_modulus <= 0:
            raise ValueError("Young's modulus must be positive")

class Material:
    def __init__(self, name: str, properties: MaterialProperties):
        self.name = name
        self.properties = properties

    def __str__(self) -> str:
        return (
            f"{self.name} "
            f"(Density: {self.properties.density} kg/m³)")

    def can_withstand_stress(self, stress: float) -> bool:
        if stress < 0:
            raise ValueError("Stress cannot be negative")
        return stress < self.properties.yield_strength

    def __eq__(self, other) -> bool:
        if not isinstance(other, Material):
            return NotImplemented
        return (
            self.name == other.name
            and self.properties == other.properties)

class StressStrainTest:
    def __init__(
        self,
        material: Material,
        force: float,
        area: float,
        original_length: float,
        change_in_length: float,):
        self.material = material
        self._force = force
        self._area = area
        self._original_length = original_length
        self._change_in_length = change_in_length

        if force <= 0:
            raise ValueError("Force must be positive")
        if area <= 0:
            raise ValueError("Area must be positive")
        if original_length <= 0:
            raise ValueError("Original length must be positive")

    @property
    def stress(self) -> float:
        return self._force / self._area

    @property
    def strain(self) -> float:
        return self._change_in_length / self._original_length

    @property
    def youngs_modulus(self) -> Optional[float]:
        if self.strain == 0:
            return None
        return (self.stress / self.strain) / 1000

    def will_fail(self) -> bool:
        return not self.material.can_withstand_stress(
            self.stress)

    def __str__(self) -> str:
        if self.youngs_modulus is None:
            modulus = "Undefined"
        else:
            modulus = f"{self.youngs_modulus:.2f} GPa"
        return (
            f"Test on {self.material.name}: "
            f"Stress={self.stress:.2f} MPa, "
            f"Strain={self.strain:.6f}, "
            f"Young's Modulus={modulus}")

class Metal(Material):
    def __init__(
        self,
        name: str,
        properties: MaterialProperties,
        is_ferrous: bool = False):
        super().__init__(name, properties)
        self.is_ferrous = is_ferrous

    def __str__(self) -> str:
        metal_type = (
            "Ferrous" if self.is_ferrous else "Non-ferrous")
        return (
            f"{self.name} "
            f"({metal_type} metal, "
            f"Density: {self.properties.density} kg/m³)")

class Plastic(Material):
    def __init__(
        self,
        name: str,
        properties: MaterialProperties,
        is_flexible: bool = False):
        super().__init__(name, properties)
        self.is_flexible = is_flexible

    def __str__(self) -> str:
        plastic_type = (
            "Flexible" if self.is_flexible else "Rigid")
        return (
            f"{self.name} "
            f"({plastic_type} plastic, "
            f"Density: {self.properties.density} kg/m³)")

class Composite(Material):
    def __init__(
        self,
        name: str,
        properties: MaterialProperties,
        is_reinforced: bool = True):
        super().__init__(name, properties)
        self.is_reinforced = is_reinforced

    def __str__(self) -> str:
        composite_type = (
            "Reinforced"
            if self.is_reinforced
            else "Non-reinforced")

        return (
            f"{self.name} "
            f"({composite_type} composite, "
            f"Density: {self.properties.density} kg/m³)")