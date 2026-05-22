from monsterdb import al_frm
def nice(x):
    print(x["name"])
    print("Color: " + x["color"])
    print("Ability: " + x["ability"])
    print("Weakness: " + x["weakness"])
    print("Power: " +  str(x["power_level"]))
xa=al_frm[int(input("Smol ID: "))]
ya=al_frm[int(input("Beeg ID: "))]
nice(xa)
print("\nVS\n")
nice(ya)
print(f"..but {xa['name']} can multiply.\n")
x,y=xa['power_level'],ya['power_level'] #xa/ya only available for additional data
xn,yn=xa['name'],ya['name']
num=1
def bonusz(z,w):
    return round((z*w)*((w/10)+0.9),1)
totpowah=x
while totpowah<y:
    totpowah=bonusz(x,num)
    print(f"{xn}: {x} power * {num} copies * {round((num/10)+0.9, 1)} team bonus = {totpowah} total power, vs {yn}: {y} power, power diff: {round(y-totpowah, 1)}")
    num+=1
