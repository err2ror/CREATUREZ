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

def breed(a, b):
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

# generate creatures
all_creats = [make_creature() for _ in range(5)]
all_mstrs = [make_monster() for _ in range(5)]
# pick parents
print("Creatures:")
for i, c in enumerate(all_creats):
    print(i, c)
print("Monsters:")
for i, c in enumerate(all_mstrs):
    print(i, c)
al={"m":all_mstrs,"c":all_creats}
a = list(input("Pick creature A [Monster/Creature] [0-4]: ").lower())
b = list(input("Pick creature B [Monster/Creature] [0-4]: ").lower()) #input sanitizing via lower()
type_a=a[0]
type_b=b[0]
num_a=int(a[1])
num_b=int(b[1])
crea_a=al[type_a][num_a]
crea_b=al[type_b][num_b] #pls put this in breed function and make it better this is just stupid
print(crea_a)
print(crea_b)
print("\nBreeding result:\n")
print(breed(crea_a, crea_b))

