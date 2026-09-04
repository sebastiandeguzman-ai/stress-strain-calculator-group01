# Key additions:
test_history = []
unique_materials = set()
UNITS = ("N", "m²", "m", "Pa")
materials_indx = {
    "steel": {"yield_strength": 250000000, "youngs_modulus": 200000000000},
    "aluminum": {"yield_strength": 95000000, "youngs_modulus": 69000000000},
    "copper": {"yield_strength": 70000000, "youngs_modulus": 117000000000}
}

# Key additions:
while True:
    material_inp = input("Enter material name (or 'quit' to exit): ").strip().lower()
    if material_inp == 'quit':
        break
    if material_inp not in materials_indx:
        print("Error: Material not found in database")
        continue

    force = float(input(f"Enter force ({UNITS[0]}): "))
    area = float(input(f"Enter area ({UNITS[1]}): "))
    original_length = float(input(f"Enter original length ({UNITS[2]}): "))
    change_in_length = float(input(f"Enter change in length ({UNITS[2]}): "))

    if force <= 0 or area <= 0 or original_length <= 0 or change_in_length <= 0:
        print("Error: All dimensions and forces must be positive numbers!")
        continue