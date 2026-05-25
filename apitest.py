from basiclog import log
from anchonkiboy import nice, maxpower
print("Loading db...")
from monsterdb import al_frm as db
def top(x,reverse=False):
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
        #print(mid)
        #log(f"{place} place done.")
        #log(f"NERD: {mid}")
        #log(f"NERD: {used}")
        nice(db[mid[0]], show_id=mid[0])

        #used.append(int(mid[0]))
print("STRESS TEST")
print("TOP 1000 HIGHEST POWER")
top(1000)
print("TOP 1000 LOWEST POWER")
top(1000, reverse=True)
