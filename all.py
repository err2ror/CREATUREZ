# ============================
#  MONSTER MEGASCRIPT v1-0
#  battle + tournament + crepowahthing + cleaner + dbstats
# ============================

import random
from monsterdb import al_frm

# ============================
#  SHARED UTILITIES
# ============================

def nice(x, show_id=None):
    print(x["name"] + "'s stats")
    print("Color:", x["color"])
    print("Ability:", x["ability"])
    print("Weakness:", x["weakness"])
    print("Power:", x["power_level"])
    if show_id is not None:
        print("ID:", show_id)

# ============================
#  BATTLE SYSTEM
# ============================

def battle(a, b, teambonus=None):
    print("=== BATTLE START ===")
    print(f"Team A (Power {a} * {round(teambonus[0]*10)/10} = {int(teambonus[0]*a)})")
    print("VS")
    print(f"Team B (Power {b} * {round(teambonus[1]*10)/10} = {int(teambonus[1]*b)})")
    print("====================")

    base_a = a * teambonus[0]
    base_b = b * teambonus[1]

    chaos_a = random.randint(int(-base_a / 5), int(base_a / 5))
    chaos_b = random.randint(int(-base_b / 5), int(base_b / 5))

    final_a = max(1, base_a + chaos_a)
    final_b = max(1, base_b + chaos_b)

    print(f"\nTeam A final power: {final_a}")
    print(f"Team B final power: {final_b}\n")

    if final_a > final_b:
        print("🏆 Team A wins!")
        return "a"
    elif final_b > final_a:
        print("🏆 Team B wins!")
        return "b"
    else:
        print("🤝 Tie! Chaos decides.")
        return random.choice(["a", "b"])

def main_battle(ids_a, ids_b):
    team_a = [al_frm[i] for i in ids_a]
    team_b = [al_frm[i] for i in ids_b]

    print("\nTeam A:")
    for c in team_a:
        nice(c)

    print("\nTeam B:")
    for c in team_b:
        nice(c)

    a_val = sum(c["power_level"] for c in team_a)
    b_val = sum(c["power_level"] for c in team_b)

    bonusa = 0.9 + 0.1 * len(ids_a)
    bonusb = 0.9 + 0.1 * len(ids_b)

    print("\n--- BATTLE RESULT ---\n")
    return battle(a_val, b_val, [bonusa, bonusb])

# ============================
#  TOURNAMENT SYSTEM
# ============================

def is_power_of_two(n):
    return n > 0 and (n & (n - 1)) == 0

def pair_up(ids):
    return [ids[i:i+2] for i in range(0, len(ids), 2)]

def run_round(brackets):
    winners = []
    for a, b in brackets:
        result = main_battle([a], [b])
        winners.append(a if result == "a" else b)
    return winners

def tournament(ids):
    if not is_power_of_two(len(ids)):
        print("ERROR: number of fighters must be power of 2")
        return

    round_num = 1
    fighters = ids[:]

    while len(fighters) > 1:
        print(f"\n=== ROUND {round_num} ===")
        brackets = pair_up(fighters)
        fighters = run_round(brackets)
        round_num += 1

    print("\n=== TOURNAMENT WINNER ===")
    winner = fighters[0]
    nice(al_frm[winner], show_id=winner)
    return winner

# ============================
#  CREPOWAHTHING (POWER SCALER)
# ============================

def crepowahthing():
    xa = al_frm[int(input("Smol ID: "))]
    ya = al_frm[int(input("Beeg ID: "))]

    nice(xa)
    print("\nVS\n")
    nice(ya)
    print(f"\n…but {xa['name']} can multiply.\n")

    x = xa["power_level"]
    y = ya["power_level"]
    xn = xa["name"]
    yn = ya["name"]

    num = 1

    def bonusz(z, w):
        return round((z * w) * ((w / 10) + 0.9), 1)

    totpowah = x

    while totpowah < y:
        totpowah = bonusz(x, num)
        print(f"{xn}: {x} power * {num} copies * {round((num/10)+0.9, 1)} team bonus = "
              f"{totpowah} total power, vs {yn}: {y}, diff: {round(y - totpowah, 1)}")
        num += 1

# ============================
#  CLEANER
# ============================

def clean_monsterdb():
    from random import choice as coits
    mstrs = al_frm
    monstardb = open("monsterdb.py", "w")

    def clean(i):
        colors = i["color"].split("ish ")
        abilities = i["ability"].split(" and ")
        weaknesses = i["weakness"].split(" and ")
        return {
            "name": i["name"],
            "color": coits(colors),
            "ability": coits(abilities),
            "weakness": coits(weaknesses),
            "power_level": i["power_level"]
        }

    print("Enumerating creatures...")
    print(f"{len(mstrs)} found.")

    mode = input("Clean monster file? [Yes/No/Log]: ").lower()
    if mode == "n":
        return

    end = []
    if mode != "l":
        for i in mstrs:
            end.append(clean(i))
    else:
        count = 1
        for i in mstrs:
            end.append(clean(i))
            print(f"Cleaned {count}/{len(mstrs)}")
            count += 1

    monstardb.write("al_frm=" + str(end))
    print("Done.")

# ============================
#  DB STATS
# ============================

def dbstats():
    print("TOP 5 POWER:")
    top(5)

    print("\nTOP 5 LOWEST POWER:")
    top(5, reverse=True)

    print("\nSPECIAL/RANDOM:")
    print("Total monsters:", len(al_frm))

    totpower = sum(m["power_level"] for m in al_frm)
    print("Average power:", totpower / len(al_frm))
    print("Total power:", totpower)

def maxpower(exclude=[], reverse=False):
    pool = {i: al_frm[i]["power_level"] for i in range(len(al_frm)) if i not in exclude}
    if not reverse:
        return max(pool, key=pool.get), max(pool.values())
    else:
        return min(pool, key=pool.get), min(pool.values())

def top(x, reverse=False):
    used = []
    for i in range(1, x+1):
        place = f"{i}ST" if i == 1 else f"{i}ND" if i == 2 else f"{i}RD" if i == 3 else f"{i}TH"
        print(f"\n{place} PLACE:")
        mid = maxpower(used, reverse=reverse)
        nice(al_frm[int(mid[0])], show_id=mid[0])
        used.append(int(mid[0]))

# ============================
#  MAIN MENU
# ============================

def main():
    while True:
        print("\n=== MONSTER MEGASCRIPT ===")
        print("1. Battle")
        print("2. Tournament")
        print("3. Power Scaling (crepowahthing)")
        print("4. Clean monsterdb")
        print("5. Database stats")
        print("6. Exit")

        choice = input("> ")

        if choice == "1":
            a = int(input("Fighter A ID: "))
            b = int(input("Fighter B ID: "))
            main_battle([a], [b])

        elif choice == "2":
            ids = input("Enter IDs separated by spaces: ")
            ids = [int(x) for x in ids.split()]
            tournament(ids)

        elif choice == "3":
            crepowahthing()

        elif choice == "4":
            clean_monsterdb()

        elif choice == "5":
            dbstats()

        elif choice == "6":
            break

        else:
            print("Invalid.")

main()

