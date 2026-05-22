from monsterdb import al_frm

def nice(x):
    print(x["name"])
    print("Color:", x["color"])
    print("Ability:", x["ability"])
    print("Weakness:", x["weakness"])
    print("Power:", x["power_level"])

# Input
xa = al_frm[int(input("Smol ID: "))]
ya = al_frm[int(input("Beeg ID: "))]

# Display
nice(xa)
print("\nVS\n")
nice(ya)
print(f"\n…but {xa['name']} can multiply.\n")

# Values
x = xa["power_level"]
y = ya["power_level"]
xn = xa["name"]
yn = ya["name"]

num = 1

def bonusz(z, w):
    return round((z * w) * ((w / 10) + 0.9), 1)

totpowah = x

# Scaling loop
while totpowah < y:
    totpowah = bonusz(x, num)
    print(f"{xn}: {x} power * {num} copies * {round((num/10)+0.9, 1)} team bonus = "
          f"{totpowah} total power, vs {yn}: {y} power, power diff: {round(y - totpowah, 1)}")
    num += 1

