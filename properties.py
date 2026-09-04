def main():

    print("=== Stress and Strain Calculator ===")
    print()

    force = float(input("Enter applied force(in Newtons): ").replace(",", ""))
    area = float(input("Enter cross-sectional area(in square meters): ").replace(",", ""))
    original_len = float(input("Enter length(in m): ").replace(",", ""))
    change_len = float(input("Enter change in length(in m): ").replace(",", ""))

    stress = force / area
    strain = change_len / original_len

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
    print()

    stress_mpa = stress / 1_000_000
    print(f"Stress in MPa: {stress_mpa:.2f} MPa")
    if change_len > 0:
        print("Loading Type: Tension")
    elif change_len < 0:
        print("Loading Type: Compression")
    else:
        print("Loading Type: Neither (No change in length)")

    print()
    print("=== Analysis Complete ===")

if __name__ == "__main__":
    main()

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
   
