from statistics import mean, stdev

from random import randint

PROF_BONUS = 6


def con_save(bonus, dc, use_ki):
    """

    :param bonus:
    :param dc:
    :param use_ki:
    :return: 2-tuple (passed check?, used 1 ki to reroll save?)
    """
    if randint(1, 20) + bonus >= dc:
        return True, False
    if use_ki:
        return randint(1, 20) + bonus >= dc, True
    return False, False


def how_long_can_i_go(base_dc, con_mod, starting_ki, starting_exhaustion=0):
    rounds_spent = 0
    rounds_since_first_failure = 0
    passed_checks = 0
    has_failed_a_check = False
    exhaustion = starting_exhaustion
    ki_points = starting_ki
    while True:
        passed_check, used_ki = con_save(con_mod + PROF_BONUS, base_dc + passed_checks, ki_points > 0)
        rounds_spent += 1
        if has_failed_a_check:
            rounds_since_first_failure += 1
        if used_ki:
            ki_points -= 1
        if passed_check:
            passed_checks += 1
        else:
            has_failed_a_check = True
            if exhaustion < 6:
                exhaustion += 1
            else:
                return rounds_spent, rounds_since_first_failure, passed_checks
        rounds_spent += 0


iterations = 100000
base_dc = 12
con_mod = 3
starting_ki = 0
run_results = []
first_failure_results = []
before_first_failure_results = []
passed_check_results = []
for _ in range(iterations):
    rounds_spent, rounds_since_first_failure, passed_checks = how_long_can_i_go(base_dc, con_mod, starting_ki)
    rounds_before_first_failure = rounds_spent - rounds_since_first_failure
    run_results.append(rounds_spent)
    first_failure_results.append(rounds_since_first_failure)
    before_first_failure_results.append(rounds_before_first_failure)
    passed_check_results.append(passed_checks)

print(f"Base DC={base_dc}, Con mod={con_mod}, Starting ki={starting_ki}, Simulations run={iterations}")
print(f"Average rounds: {mean(run_results)}, stdev={stdev(run_results)}")
print(f"Average rounds since first failure: {mean(first_failure_results)}, stdev={stdev(first_failure_results)}")
print(f"Average rounds before first failure: {mean(before_first_failure_results)}, stdev={stdev(before_first_failure_results)}")
print(f"Average successful saves: {mean(passed_check_results)}, stdev={stdev(passed_check_results)}")
