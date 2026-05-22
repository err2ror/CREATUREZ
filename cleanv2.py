# Monster Cleaner v2-4
from monsterdb import al_frm as mstrs
from random import choice as pick

monstardb = open("monsterdb.py", "w")

def clean(mon):
    # Split attributes into lists
    colors = mon["color"].split("ish ")
    abilities = mon["ability"].split(" and ")
    weaknesses = mon["weakness"].split(" and ")

    return {
        "name": mon["name"],
        "color": pick(colors),
        "ability": pick(abilities),
        "weakness": pick(weaknesses),
        "power_level": mon["power_level"]
    }

print("Enumerating total creatures...")
print(f"{len(mstrs)} creatures found.")

mode = input("Clean monster file? [Yes/No/Log]: ").lower()
if mode == "n":
    exit()

end = []
total = len(mstrs)

if mode == "l":
    for i, mon in enumerate(mstrs, start=1):
        cleaned = clean(mon)
        end.append(cleaned)
        print(f"Cleaned monster {i}/{total}")
else:
    for mon in mstrs:
        end.append(clean(mon))

def save(file):
    monstardb.write("al_frm=" + str(file))

save(end)

