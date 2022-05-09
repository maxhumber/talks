import random

def flip_coin():
    face = random.choice(["Heads", "Tails"])
    return face

def write_coin():
    face = flip_coin()
    with open("/Users/max/Repos/HDD/coins.txt", "a") as f:
        f.write(f"{face}\n")

if __name__ == "__main__":
    write_coin()
