import random
needsinit=False
try:
    from monsterdb import al_frm
    monstardb=open("monsterdb.py","w")
except:
    needsinit=True
    monstardb=open("monsterdb.py","w")
def nice(x):
    print(x["name"] + "'s stats")
    print("Color: " + x["color"])
    print("Ability: " + x["ability"])
    print("Weakness: " + x["weakness"])
    print("Power: " +  str(x["power_level"]))
def make_creature():
    species = ["Blob", "Gorf", "Zibble", "Snorf", "Wumpus", "Glip"]
    colors = ["red", "blue", "green", "purple", "neon yellow", "transparent"]
    abilities = ["teleports badly", "screams politely", "eats electricity", "vibrates", "floats sometimes", "knows your secrets"]
    weaknesses = ["water", "math", "loud noises", "Mondays", "gravity", "social interaction"]

    return {
        "name": random.choice(species) + "-" + str(random.randint(100, 999)),
        "color": random.choice(colors),
        "ability": random.choice(abilities),
        "weakness": random.choice(weaknesses),
        "power_level": random.randint(1, 9000)
    }

def make_monster():
    species = ["Blug", "Gorfo", "Zibbler", "Snooor", "Wumpo", "Glop"]
    colors = ["red", "blue", "green", "purple", "neon yellow", "raimbow", "transparent"]
    abilities = ["teleports", "screams", "eats electricity", "vibrates", "floats sometimes", "knows your secrets"]
    weaknesses = ["fire", "english", "absence of noises", "Sundays", "space", "loneliness"]

    return {
        "name": random.choice(species) + "-" + str(random.randint(1000, 9999)),
        "color": random.choice(colors),
        "ability": random.choice(abilities),
        "weakness": random.choice(weaknesses),
        "power_level": random.randint(1000, 90000)
    }

def genbrdrndtxt(x, y):
    return "".join(random.choice([a, b]) for a, b in zip(x, y))

def breedraw(a, b, secretconfig=None):
    nameA, idA = a["name"].split("-")
    nameB, idB = b["name"].split("-")

    new_name = genbrdrndtxt(nameA, nameB)
    new_id = str(int(idA) + int(idB))

    # config handling
    noconfig = True
    if secretconfig and secretconfig.get("exists"):
        noconfig = False

    if noconfig:
        color = f"{a['color']}ish {b['color']}"
        ability = f"{a['ability']} and {b['ability']}"
        weakness = f"{a['weakness']} and {b['weakness']}"
    elif secretconfig["truncate"]:
        color = random.choice([a["color"], b["color"]])
        ability = random.choice([a["ability"], b["ability"]])
        weakness = random.choice([a["weakness"], b["weakness"]])
    else:
        color = f"{a['color']}ish {b['color']}"
        ability = f"{a['ability']} and {b['ability']}"
        weakness = f"{a['weakness']} and {b['weakness']}"

    power_level = a["power_level"] + b["power_level"]

    return {
        "name": new_name + "-" + new_id,
        "color": color,
        "ability": ability,
        "weakness": weakness,
        "power_level": power_level
    }

def breed(code_a, code_b, creatures, monsters, secretconfig=None):
    pool = {"c": creatures, "m": monsters}

    type_a, idx_a = code_a[0], int(code_a[1])
    type_b, idx_b = code_b[0], int(code_b[1])

    a = pool[type_a][idx_a]
    b = pool[type_b][idx_b]

    return breedraw(a, b, secretconfig=secretconfig)

# generate lists
if needsinit == True:
    creatures = [make_creature() for _ in range(5)]
    monsters = [make_monster() for _ in range(5)]
    al_frm = creatures + monsters
print("All creatures:")
for i, c in enumerate(al_frm):
    print(i, c)

config = {
    "truncate": False,
    "exists": True
}
def save(file):
    global monstardb
    azertyuiop="al_frm="+str(file)
    monstardb.write(azertyuiop)
def parsechc(ab):
    global al_frm, config
    if ab in ("autobreed", "chaos"):
        maxtimes=int(input("How many breeds do you want? [WILL NOT SAVE IF YOU TERMINATE BEFORE END]: "))
        print(maxtimes)
        for i in range(maxtimes):
            print(i)
            new = breedraw(random.choice(al_frm), random.choice(al_frm), secretconfig=config)
            al_frm.append(new)
            print("New breed:")
            print(new)
        return 1
    if ab == "truncate":
        config["truncate"] = True
        return 5  # needs another cheat code
    if ab == "exit":
        return 3  # continue script
    return 1  # exit program

a = input(f"Pick A (0-{len(al_frm)-1}): ").lower()

# easter egg
if a == "supersecretpassword123123123":
    print("You found an easteregg!")
    x = 5
    while x == 5:
        x = parsechc(input("You can enter a cheat code!: "))
    if x == 1:
        save(al_frm)
        exit()
    if x == 3:
        a = input(f"Pick A (0-{len(al_frm)-1}): ").lower()

b = input(f"Pick B (0-{len(al_frm)-1}): ").lower()

print("\nBreeding result (Raw):\n")
final=breedraw(al_frm[int(a)], al_frm[int(b)], secretconfig=config)
print(final)
print("\nBreeding result (Fancy):\n")
nice(final)
al_frm.append(final)
save(al_frm)
