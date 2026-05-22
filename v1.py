import random
def make_creature():
    species = ["Blob", "Gorf", "Zibble", "Snorf", "Wumpus", "Glip"]
    colors = ["red", "blue", "green", "purple", "neon yellow", "transparent"]
    abilities = ["teleports badly", "screams politely", "eats electricity", "vibrates", "floats sometimes", "knows your secrets"]
    weaknesses = ["water", "math", "loud noises", "Mondays", "gravity", "social interaction"]

    creature = {
        "name": random.choice(species) + "-" + str(random.randint(100, 999)),
        "color": random.choice(colors),
        "ability": random.choice(abilities),
        "weakness": random.choice(weaknesses),
        "power_level": random.randint(1, 9000)
    }

    return creature
all_creats=[]
for i in range(1,10):
    all_creats.append(make_creature())
def genbrdrndtxt(x,y):
    end=""
    x=list(x)
    y=list(y)
    for i in list(range(0,min(len(x),len(y)))):
        if random.random() > 0.5:
            end+=x[i]
        else:
            end+=y[i]
    return end
def breed(a,b):
    speci = genbrdrndtxt(a["name"],b["name"])
    print(speci)
    print("-")
    print(str(int((a["name"].split("-"))[1])+int(b["name"].split("-")[1])))
    creature = {
        "name": speci + "-" + str(int((a["name"].split("-"))[1])+int(b["name"].split("-")[1])),
        "color": a["color"]+"ish "+b["color"],
        "ability": a["ability"]+" and "+b["ability"],
        "weakness": a["weakness"]+" and "+b["weakness"],
        "power_level": a["power_level"]+b["power_level"]
    }
    return creature
breeda=all_creats[int(input("a"))]
print(breeda)
breedb=all_creats[int(input("b"))]
print(breedb)
print("breed: ")
print(breed(breeda,breedb))
