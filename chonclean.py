# ============================================
#  CHONKER v2.0_CLEAN (Clean Variable Names)
# ============================================

import random
import os
import shutil
import datetime

class ManuallyInitiatedCrash(Exception):
    pass

# ============================================================
#  SHARED UTILITIES
# ============================================================

def get_db():
    if input("Legacy get_db call detected! [T]hrow error or [P]ass: ").lower() == "t":
        raise ManuallyInitiatedCrash

try:
    from monsterdb import al_frm
    db = list(al_frm)
    needsInit = False
except:
    print("HEYO BRO YE MIGHT WANNA COPY A BACKUP")
    db = []
    needsInit = True

def save(file):
    with open("monsterdb.py", "w", encoding="utf-8") as f:
        f.write("al_frm=" + str(file))
        f.flush()

def nice(mon, showID=None):
    print(mon["name"] + "'s stats")
    print("Color:", mon["color"])
    print("Ability:", mon["ability"])
    print("Weakness:", mon["weakness"])
    print("Power:", mon["power_level"])
    if showID is not None:
        print("ID:", showID)

# ============================================================
# RANDOM TOURNAMENT APIS
# ============================================================

def calctot(team, out="fp", chaos=0.2):
    basePower = sum(c["power_level"] for c in team)
    initPower = basePower

    if out == "tp":
        return basePower

    bonus = 0.9 + 0.1 * len(team)
    bonusPower = basePower * bonus

    if out == "bp":
        return bonusPower

    chaosFactor = (random.random() * 2 * chaos) - chaos + 1
    finalPower = bonusPower * chaosFactor

    if out == "log":
        return {
            "0": finalPower,
            "nerd": [chaosFactor, bonus, bonusPower, initPower]
        }

    return finalPower

def bonusz(z, w):
    return round((z * w) * ((w / 10) + 0.9), 1)

# ============================================================
#  BATTLE SYSTEM
# ============================================================

def battle(powerA, powerB, debugInfo):
    debugA, debugB = debugInfo

    print("=== BATTLE START ===")
    print(f"Team A (Power {debugA[3]} * chaos {round(debugA[0], 2)} = {debugA[2]})")
    print("VS")
    print(f"Team B (Power {debugB[3]} * chaos {round(debugB[0], 2)} = {debugB[2]})")
    print("====================")

    print(f"\nTeam A final power: {powerA}")
    print(f"Team B final power: {powerB}\n")

    if powerA > powerB:
        print("🏆 Team A wins!")
        return "a"
    elif powerB > powerA:
        print("🏆 Team B wins!")
        return "b"
    else:
        print("🤝 Tie! Chaos decides.")
        return random.choice(["a", "b"])

def main_battle(idsA=None, idsB=None):
    print(f"DB loaded with {len(db)} monsters.")

    if not idsA:
        print("Enter IDs for Team A (space-separated):")
        idsA = [int(x) for x in input("> ").split()]

    if not idsB:
        print("Enter IDs for Team B (space-separated):")
        idsB = [int(x) for x in input("> ").split()]

    teamA = [db[i] for i in idsA]
    teamB = [db[i] for i in idsB]

    print("\nTeam A:")
    for mon in teamA:
        nice(mon)

    print("\nTeam B:")
    for mon in teamB:
        nice(mon)

    calcA = calctot(teamA, out="log")
    calcB = calctot(teamB, out="log")

    return battle(calcA["0"], calcB["0"], debugInfo=[calcA["nerd"], calcB["nerd"]])

# ============================================================
#  TOURNAMENT SYSTEM
# ============================================================

def is_power_of_two(n):
    return n > 0 and (n & (n - 1)) == 0

def pair_up(ids):
    return [ids[i:i+2] for i in range(0, len(ids), 2)]

def run_round(brackets):
    winners = []
    for idA, idB in brackets:
        result = main_battle(idsA=[idA], idsB=[idB])
        winners.append(idA if result == "a" else idB)
    return winners

def tournament():
    print(f"DB loaded with {len(db)} monsters.")
    print("Enter fighter IDs (space-separated, power of 2 count):")

    fighters = [int(x) for x in input("> ").split()]

    if not is_power_of_two(len(fighters)):
        print("ERROR: number of fighters must be power of 2")
        return

    roundNum = 1
    while len(fighters) > 1:
        print(f"\n=== ROUND {roundNum} ===")
        fighters = run_round(pair_up(fighters))
        roundNum += 1

    print("\n=== TOURNAMENT WINNER ===")
    winner = fighters[0]
    nice(db[winner], showID=winner)

# ============================================================
#  CREPOWAHTHING
# ============================================================

def crepowahthing():
    print(f"DB loaded with {len(db)} monsters.")

    smol = db[int(input("Smol ID: "))]
    beeg = db[int(input("Beeg ID: "))]

    nice(smol)
    print("\nVS\n")
    nice(beeg)
    print(f"\n…but {smol['name']} can multiply.\n")

    basePower = smol["power_level"]
    targetPower = beeg["power_level"]

    nameA = smol["name"]
    nameB = beeg["name"]

    copies = 1
    totalPower = basePower

    while totalPower < targetPower:
        totalPower = bonusz(basePower, copies)
        print(f"{nameA}: {basePower} power * {copies} copies * "
              f"{round((copies/10)+0.9, 1)} team bonus = {totalPower}, "
              f"vs {nameB}: {targetPower}, diff: {round(targetPower - totalPower, 1)}")
        copies += 1

# ============================================================
#  CLEANER
# ============================================================

def clean_monsterdb():
    print("Enumerating creatures...")
    print(f"{len(db)} found.")

    mode = input("Clean monster file? [Yes/No/Log]: ").lower()
    if mode == "n":
        return

    def clean(mon):
        colors = mon["color"].split("ish ")
        abilities = mon["ability"].split(" and ")
        weaknesses = mon["weakness"].split(" and ")
        return {
            "name": mon["name"],
            "color": random.choice(colors),
            "ability": random.choice(abilities),
            "weakness": random.choice(weaknesses),
            "power_level": mon["power_level"]
        }

    cleanedDB = []
    if mode != "l":
        for mon in db:
            cleanedDB.append(clean(mon))
    else:
        for idx, mon in enumerate(db, start=1):
            cleanedDB.append(clean(mon))
            print(f"Cleaned {idx}/{len(db)}")

    if os.path.exists("monsterdb.py"):
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        shutil.copy("monsterdb.py", f"monsterdb_backup_{timestamp}.py")

    save(cleanedDB)
    print("Saved cleaned monsterdb.py")

# ============================================================
#  DB STATS
# ============================================================

def maxpower(exclude=None, reverse=False):
    if exclude is None:
        exclude = []

    pool = {str(i): db[i]["power_level"] for i in range(len(db)) if i not in exclude}
    key = max(pool, key=pool.get) if not reverse else min(pool, key=pool.get)
    return key, pool[key]

def top(n, reverse=False):
    used = []
    for rank in range(1, n+1):
        place = {1: "1ST", 2: "2ND", 3: "3RD"}.get(rank, f"{rank}TH")
        print(f"\n{place} PLACE:")

        entry = maxpower(used, reverse=reverse)
        nice(db[int(entry[0])], showID=entry[0])
        used.append(int(entry[0]))

def dbstats():
    print("TOP 5 POWER:")
    top(5)

    print("\nTOP 5 LOWEST POWER:")
    top(5, reverse=True)

    print("\nSPECIAL/RANDOM:")
    print("Total monsters:", len(db))

    totalPower = sum(m["power_level"] for m in db)
    print("Average power:", totalPower / len(db))
    print("Total power:", totalPower)

# ============================================================
#  BREEDER
# ============================================================

def breeder():
    global db, needsInit

    if os.path.exists("monsterdb.py"):
        timestamp = datetime.datetime.now().strftime("%S%M%m%d%H%Y")
        shutil.copy("monsterdb.py", f"monsterdb_backup_{timestamp}.py")

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

    def breedraw(monA, monB, config=None):
        nameA, idA = monA["name"].split("-")
        nameB, idB = monB["name"].split("-")

        newName = genbrdrndtxt(nameA, nameB)
        newID = str(int(idA) + int(idB))

        if config and config.get("exists"):
            if config["truncate"]:
                color = random.choice([monA["color"], monB["color"]])
                ability = random.choice([monA["ability"], monB["ability"]])
                weakness = random.choice([monA["weakness"], monB["weakness"]])
            else:
                color = f"{monA['color']}ish {monB['color']}"
                ability = f"{monA['ability']} and {monB['ability']}"
                weakness = f"{monA['weakness']} and {monB['weakness']}"
        else:
            color = f"{monA['color']}ish {monB['color']}"
            ability = f"{monA['ability']} and {monB['ability']}"
            weakness = f"{monA['weakness']} and {monB['weakness']}"

        power = monA["power_level"] + monB["power_level"]

        return {
            "name": newName + "-" + newID,
            "color": color,
            "ability": ability,
            "weakness": weakness,
            "power_level": power
        }

    if needsInit:
        creatures = [make_creature() for _ in range(5)]
        monsters = [make_monster() for _ in range(5)]
        db = creatures + monsters
        needsInit = False

    print("All creatures:")
    for i, mon in enumerate(db):
        print(i, mon)

    config = {"truncate": False, "exists": True}

    def parsechc(code):
        nonlocal config
        if code in ("autobreed", "chaos"):
            breedCount = int(input("How many breeds? (WILL NOT SAVE IF INTERRUPTED): "))
            for i in range(breedCount):
                print(i)
                newMon = breedraw(random.choice(db), random.choice(db), config)
                db.append(newMon)
                print("New breed:", newMon)
            return 1
        if code == "truncate":
            config["truncate"] = True
            return 5
        if code == "exit":
            return 3
        return 1

    idA = input(f"Pick A (0-{len(db)-1}): ").lower()

    if idA == "supersecretpassword123123123":
        print("You found an easteregg!")
        cheatState = 5
        while cheatState == 5:
            cheatState = parsechc(input("Enter cheat code: "))
        if cheatState == 1:
            save(db)
            print("Saved and exiting breeder.")
            return
        if cheatState == 3:
            idA = input(f"Pick A (0-{len(db)-1}): ").lower()

    idB = input(f"Pick B (0-{len(db)-1}): ").lower()

    offspring = breedraw(db[int(idA)], db[int(idB)], config)
    print("\nBreeding result (Raw):\n", offspring)
    print("\nBreeding result (Fancy):\n")
    nice(offspring)

    db.append(offspring)
    save(db)
    print("Saved new monsterdb.py")

# ============================================================
#  MAIN MENU
# ============================================================

def main():
    while True:
        print("=== CHONKER V2 CLEAN VARS ===")
        if len(db) > 10000:
            print("just like ur db")

        print("1. Battle")
        print("2. Tournament")
        print("3. Power Scaling (crepowahthing)")
        print("4. Clean monsterdb")
        print("5. Database stats")
        print("6. Breeder")
        print("7. Exit")

        try:
            choice = input("> ").strip()
        except KeyboardInterrupt:
            print("\nSaving...")
            save(db)
            raise ManuallyInitiatedCrash("Ctrl‑C has been pressed.")

        try:
            if choice == "1":
                main_battle()
            elif choice == "2":
                tournament()
            elif choice == "3":
                crepowahthing()
            elif choice == "4":
                clean_monsterdb()
            elif choice == "5":
                dbstats()
            elif choice == "6":
                breeder()
            elif choice == "7":
                break
            else:
                print("Invalid choice.")
        except KeyboardInterrupt:
            print("\nSaving...")
            save(db)
            raise ManuallyInitiatedCrash("Ctrl‑C has been pressed.")

if __name__ == "__main__":
    main()

