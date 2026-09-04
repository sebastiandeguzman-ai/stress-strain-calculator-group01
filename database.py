# Key additions:
def main():

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
        print("  ")
        print("Available materials in database: steel, aluminum, copper")

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

        # Key additions:
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

        print("  ")
        print("  ")
        print(f"Result for {index_['material']}___")
        print(f"Stress          : {round(stress, 2)} {UNITS[3]}")
        print(f"Strain          : {round(strain, 6)}")
        print(f"Safety Result   : {safety_status}")
        pass

    except ValueError:
        print("Error: Invalid input. Please enter numeric values.")
    except ZeroDivisionError:
        print("Error: Area and original length cannot be zero!")
    except KeyError:
        print("Error: Material not found in database!")

    # Key additions:
    print("___")
    print("SESSION SUMMARY")
    print("___")
    print("Total calculations:", len(test_history))
    print("Unique materials tested:", unique_materials)

    if len(test_history) > 0:
        print("  ")
        print("Detailed Calculation History")
        for idx, item in enumerate(test_history, start=1):
            print(f"Test #{idx}: {item['material']} | Stress: {round(item['stress'], 2)} {UNITS[3]} | Result: {item['safety result']}")

    # Key additions:
        highest_stress = max(item["stress"] for item in test_history)
        lowest_sf = min(item["safety_factor_raw"] for item in test_history)
        avg_strain = sum(item["strain"] for item in test_history) / len(test_history)

        print("  ")
        print("Session Statistics___")
        print(f"Highest Stress       : {round(highest_stress, 2)} {UNITS[3]}")
        print(f"Lowest Safety Factor : {round(lowest_sf, 2)}")
        print(f"Average Strain       : {round(avg_strain, 6)}")

        print("  ")
        print("Material Test Counts:")
        mat_counts = {}
        for item in test_history:
            mat = item["material"]
            mat_counts[mat] = mat_counts.get(mat, 0) + 1

        
        for mat, count in mat_counts.items():
            print(f"  - {mat}: {count} test(s)")
    else:
        print("No test calculations were recorded during this session.")

    print("___")
    
if __name__ == "__main__":
    main()
