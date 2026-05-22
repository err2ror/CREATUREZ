def nice(x):
    print(x["name"] + "'s stats")
    print("Color: " + x["color"])
    print("Ability: " + x["ability"])
    print("Weakness: " + x["weakness"])
    print("Power: " + str(x["power_level"]))
def creatselect()
    print("All available creatures/monsters:")
    for i, c in enumerate(al_frm):
        print(i, c["name"])
    try:
        a = int(input(f"Pick A (0-{len(al_frm)-1}): "))
        b = int(input(f"Pick B (0-{len(al_frm)-1}): "))
    except:
        print("Invalid input.")
        exit()

