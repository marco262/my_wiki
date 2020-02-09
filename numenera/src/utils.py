from random import randint


def pick_mutation(mutations):
    r = randint(1, 100)
    for m in mutations:
        if m[1] is None:
            if m[0] == r:
                return m
        elif m[0] <= r <= m[1]:
            return m


def pick_two_mutations(mutations):
    m = pick_mutation(mutations)
    n = m
    while n == m:
        n = pick_mutation(mutations)
    return m, n
