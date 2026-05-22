import random

# Try loading the saved monster database
try:
    from monsterdb import al_frm
except:
    print("monsterdb.py not found or invalid.")
    print("Make sure your breeder script has run at least once.")
    exit()

def nice(x):
    print(x["name"] + "'s stats")
    print("Color: " + x["color"])
    print("Ability: " + x["ability"])
    print("Weakness: " + x["weakness"])
    print("Power: " + str(x["power_level"]))

def battle(a, b):
    print("=== BATTLE START ===")
    print(f"{a['name']} (Power {a['power_level']})")
    print("VS")
    print(f"{b['name']} (Power {b['power_level']})")
    print("====================")

    base_a = a["power_level"]
    base_b = b["power_level"]

    # Chaos factor: ±20%
    chaos_a = random.randint(-base_a // 5, base_a // 5)
    chaos_b = random.randint(-base_b // 5, base_b // 5)

    final_a = max(1, base_a + chaos_a)
    final_b = max(1, base_b + chaos_b)

    print(f"\n{a['name']} final power: {final_a}")
    print(f"{b['name']} final power: {final_b}\n")

    if final_a > final_b:
        print(f"🏆 {a['name']} wins the battle!")
        return a
    elif final_b > final_a:
        print(f"🏆 {b['name']} wins the battle!")
        return b
    else:
        print("🤝 It's a tie! Both collapse from exhaustion.")
        return None

# Main loop
print("All available creatures/monsters:")
for i, c in enumerate(al_frm):
    print(i, c["name"], "(Power:", c["power_level"], ")")

try:
    a = int(input(f"Pick fighter A (0-{len(al_frm)-1}): "))
    b = int(input(f"Pick fighter B (0-{len(al_frm)-1}): "))
except:
    print("Invalid input.")
    exit()

crea_a = al_frm[a]
crea_b = al_frm[b]

print("\nFighter A:")
nice(crea_a)
print("\nFighter B:")
nice(crea_b)

print("\n--- BATTLE RESULT ---\n")
battle(crea_a, crea_b)

