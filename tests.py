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

@dataclass
class TestResult:
    material_name: str
    stress: float
    strain: float
    youngs_modulus: Optional[float]
    failed: bool

class TestAnalysis:
    def __init__(self):
        self.tests: List[StressStrainTest] = []

    def add_test(self, test: StressStrainTest):
        if not isinstance(test, StressStrainTest):
            raise TypeError("Only StressStrainTest objects can be added")

        self.tests.append(test)

    def get_results(self) -> List[TestResult]:
        results = []
        for test in self.tests:
            results.append(
                TestResult(
                    material_name=test.material.name,
                    stress=test.stress,
                    strain=test.strain,
                    youngs_modulus=test.youngs_modulus,
                    failed=test.will_fail()))
        return results

    def compare_materials(self):
        if not self.tests:
            print("No tests available.")
            return

        print("\n----- MATERIAL COMPARISON -----")

        for test in self.tests:
            status = (
                "FAILED"
                if test.will_fail()
                else "PASSED")
            print(
                f"{test.material.name}: "
                f"Stress={test.stress:.2f} MPa | "
                f"Yield Strength="
                f"{test.material.properties.yield_strength:.2f} MPa | "
                f"Status={status}")

    def strongest_material(self) -> Optional[Material]:
        if not self.tests:
            return None

        strongest_test = max(
            self.tests,
            key=lambda test:
            test.material.properties.yield_strength)

        return strongest_test.material

    def summary_report(self):
        if not self.tests:
            print("No test results available.")
            return

        print("\n===== STRESS-STRAIN TEST REPORT =====")

        for number, test in enumerate(self.tests, start=1):

            print(f"\nTest {number}")
            print(test)
            print(
                f"Typical Young's Modulus: "
                f"{test.material.properties.typical_youngs_modulus:.2f} GPa")
            print(
                f"Result: "
                f"{'FAILED' if test.will_fail() else 'PASSED'}")

        strongest = self.strongest_material()

        if strongest:
            print("-" * 35)
            print(
                f"Strongest Material: {strongest.name}")
            print(
                f"Yield Strength: "
                f"{strongest.properties.yield_strength:.2f} MPa")
            print("-" * 35)

# Material Properties
steel_properties = MaterialProperties(
    density=7850,
    yield_strength=250,
    typical_youngs_modulus=200)

aluminum_properties = MaterialProperties(
    density=2700,
    yield_strength=276,
    typical_youngs_modulus=69)

nylon_properties = MaterialProperties(
    density=1150,
    yield_strength=70,
    typical_youngs_modulus=2.8)

carbon_fiber_properties = MaterialProperties(
    density=1600,
    yield_strength=600,
    typical_youngs_modulus=70)

# Material Objects
steel = Metal(
    "Steel",
    steel_properties,
    is_ferrous=True)

aluminum = Metal(
    "Aluminum",
    aluminum_properties,
    is_ferrous=False)

nylon = Plastic(
    "Nylon",
    nylon_properties,
    is_flexible=True)

carbon_fiber = Composite(
    "Carbon Fiber",
    carbon_fiber_properties,
    is_reinforced=True)

# Tests
steel_test = StressStrainTest(
    steel,
    force=5000,
    area=25,
    original_length=100,
    change_in_length=0.5)

aluminum_test = StressStrainTest(
    aluminum,
    force=6000,
    area=25,
    original_length=100,
    change_in_length=0.8)

nylon_test = StressStrainTest(
    nylon,
    force=2000,
    area=25,
    original_length=100,
    change_in_length=2)

carbon_fiber_test = StressStrainTest(
    carbon_fiber,
    force=10000,
    area=25,
    original_length=100,
    change_in_length=0.3)

analysis = TestAnalysis()
analysis.add_test(steel_test)
analysis.add_test(aluminum_test)
analysis.add_test(nylon_test)
analysis.add_test(carbon_fiber_test)


print("===== MATERIALS =====")
print(steel)
print(aluminum)
print(nylon)
print(carbon_fiber)

print("\n----- INDIVIDUAL TEST -----")
print(steel_test)

print(
    f"Will the material fail? "
    f"{'Yes' if steel_test.will_fail() else 'No'}")

print(
    f"Calculated Young's modulus: "
    f"{steel_test.youngs_modulus:.2f} GPa")

print(
    f"Typical Young's modulus: "
    f"{steel.properties.typical_youngs_modulus:.2f} GPa")

analysis.compare_materials()
analysis.summary_report()

same_steel = Metal(
    "Steel",
    MaterialProperties(
        density=7850,
        yield_strength=250,
        typical_youngs_modulus=200
    ),
    is_ferrous=True)

print("\n======= OBJECT COMPARISON =======")

print(
    f"Are the steel objects equal? "
    f"{steel == same_steel}")