from math import pi
from random import random

COIN_PROBABILITIES = [
    ("copper", 0.2),
    ("silver", 0.3),
    ("gem", 0.01),
    ("gold", 1)
]

COIN_VALUES = {
    "copper": 0.01,
    "silver": 0.1,
    "gold": 1,
    "gem": 10
}

target_amount = round(500000 * (1 + random() * 0.10), 2)

print("Generating hoard equivalent to {} gp".format(target_amount))

hoard = {
    "copper": 0,
    "silver": 0,
    "gold": 0,
    "gem": 0
}


def hoard_total(hoard):
    total = 0
    for coin, amount in hoard.items():
        total += COIN_VALUES[coin] * amount
    return total


while hoard_total(hoard) < target_amount:
    for coin, p in COIN_PROBABILITIES:
        if random() <= p:
            hoard[coin] += 1

for coin, amount in hoard.items():
    print("* {:,} {} pieces".format(amount, coin))
print("\nTotal value: {:,} gp".format(hoard_total(hoard)))

total_coins = sum(hoard.values())
print("Total 'coins': {:,}".format(total_coins))
total_weight = total_coins / 50
print("Total weight: {} pounds".format(total_weight))
coin_volume = 0.6025**2 * pi * 0.085
packing_density = 0.7
total_volume = coin_volume * total_coins / packing_density
print("Total volume: {:,} in^3".format(round(total_volume, 2)))
