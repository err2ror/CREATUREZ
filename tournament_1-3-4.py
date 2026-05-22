import random
from time import sleep
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
        print(f"🏆 Team A wins the battle!")
        return "a"
    elif final_b > final_a:
        print(f"🏆 Team B wins the battle!")
        return "b"
    else:
        print("🤝 It's a tie! Everyone collapse from exhaustion.")
        return random.choice(["a","b"])



# Main loop
#print("All available creatures/monsters:")
#for i, c in enumerate(al_frm):
#    print(i, c["name"], "(Power:", c["power_level"], ")")
#ta and tb are ids
def main_battle(ta,tb):
    az=[ta]
    bz=[tb]
    '''
    a = input(f"Pick fighter A (0-{len(al_frm)-1}) (Add the word team to team with another fighter): ")
    az = []
    sani=a.replace("team","").strip(" ")
    az.append(int(sani))
    while "team" in a:
        a = input(f"Pick fighter A (0-{len(al_frm)-1}) (Add the word team to team with another fighter): ")
    sani=a.replace("team","").strip(" ")
    az.append(int(sani))
    b = input(f"Pick fighter B (0-{len(al_frm)-1}) (Add the word team to team with another fighter): ")
    bz = []
    sani=b.replace("team","").strip(" ")
    bz.append(int(sani))
    while "team" in b:
    b = input(f"Pick fighter B (0-{len(al_frm)-1}) (Add the word team to team with another fighter): ")
    sani=b.replace("team","").strip(" ")
    bz.append(int(sani))'''
    creas_a = []
    creas_b = []
    for i in az:
        creas_a.append(al_frm[i])
    for i in bz:
        creas_b.append(al_frm[i])
    print("\nTeam A:")
    for i in creas_a:
        nice(i)
    print("\nTeam B:")
    for i in creas_b:
        nice(i)
    a_val=0
    for i in creas_a:
        a_val+=i["power_level"]
    b_val=0
    for i in creas_b:
        b_val+=i["power_level"]
    bonusa=0.9+(0.1*len(az))
    bonusb=0.9+(0.1*len(bz))
    print("\n--- BATTLE RESULT ---\n")
    ab=battle(a_val, b_val, teambonus=[bonusa,bonusb])
    if ab:
        return ab
from math import log2
def tournament(ids):
    if log2(len(ids)) != int(log2(len(ids))):
        exit("ERROR: lazy") #this doesnt mean we keep it this way forever
    tourn_len=int(log2(len(ids)))
    for aaa in range(tourn_len):
        brackets=[]
        g=[]
        for i in range(len(ids)):
            if i%2==0:
                if g:
                    brackets.append(g)
                g=[ids[i]]
            if i%2 == 1:
                g.append(ids[i])
        brackets.append(g)
        outs=[]
        for i in brackets:
            out=main_battle(i[0],i[1])
            if out == "a":
                outs.append(1)
            else:
                outs.append(0)
        ids=[]
        for i in range(len(outs)):
            cb=brackets[i]
            ids.append(cb[outs[i]])
tournament([1,2,3,4,5,6,7,8])

#CHANGELOG
#Initial release of tournament.py
#Added tournament function
#maybe some other things that im too lazy to list
#TO-DO
#add gui/cli/ui
