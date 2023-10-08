import random
from math import pi, log10, ceil

COIN_VALUES = {
    "copper": 0.01,
    "silver": 0.1,
    "gold": 1,
    "platinum": 10,
}


def main():
    # target_amount = round(5000 * (1 + random.random() * 0.10), 2)
    target_amount = 120000
    # target_amount = 237.49 - (30 * 4) - (3 * 4)

    print("Generating hoard equivalent to {} gp".format(target_amount))

    hoard = generate_hoard_v2(target_amount)

    print("")
    for coin, amount in hoard.items():
        print("* {:,} {} pieces".format(amount, coin))
    print("")
    print("Total value: {:,} gp".format(hoard_total(hoard)))
    total_coins = sum(hoard.values())
    print("Total coins: {:,}".format(total_coins))
    total_weight = total_coins / 50
    print("Total weight: {} pounds".format(total_weight))
    coin_volume = 0.6025 ** 2 * pi * 0.085
    packing_density = 0.7
    total_volume = coin_volume * total_coins / packing_density
    print("Total volume: {:,} in^3".format(round(total_volume, 2)))


def hoard_total(hoard):
    total = 0
    for coin, amount in hoard.items():
        total += COIN_VALUES[coin] * amount
    return total


def generate_hoard_v1(target_amount: int):
    coin_probabilities = [
        ("copper", 1),
        ("silver", 0.1),
        ("gold", 0.01),
        ("platinum", 0.001),
    ]
    hoard = {
        "copper": 0,
        "silver": 0,
        "gold": 0,
        "platinum": 0
    }

    while hoard_total(hoard) < target_amount:
        coin = random.choices(*zip(*coin_probabilities))[0]
        hoard[coin] += 1

    return hoard


def generate_hoard_v2(target_amount: int):
    """

    """
    hoard = {
        "copper": 0,
        "silver": 0,
        "gold": 0,
        "platinum": 0
    }
    coin, value = None, None
    for coin, value in COIN_VALUES.items():
        print(f"Remaining value needed: {target_amount:,} gp")
        magnitude = log10(target_amount)
        lower_bound_magnitude = magnitude - log10(value) - 1
        upper_bound_magnitude = lower_bound_magnitude + 1
        print(f"{coin}: {int(10 ** lower_bound_magnitude):,} to {int(10 ** upper_bound_magnitude):,}")
        mag = random.random() * (upper_bound_magnitude - lower_bound_magnitude) + lower_bound_magnitude
        amount = int(10 ** mag)
        print("Adding {:,} {} pieces".format(amount, coin))
        hoard[coin] = amount
        target_amount -= amount * value
    print(f"Remaining value needed: {target_amount:,} gp")
    amount = ceil(target_amount / value)
    print("Adding {:,} {} pieces".format(amount, coin))
    hoard[coin] += amount
    return hoard


if __name__ == '__main__':
    main()
