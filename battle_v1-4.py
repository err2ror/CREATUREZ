import random

def battle(crea_a, crea_b):
    print("=== BATTLE START ===")
    print(f"{crea_a['name']} (Power {crea_a['power_level']})")
    print(f"VS")
    print(f"{crea_b['name']} (Power {crea_b['power_level']})")
    print("====================")

    # base stats
    power_a = crea_a["power_level"]
    power_b = crea_b["power_level"]

    # randomness factor (chaos)
    chaos_a = random.randint(-power_a // 5, power_a // 5)
    chaos_b = random.randint(-power_b // 5, power_b // 5)

    final_a = max(1, power_a + chaos_a)
    final_b = max(1, power_b + chaos_b)

    print(f"\n{crea_a['name']} final power: {final_a}")
    print(f"{crea_b['name']} final power: {final_b}\n")

    # winner logic
    if final_a > final_b:
        print(f"🏆 {crea_a['name']} wins the battle!")
        return crea_a
    elif final_b > final_a:
        print(f"🏆 {crea_b['name']} wins the battle!")
        return crea_b
    else:
        print("🤝 It's a tie! Both collapse from exhaustion.")
        return None

def quick_battle():
    """Small helper for manual testing."""
    a = {
        "name": "TestA-123",
        "power_level": 5000,
        "color": "red",
        "ability": "vibrates",
        "weakness": "math"
    }
    b = {
        "name": "TestB-999",
        "power_level": 7000,
        "color": "blue",
        "ability": "floats sometimes",
        "weakness": "gravity"
    }
    battle(a, b)

if __name__ == "__main__":
    quick_battle()

