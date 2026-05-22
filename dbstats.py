from monsterdb import al_frm
def nice(x,idk=False):
    print(x["name"] + "'s stats")
    print("Color: " + x["color"])
    print("Ability: " + x["ability"])
    print("Weakness: " + x["weakness"])
    print("Power: " + str(x["power_level"]))
    if idk:
        print("ID: " + str(idk))
def creatselect():
    print("All available creatures/monsters:")
    for i, c in enumerate(al_frm):
        print(i, c["name"])
    try:
        a = int(input(f"Pick A (0-{len(al_frm)-1}): "))
        b = int(input(f"Pick B (0-{len(al_frm)-1}): "))
    except:
        print("Invalid input.")
        return "ERROR"
    return [a,b]
def maxpower(cretair=[],reverse=False):
    e={}
    for i in range(0,len(al_frm)):
        if i not in cretair:
            e[str(i)]=al_frm[i]["power_level"]
    if not reverse:
        return [max(e, key=e.get),max(e.values())]
    else:
        return [min(e, key=e.get),min(e.values())]
ma=maxpower()
#nice(al_frm[int(ma[0])],idk=ma[0])
#for i in range(0,len(al_frm)):
#    nice(al_frm[i],idk=i)
def minpower(cretair=[]):
    e={}
    for i in range(0,len(al_frm)):
        if i not in cretair:
            e[str(i)]=al_frm[i]["power_level"]
    return [min(e, key=e.get),min(e.values())]
#ma=minpower()
poo=3
def top(x,reverse=False):
    shot=[]
    for i in range(1,x+1):
        if i == 1:
            print("\n1ST PLACE:")
            ma=maxpower(reverse=reverse)
        elif i == 2:
            print("\n2ND PLACE:")
            ma=maxpower(cretair=shot,reverse=reverse)
        elif i == 3:
            print("\n3RD PLACE:")
            ma=maxpower(cretair=shot,reverse=reverse)
        else:
            print(f"\n{i}TH PLACE:")
            ma=maxpower(cretair=shot,reverse=reverse)
        nice(al_frm[int(ma[0])],idk=ma[0])
        shot.append(int(ma[0]))
print("TOP 500 POWER:")
top(500)

print("\nTOP 500 LOWEST POWER:")
top(500,reverse=True)

print("\nSPECIAL/RANDOM:")
print("Monsterdb.py stats:")
print(f"Total monsters: {len(al_frm)}")
e={}
for i in range(0,len(al_frm)):
    e[str(i)]=al_frm[i]["power_level"]
totpower=0
totmstr=0
for i in e:
    totpower+=e[i]
    totmstr+=1
print(f"Average power: {totpower/totmstr}")
print(f"Total power across all monsters: {totpower}")
