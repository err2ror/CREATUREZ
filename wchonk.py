# CHONKER v3.2 – CREATUREZ+ (fixed rarity system)
import random
import os
import shutil
import datetime

class ManuallyInitiatedCrash(Exception):
    pass

# ============================
#  SHARED UTILITIES
# ============================

def get_db():
    if input("Legacy get_db call detected! [T]hrow error or [P]ass").lower() == "t":
        raise ManuallyInitiatedCrash

try:
    from monsterdb import al_frm
    db = al_frm
    needsinit = False
except:
    print("HEYO BRO YE MIGHT WANNA COPY A BACKUP")
    db = []
    needsinit = True

def save(file):
    azertyuiop = "al_frm=" + str(file)
    monstardb = open("monsterdb.py", "w", encoding="utf-8")
    monstardb.write(azertyuiop)
    monstardb.flush()

def nice(x, show_id=None):
    print(x["name"])
    print("Color:", x["color"])
    print("Ability:", x["ability"])
    print("Weakness:", x["weakness"])
    print("Power:", x["power_level"])
    if "rarity" in x:
        print("Rarity:", x["rarity"])
    if show_id is not None:
        print("ID:", show_id)

# ============================
#  RARITY SYSTEM (THRESHOLDS)
# ============================

k = 1000
m = k**2
b = m * k

# name -> power threshold (strictly less than)
RARITY_THRESHOLDS = [
    ("bruh", 2000),
    ("super common", 10000),
    ("very common", 50000),
    ("common", 75000),
    ("not that common", 99999),
    ("uncommon", 200 * k),
    ("cool", 300 * k),
    ("slightly rare", 400 * k),
    ("kinda rare", 500 * k),
    ("rare", m),
    ("very rare", 5 * m),
    ("extremely rare", 10 * m),
    ("super omega giga super 69 rare", 50 * m),
    ("mehpic", 55 * m),
    ("not very epic", 60 * m),
    ("epic", 100 * m),
    ("very epic", 200 * m),
    ("super epic", 300 * m),
    ("uncanny", 500 * m),
    ("legendary", 600 * m),
    ("heroical", 700 * m),
    ("mythical", 2 * b),
    ("godly", 5 * b),
    ("wtf", 10 * b)
]

# for quick lookup of order
RARITY_INDEX = {name: i for i, (name, _) in enumerate(RARITY_THRESHOLDS)}

def get_rarity(power):
    for name, threshold in RARITY_THRESHOLDS:
        if power < threshold:
            return name
    return "wtf"

# ============================
# TEAM SYNERGY / POWER HELPERS
# ============================

def compute_team_bonus(team):
    """
    Synergy 2.0:
    - base bonus: 0.9 + 0.1 * team size (old behavior)
    - +5% if all same color
    - +rarity_bonus based on average rarity index / 100
    """
    if not team:
        return 1.0

    bonus = 0.9 + 0.1 * len(team)

    colors = {c["color"] for c in team}
    if len(colors) == 1:
        bonus *= 1.05  # +5%

    rarity_indices = []
    for c in team:
        r = c.get("rarity")
        if r in RARITY_INDEX:
            rarity_indices.append(RARITY_INDEX[r])
    if rarity_indices:
        avg_rarity = sum(rarity_indices) / len(rarity_indices)
        rarity_bonus = 1.0 + (avg_rarity / 100.0)
        bonus *= rarity_bonus

    return bonus

# ============================
# RANDOM TOURNAMENT APIS
# ============================

def calctot(team, out="fp", chaos=0.2):
    val = sum(c["power_level"] for c in team)
    if out == "tp":
        return val
    initval = val

    bonus = compute_team_bonus(team)

    val = val * bonus
    if out == "bp":
        return val
    savval = val
    chaosf = random.random() * 2 * chaos
    chaosf -= chaos
    chaosf += 1
    val = val * chaosf
    if out == "log":
        return {
            "0": val,
            "nerd": [chaosf, bonus, savval, initval]
        }
    else:
        return val

def bonusz(z, w):
    return round((z * w) * ((w / 10) + 0.9), 1)

# ============================
#  BATTLE SYSTEM
# ============================

def battle(a, b, randomdebug: list):
    rdba = randomdebug[0]
    rdbb = randomdebug[1]
    if not randomdebug:
        raise Exception("no chaos :(")
    print("=== BATTLE START ===")
    print(f"Team A (Power {rdba[3]} * {round(rdba[0], 1)} = {rdba[2]})")
    print("VS")
    print(f"Team B (Power {rdbb[3]} * {round(rdbb[0], 1)} = {rdbb[2]})")
    print("====================")

    print(f"\nTeam A final power: {a}")
    print(f"Team B final power: {b}\n")

    if a > b:
        print("🏆 Team A wins!")
        return "a"
    elif b > a:
        print("🏆 Team B wins!")
        return "b"
    else:
        print("🤝 Tie! Chaos decides.")
        return random.choice(["a", "b"])

def main_battle(ids_a=None, ids_b=None):
    print(f"DB loaded with {len(db)} monsters.")
    if not ids_a:
        print("Enter IDs for Team A (space-separated):")
        ids_a = [int(x) for x in input("> ").split()]
    if not ids_b:
        print("Enter IDs for Team B (space-separated):")
        ids_b = [int(x) for x in input("> ").split()]

    team_a = [db[i] for i in ids_a]
    team_b = [db[i] for i in ids_b]

    print("\nTeam A:")
    for c in team_a:
        nice(c)

    print("\nTeam B:")
    for c in team_b:
        nice(c)

    a_full = calctot(team_a, out="log")
    a_val = a_full["0"]
    b_full = calctot(team_b, out="log")
    b_val = b_full["0"]
    a_nerd = a_full["nerd"]
    b_nerd = b_full["nerd"]

    return battle(a_val, b_val, randomdebug=[a_nerd, b_nerd])

# ============================
#  TOURNAMENT SYSTEM
# ============================

def is_power_of_two(n):
    return n > 0 and (n & (n - 1)) == 0

def pair_up(ids):
    return [ids[i:i+2] for i in range(0, len(ids), 2)]

def run_round(brackets, db):
    winners = []
    for a, b in brackets:
        team_a = [a]
        team_b = [b]
        result = main_battle(ids_a=team_a, ids_b=team_b)
        winners.append(a if result == "a" else b)
    return winners

def tournament():
    print(f"DB loaded with {len(db)} monsters.")
    print("Enter fighter IDs (space-separated, power of 2 count):")
    fighters = [int(x) for x in input("> ").split()]

    if not is_power_of_two(len(fighters)):
        print("ERROR: number of fighters must be power of 2")
        return

    round_num = 1
    while len(fighters) > 1:
        print(f"\n=== ROUND {round_num} ===")
        brackets = pair_up(fighters)
        fighters = run_round(brackets, db)
        round_num += 1

    print("\n=== TOURNAMENT WINNER ===")
    winner = fighters[0]
    nice(db[winner], show_id=winner)

# ============================
#  CREPOWAHTHING (POWER SCALER)
# ============================

def crepowahthing():
    print(f"DB loaded with {len(db)} monsters.")
    xa = db[int(input("Smol ID: "))]
    ya = db[int(input("Beeg ID: "))]

    nice(xa)
    print("\nVS\n")
    nice(ya)
    print(f"\n…but {xa['name']} can multiply.\n")

    x = xa["power_level"]
    y = ya["power_level"]
    xn = xa["name"]
    yn = ya["name"]

    num = 1
    totpowah = x

    while totpowah < y:
        totpowah = bonusz(x, num)
        print(f"{xn}: {x} power * {num} copies * {round((num/10)+0.9, 1)} team bonus = "
              f"{totpowah} total power, vs {yn}: {y} power, power diff: {round(y - totpowah, 1)}")
        num += 1

# ============================
#  CLEANER
# ============================

def clean_monsterdb():
    from random import choice as coits
    print("Enumerating creatures...")
    print(f"{len(db)} found.")

    mode = input("Clean monster file? [Yes/No/Log]: ").lower()
    if mode == "n":
        return

    end = []

    def clean(i):
        colors = i["color"].split("ish ")
        abilities = i["ability"].split(" and ")
        weaknesses = i["weakness"].split(" and ")
        return {
            "name": i["name"],
            "color": coits(colors),
            "ability": coits(abilities),
            "weakness": coits(weaknesses),
            "power_level": i["power_level"],
            "rarity": i.get("rarity", get_rarity(i["power_level"])),
            "traits": i.get("traits", []),
            "version": i.get("version", 3)
        }

    if mode != "l":
        for i in db:
            end.append(clean(i))
    else:
        count = 1
        for i in db:
            end.append(clean(i))
            print(f"Cleaned {count}/{len(db)}")
            count += 1

    if os.path.exists("monsterdb.py"):
        ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        shutil.copy("monsterdb.py", f"monsterdb_backup_{ts}.py")

    save(end)
    print("Saved cleaned monsterdb.py")

# ============================
#  DB STATS
# ============================

def maxpower(exclude=None, reverse=False):
    if exclude is None:
        exclude = []
    exclude = set(exclude)
    pool = [(i, m) for i, m in enumerate(db) if i not in exclude]
    if not reverse:
        idx, mon = max(pool, key=lambda x: x[1]["power_level"])
    else:
        idx, mon = min(pool, key=lambda x: x[1]["power_level"])
    return idx, mon

def faxtpower(exclude=None, reverse=False):
    if exclude is None:
        exclude = []
    exclude = set(exclude)

    pool = db[:]
    idmap = list(range(len(db)))
    pos_of = list(range(len(db)))

    for orig_id in exclude:
        pos = pos_of[orig_id]
        last = len(pool) - 1

        if pos != last:
            pool[pos], pool[last] = pool[last], pool[pos]
            idmap[pos], idmap[last] = idmap[last], idmap[pos]
            pos_of[idmap[pos]] = pos
            pos_of[idmap[last]] = last

        del pool[last]
        del idmap[last]

    if not reverse:
        pos = max(range(len(pool)), key=lambda i: pool[i]["power_level"])
    else:
        pos = min(range(len(pool)), key=lambda i: pool[i]["power_level"])

    orig_id = idmap[pos]
    return orig_id, pool[pos]

def top_legacy(x, reverse=False):
    used = []
    for i in range(1, x+1):
        if i == 1:
            place = "1ST"
        elif i == 2:
            place = "2ND"
        elif i == 3:
            place = "3RD"
        else:
            place = f"{i}TH"
        print(f"\n{place} PLACE:")
        mid = maxpower(exclude=used, reverse=reverse)
        nice(db[int(mid[0])], show_id=mid[0])
        used.append(int(mid[0]))

def top(x, reverse=False):
    used = []
    for i in range(1, x+1):
        if i == 1:
            place = "1ST"
        elif i == 2:
            place = "2ND"
        elif i == 3:
            place = "3RD"
        else:
            place = f"{i}TH"
        print(f"\n{place} PLACE:")
        mid = faxtpower(exclude=sorted(set(used), reverse=True), reverse=reverse)
        used.append(mid[0])
        nice(db[mid[0]], show_id=mid[0])

def top_maxpow(x, reverse=False):
    used = []
    for i in range(1, x+1):
        if i == 1:
            place = "1ST"
        elif i == 2:
            place = "2ND"
        elif i == 3:
            place = "3RD"
        else:
            place = f"{i}TH"
        print(f"\n{place} PLACE:")
        mid = maxpower(exclude=sorted(set(used), reverse=True), reverse=reverse)
        used.append(mid[0])
        nice(db[mid[0]], show_id=mid[0])

def dbstats(numtop=5):
    print("TOP 5 POWER:")
    top(numtop)

    print("\nTOP 5 LOWEST POWER:")
    top(numtop, reverse=True)

    print("\nSPECIAL/RANDOM:")
    print("Total monsters:", len(db))

    totpower = sum(m["power_level"] for m in db)
    print("Average power:", totpower / len(db))
    print("Total power:", totpower)

# ============================
#  MONSTER UPGRADER
# ============================

def upgrade_monsters(iamasecretargumentshutup=False):
    print("=== MONSTER UPGRADER ===")
    print(f"Upgrading {len(db)} monsters...")
    for m in db:
        if "rarity" not in m or iamasecretargumentshutup:
            m["rarity"] = get_rarity(m["power_level"])
        if "traits" not in m or iamasecretargumentshutup:
            m["traits"] = []
        if "version" not in m or iamasecretargumentshutup:
            m["version"] = 3
    save(db)
    print("Upgrade complete! All monsters now have rarity + traits + version.")

# ============================
#  BREEDER
# ============================

def breeder():
    if os.path.exists("monsterdb.py"):
        ts = datetime.datetime.now().strftime("%S%M%m%d%H%Y")
        shutil.copy("monsterdb.py", f"monsterdb_backup.py_{ts}")

    monstardb = open("monsterdb.py", "w", encoding="utf-8")

    def make_creature():
        species = ["Blob", "Gorf", "Zibble", "Snorf", "Wumpus", "Glip"]
        colors = ["red", "blue", "green", "purple", "neon yellow", "transparent"]
        abilities = ["teleports badly", "screams politely", "eats electricity", "vibrates", "floats sometimes", "knows your secrets"]
        weaknesses = ["water", "math", "loud noises", "Mondays", "gravity", "social interaction"]
        power = random.randint(1, 9000)
        return {
            "name": random.choice(species) + "-" + str(random.randint(100, 999)),
            "color": random.choice(colors),
            "ability": random.choice(abilities),
            "weakness": random.choice(weaknesses),
            "power_level": power,
            "rarity": get_rarity(power),
            "traits": [],
            "version": 3
        }

    def make_monster():
        species = ["Blug", "Gorfo", "Zibbler", "Snooor", "Wumpo", "Glop"]
        colors = ["red", "blue", "green", "purple", "neon yellow", "raimbow", "transparent"]
        abilities = ["teleports", "screams", "eats electricity", "vibrates", "floats sometimes", "knows your secrets"]
        weaknesses = ["fire", "english", "absence of noises", "Sundays", "space", "loneliness"]
        power = random.randint(1000, 90000)
        return {
            "name": random.choice(species) + "-" + str(random.randint(1000, 9999)),
            "color": random.choice(colors),
            "ability": random.choice(abilities),
            "weakness": random.choice(weaknesses),
            "power_level": power,
            "rarity": get_rarity(power),
            "traits": [],
            "version": 3
        }

    def genbrdrndtxt(x, y):
        return "".join(random.choice([a, b]) for a, b in zip(x, y))

    def breedraw(a, b, secretconfig=None):
        nameA, idA = a["name"].split("-")
        nameB, idB = b["name"].split("-")

        new_name = genbrdrndtxt(nameA, nameB)
        new_id = str(int(idA) + int(idB))

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
        rarity = get_rarity(power_level)

        return {
            "name": new_name + "-" + new_id,
            "color": color,
            "ability": ability,
            "weakness": weakness,
            "power_level": power_level,
            "rarity": rarity,
            "traits": [],
            "version": 3
        }

    global db
    if needsinit:
        creatures = [make_creature() for _ in range(5)]
        monsters = [make_monster() for _ in range(5)]
        db = creatures + monsters
    print("All creatures:")
    for i, c in enumerate(db):
        print(i, c)

    config = {
        "truncate": False,
        "exists": True
    }

    def parsechc(ab):
        nonlocal config
        if ab in ("autobreed", "chaos"):
            maxtimes = int(input("How many breeds do you want? [WILL NOT SAVE IF YOU TERMINATE BEFORE END]: "))
            print(maxtimes)
            for i in range(maxtimes):
                print(i)
                new = breedraw(random.choice(db), random.choice(db), secretconfig=config)
                db.append(new)
                print("New breed:")
                print(new)
            return 1
        if ab == "truncate":
            config["truncate"] = True
            return 5
        if ab == "exit":
            return 3
        return 1

    a = input(f"Pick A (0-{len(db)-1}): ").lower()

    if a == "supersecretpassword123123123":
        print("You found an easteregg!")
        x = 5
        while x == 5:
            x = parsechc(input("You can enter a cheat code!: "))
        if x == 1:
            save(db)
            print("Saved and exiting breeder.")
            return
        if x == 3:
            a = input(f"Pick A (0-{len(db)-1}): ").lower()

    b = input(f"Pick B (0-{len(db)-1}): ").lower()

    final = breedraw(db[int(a)], db[int(b)], secretconfig=config)
    print("\nBreeding result (Raw):\n")
    print(final)
    print("\nBreeding result (Fancy):\n")
    nice(final)
    db.append(final)
    save(db)
    print("Saved new monsterdb.py")

# ============================
#  MAIN MENU
# ============================

def main():
    while True:
        print("=== CHONKER V3.2 – CREATUREZ+ ===")
        if len(db) > 10000:
            print("just like ur db")
        print("1. Battle")
        print("2. Tournament")
        print("3. Power Scaling (crepowahthing)")
        print("4. Clean monsterdb")
        print("5. Database stats")
        print("6. Breeder")
        print("7. Stat viewer")
        print("8. Upgrade old monsters")
        print("9. Exit")
        try:
            choice = input("> ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nSaving...")
            save(db)
            raise ManuallyInitiatedCrash("Ctrl-C or Ctrl-D has been pressed.")

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
                x = input("View stats of (ID) [X: exit]: ")
                while True:
                    if x.lower() == "x":
                        break
                    nice(db[int(x)])
                    x = input("View stats of (ID) [X: exit]: ")
            elif choice == "8":
                upgrade_monsters()
            elif choice == "9":
                break
            else:
                print("Invalid choice.")
        except (KeyboardInterrupt, EOFError):
            print("\nSaving...")
            save(db)
            raise ManuallyInitiatedCrash("Ctrl-C or Ctrl-D has been pressed.")

if __name__ == "__main__":
    main()

