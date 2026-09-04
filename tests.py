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