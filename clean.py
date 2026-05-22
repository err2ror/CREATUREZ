#Monster Cleaner v1-4
from monsterdb import al_frm as mstrs
monstardb=open("monsterdb.py","w")
from random import choice as coits
'''return {
        "name": random.choice(species) + "-" + str(random.randint(1000, 9999)),
        "color": random.choice(colors),
        "ability": random.choice(abilities),
        "weakness": random.choice(weaknesses),
        "power_level": random.randint(1000, 90000)
    }'''
end=[]
def clean(i):
    name=i["name"]
    color=i["color"]
    ability=i["ability"]
    weakness=i["weakness"]
    power_level=i["power_level"]
    colors=color.split("ish ")
    abilities=ability.split(" and ")
    weaknesses=weakness.split(" and ")
    color=coits(colors)
    ability=coits(abilities)
    weakness=coits(weaknesses)
    return {
        "name": name,
        "color": color,
        "ability": ability,
        "weakness": weakness,
        "power_level": power_level
    }
print("Enumerating total creatures...") # by this point creature=monster
print(f"{len(mstrs)} creatures found.")
tot=len(mstrs)
xabcd=input("Do you want to clean the monster file? [Yes/No/Log]: ").lower()
if xabcd == "n":
    exit(0)
if xabcd != "l":
    for i in mstrs:
        end.append(clean(i))
else:
    count=1
    for i in mstrs:
        end.append(clean(i))
        print(f"Cleaned monster n°{count}/{tot}")
        count+=1
def save(file):
    global monstardb
    azertyuiop="al_frm="+str(file)
    monstardb.write(azertyuiop)
save(end)
