# Key additions:
test_history = []
unique_materials = set()
UNITS = ("N", "m²", "m", "Pa")
materials_indx = {
    "steel": {"yield_strength": 250000000, "youngs_modulus": 200000000000},
    "aluminum": {"yield_strength": 95000000, "youngs_modulus": 69000000000},
    "copper": {"yield_strength": 70000000, "youngs_modulus": 117000000000}
}
