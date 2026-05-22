import random
from math import log2
from monsterdb import al_frm
def nice(x,idk=None):
    print(x["name"] + "'s stats")
    print("Color: " + x["color"])
    print("Ability: " + x["ability"])
    print("Weakness: " + x["weakness"])
    print("Power: " +  str(x["power_level"]))
    if idk:
        print("ID: "+str(idk))

def battle(a, b, teambonus=None):
    print("=== BATTLE START ===")
    print(f"Team A (Power {a} * {round(teambonus[0]*10)/10} = {int(teambonus[0]*a)})")
    print("VS")
    print(f"Team B (Power {b} * {round(teambonus[1]*10)/10} = {int(teambonus[1]*b)})")
    print("====================")

    base_a = a * teambonus[0]
    base_b = b * teambonus[1]

    # Chaos factor: ±20%
    chaos_a = random.randint(int(-base_a / 5), int(base_a / 5))
    chaos_b = random.randint(int(-base_b / 5), int(base_b / 5))

    final_a = max(1, base_a + chaos_a)
    final_b = max(1, base_b + chaos_b)

    print(f"\nTeam A's final power: {final_a}")
    print(f"Team B's final power: {final_b}\n")

    if final_a > final_b:
        print("🏆 Team A wins the battle!")
        return "a"
    elif final_b > final_a:
        print("🏆 Team B wins the battle!")
        return "b"
    else:
        print("🤝 It's a tie! Everyone collapses from exhaustion.")
        return random.choice(["a", "b"])

# -----------------------------
#  main_battle stays UNTOUCHED
# -----------------------------

def main_battle(ta, tb):
    az = [ta]
    bz = [tb]

    creas_a = [al_frm[i] for i in az]
    creas_b = [al_frm[i] for i in bz]

    print("\nTeam A:")
    for i in range(len(creas_a)):
        #print(i["name"], i["power_level"]) THAT WAS A BIG DOWNGRADE
        nice(creas_a[i],idk=az[i])

    print("\nTeam B:")
    for i in range(len(creas_b)):
        #print(i["name"], i["power_level"])
        nice(creas_b[i],idk=bz[i])

    a_val = sum(i["power_level"] for i in creas_a)
    b_val = sum(i["power_level"] for i in creas_b)

    bonusa = 0.9 + (0.1 * len(az))
    bonusb = 0.9 + (0.1 * len(bz))

    print("\n--- BATTLE RESULT ---\n")
    result = battle(a_val, b_val, teambonus=[bonusa, bonusb])
    return result


# -----------------------------
#  NEW: clean, flexible tournament
# -----------------------------

def is_power_of_two(n):
    return n > 0 and (n & (n - 1)) == 0

def pair_up(ids):
    """Turns [1,2,3,4] into [[1,2],[3,4]]"""
    return [ids[i:i+2] for i in range(0, len(ids), 2)]

def run_round(brackets):
    """Runs one round and returns winners."""
    winners = []
    for a, b in brackets:
        result = main_battle(a, b)
        winners.append(a if result == "a" else b)
    return winners

def tournament(ids):
    """Runs a full tournament until 1 winner remains."""
    if not is_power_of_two(len(ids)):
        print("ERROR: Number of fighters must be a power of 2.")
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
    print(f"Winner ID: {winner}")
    nice(al_frm[winner])
    return winner


# Example:
tournament([1,2,3,4,5,6,7,8,100000,100001,100002,100004,100005,100006,100007,100008])
