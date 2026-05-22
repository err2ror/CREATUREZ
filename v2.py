import random

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
def breedraw(crea_a,crea_b):
    #breeds raw creatures instead of parsing from pool
    a,b=crea_a,crea_b
    
    nameA, idA = a["name"].split("-")
    nameB, idB = b["name"].split("-")

    new_name = genbrdrndtxt(nameA, nameB)
    new_id = str(int(idA) + int(idB))

    return {
        "name": new_name + "-" + new_id,
        "color": f"{a['color']}ish {b['color']}",
        "ability": f"{a['ability']} and {b['ability']}",
        "weakness": f"{a['weakness']} and {b['weakness']}",
        "power_level": a["power_level"] + b["power_level"]
    }
def breed(code_a, code_b, creatures, monsters):
    # decode "c3" or "m1"
    type_a, idx_a = code_a[0], int(code_a[1])
    type_b, idx_b = code_b[0], int(code_b[1])

    pool = {"c": creatures, "m": monsters}

    a = pool[type_a][idx_a]
    b = pool[type_b][idx_b]

    breedraw(a,b)
# generate lists
creatures = [make_creature() for _ in range(5)]
monsters = [make_monster() for _ in range(5)]
al_frm=creatures+monsters
print("Creatures:")
for i, c in enumerate(creatures):
    print(i, c)

print("\nMonsters:")
for i, m in enumerate(monsters):
    print(i, m)
breeds=[]
# user input
valida=["c0","c1","c2","c3","c4","m0","m1","m2","m3","m4"]
a = input("Pick A (c0–c4 or m0–m4): ").lower()
b = input("Pick B (c0–c4 or m0–m4): ").lower()
if a == "supersecretpassword123123123":
    print("You found an easteregg!")
    ab=input("You can enter a cheat code!:")
    if ab == "autobreed" or ab == "chaos":
        while True:
            new=breedraw(random.choice(al_frm),random.choice(al_frm))
            al_frm.append(new)
            print("New breed:")
            print(new)
print("\nBreeding result:\n")
print(breed(a, b, creatures, monsters))

