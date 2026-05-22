sample={
        "name": "test-111",
        "color": "idk m8",
        "ability": "something",
        "weakness": "sunshine and raimbows",
        "power_level": -1
}
def nice(x):
    print(x["name"] + "'s stats")
    print("Color: " + x["color"])
    print("Ability: " + x["ability"])
    print("Weakness: " + x["weakness"])
    print("Power: " +  str(x["power_level"]))
if __name__ == "__main__":
    nice(sample)
