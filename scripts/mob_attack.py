# d = {
#     1: 1,
#     2: 1,
#     3: 1,
#     4: 1,
#     5: 1,
#     6: 2,
#     7: 2,
#     8: 2,
#     9: 2,
#     10: 2,
#     11: 2,
#     12: 2,
#     13: 3,
#     14: 3,
#     15: 4,
#     16: 4,
#     17: 5,
#     18: 5,
#     19: 10,
#     20: 20
# }
from math import log

d = {
    1: 1,
    2: 1,
    3: 1,
    4: 1,
    5: 1,
    6: 2,
    7: 2,
    8: 2,
    9: 2,
    10: 2,
    11: 3,
    12: 3,
    13: 4,
    14: 4,
    15: 5,
    16: 6,
    17: 7,
    18: 10,
    19: 15,
    20: 30
}

threshold = 0.79


def percentage_chance(num):
    return (21 - num) * 0.05


print("For a target roll of <A>, if there are <B> attackers, there is a <C> chance that one will hit.")
for i in range(1, 21):
    p = percentage_chance(i)
    number_needed = 1
    while True:
        chance_of_at_least_one_hit = 1 - ((1 - p) ** number_needed)
        if chance_of_at_least_one_hit >= threshold:
            break
        number_needed += 1
    print("{:>2} | {:>2} | {:.1%}".format(i, number_needed, chance_of_at_least_one_hit))
