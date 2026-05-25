from monsterdb import al_frm 
print(min(al_frm, key=lambda m: m["power_level"]))
