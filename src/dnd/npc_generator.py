import sys
from math import ceil
from typing import Any, Union, List, Optional

from src.dnd.npc_enums import cr_list, races, roles, die_types, total_damage_dict

g_hp = "average"
g_dmg = "dice"


def get_options():
    """
    Returns the available CR, Race, and Weapon values, as well as the HP and Damage options.
    """
    return [cr_list, races.keys(), roles.keys(), die_types.keys(), g_hp, g_dmg]


def set_options(hp="average", damage="average"):
    """
    Sets the global options for all created NPCs for how their HP and Damage are calculated.
    The f"hp" parameter accepts the following values:
      * average: The average of the range given, taking into account racial and other bonuses.
      * random: A random value from within the range given, taking into account racial and other bonuses.
    The f"damage" parameter accepts the same values as f"hp", as well as the following:
      * dice: A best-guess for a dice value based on the damage range, with a modifier to bring the average dice roll
              up to the average of the damage range. If a weapon value is provided (either weapon name or dice value),
              that weapon value will be used instead, and the damage modifier will be adjusted as appropriate.
    @param hp
    @param damage
    """
    global g_hp, g_dmg
    g_hp = hp
    g_dmg = damage


def create_npc(cr: str=None, level: str=None, race="", role="", damage_die_type="", dmg_option: str=None, **kwargs):
    """
    Meant to be used with encounter calculators like https://kastark.co.uk/rpgs/encounter-calculator-5th/
    """
    if race == "":
        race = "Human"
    if not dmg_option:
        dmg_option = g_dmg
    # Allow "hp" as a valid kwarg
    if "hp" in kwargs:
        kwargs["hit_points"] = kwargs["hp"]
    name = kwargs.get("name") or f"the {race.lower()}"
    normalized_cr = get_normalized_cr(cr, level)
    cr_values = get_cr_values(normalized_cr)
    prof_bonus = adjust(cr_values["prof_bonus"], kwargs.get("prof_bonus"))
    atk_dict = get_attack(normalized_cr, race, role)
    def_dict = get_defense(normalized_cr, race, role)
    num_attacks = adjust(atk_dict["num_attacks"], kwargs.get("num_attacks"))
    total_damage = int(adjust(atk_dict["total_damage"], kwargs.get("total_damage")))
    damage = get_dmg_value(total_damage, dmg_option, num_attacks, damage_die_type)
    double_damage = get_dmg_value(total_damage * 2, dmg_option, 1, "")
    triple_damage = get_dmg_value(total_damage * 3, dmg_option, 1, "")
    save_dc = atk_dict["save_dc"]
    placeholders_values = [damage, double_damage, triple_damage, save_dc, prof_bonus, name]
    special_abilities = adjust(
        fill_placeholders(get_list(race, role, "special_abilities"), *placeholders_values),
        kwargs.get("special_abilities")
    )
    bonus_actions = adjust(
        fill_placeholders(get_list(race, role, "bonus_actions"), *placeholders_values),
        kwargs.get("bonus_actions")
    )
    actions = adjust(
        fill_placeholders(get_list(race, role, "actions"), *placeholders_values),
        kwargs.get("actions")
    )
    reactions = adjust(
        fill_placeholders(get_list(race, role, "reactions"), *placeholders_values),
        kwargs.get("reactions")
    )
    villain_actions = adjust(
        fill_placeholders(get_list(race, role, "villain_actions"), *placeholders_values),
        kwargs.get("villain_actions")
    )
    return {
        "cr": cr,
        "level": level,
        "race": race,
        "role": role,
        "speed": get_speed(races[race], roles[role], kwargs.get("speed")),
        "stat_bonus": adjust(cr_values["stat_bonus"], kwargs.get("stat_bonus")),
        "prof_bonus": prof_bonus,
        "armor_class": adjust(def_dict["ac"], kwargs.get("armor_class")),
        "hit_points": adjust(def_dict["hp"], kwargs.get("hit_points")),
        "damage_resistances": adjust(get_trait(race, role, "damage_resistances"), kwargs.get("damage_resistances")),
        "damage_immunities": adjust(get_trait(race, role, "damage_immunities"), kwargs.get("damage_immunities")),
        "damage_vulnerabilities": adjust(get_trait(race, role, "damage_vulnerabilities"), kwargs.get("damage_vulnerabilities")),
        "senses": adjust(get_trait(race, role, "senses"), kwargs.get("senses")),
        "special_abilities": special_abilities,
        "bonus_actions": bonus_actions,
        "actions": actions,
        "reactions": reactions,
        "villain_actions": villain_actions,
        "attack": adjust(atk_dict["attack"], kwargs.get("attack")),
        "damage": adjust(damage, kwargs.get("damage")),
        "double_damage": double_damage,
        "triple_damage": triple_damage,
        "save_dc": adjust(save_dc, kwargs.get("save_dc")),
        "num_attacks": num_attacks,
    }
    # except Exception as e:
    #     raise Exception(f"Error when generating NPC({cr}, {race}, {role}, {damage_die_type}, {dmg_option}, {kwargs})\n"
    #                     f"{e}")


def get_cr_values(normalized_cr: int):
    """
    Using equations from http://blogofholding.com/?p=7338
    """
    total_damage = total_damage_dict.get(normalized_cr, 5 * (normalized_cr + 1))
    s = 2 + normalized_cr // 4
    good_save = 4 + normalized_cr // 2
    return {
        "stat_bonus": s,
        "prof_bonus": good_save - s,
        "ac": 13 + normalized_cr // 3,
        "hp": total_damage * 3,
        "attack": 4 + normalized_cr // 2,
        "total_damage": total_damage,
        "save_dc": 11 + normalized_cr // 2,
        "num_attacks": (normalized_cr - 1) // 5 + 2
    }


def get_normalized_cr(cr: Optional[str], level: str = None) -> int:
    """
    Adjusts "0", "1/8", "1/4", and "1/2" to -3, -2, -1, and 0 respectively
    """
    if level is not None:
        return int(level) - 3
    c = ("0", "1/8", "1/4", "1/2")
    if str(cr) in c:
        return c.index(str(cr)) - 3
    return int(cr)


def get_speed(*dicts):
    speed = "30 ft."
    for d in dicts:
        if d and "speed" in d:
            speed = d["speed"]
    return speed


def get_attack(cr: int, race: str, role: str):
    return get_adjusted_cr_values(cr, race, role, "atk_cr", ["num_attacks"])


def get_defense(cr: int, race: str, role: str):
    return get_adjusted_cr_values(cr, race, role, "def_cr", ["ac"])


def get_adjusted_cr_values(cr: int, race: str, role: str, key: str, extra_keys: List[str] = None) -> dict:
    cr = adjust_cr(cr, races[race].get(key, 0))
    cr = adjust_cr(cr, roles[role].get(key, 0))
    cr_values = get_cr_values(cr)
    if extra_keys:
        for extra_key in extra_keys:
            cr_values[extra_key] = adjust(cr_values[extra_key], races[race].get(extra_key))
            cr_values[extra_key] = adjust(cr_values[extra_key], roles[role].get(extra_key))
    return cr_values


def adjust_cr(cr: int, adjustment: int) -> int:
    if adjustment == 0:
        return cr
    # index = cr_list.index(str(cr))
    # index += adjustment
    # index = min(max(index, 0), len(cr_list) - 1)
    # return cr_list[index]
    cr += adjustment
    return min(max(cr, -3), 30)


# def get_hp_value(values, hp_option):
#     if hp_option == "average":
#         return avg(values)
#     elif hp_option == "random":
#         return randint(values[0], values[1])
#     print(f"Invalid HP option: {hp_option}")
#     return None


def get_trait(race, role, key):
    return ", ".join(get_list(race, role, key))


def fill_placeholders(ability_list, damage, double_damage, triple_damage, save_dc, prof_bonus, name):
    for i in range(len(ability_list)):
        # noinspection StrFormat
        try:
            ability_list[i] = ability_list[i].format(
                damage=damage,
                double_damage=double_damage,
                triple_damage=triple_damage,
                save_dc=save_dc,
                prof_bonus=prof_bonus,
                name=name,
                Name=name.title(),
            )
        except ValueError:
            print(ability_list, file=sys.stderr)
            raise
    return ability_list


def get_list(race, role, key):
    item_list = []
    d = races[race]
    if key in d:
        item_list += d[key]
    d = roles[role]
    if key in d:
        item_list += d[key]
    return item_list


def get_dmg_value(value, dmg_option, num_attacks, die_type):
    avg_damage = myround(value / int(num_attacks))
    # print(f"Inputs: {value} | {num_attacks} | {int(num_attacks)} | {value / int(num_attacks)} | {avg_damage}")
    if dmg_option == "average":
        return avg_damage
    elif dmg_option == "dice":
        # print(f"Average damage: {avg_damage}")
        if die_type == "":
            die_avg = 3.5  # Default to d6
        else:
            die_avg = die_types[die_type]
        # print(f"Die type: {die_type}")
        # print(f"Die average: {die_avg}")
        num_dice = int(avg_damage / die_avg)  # Number of d6s
        # print(f"Num dice: {num_dice}")
        if num_dice == 0:
            if die_type == "":  # If die_type is undefined and the damage is too small, allow us to drop to d4
                die_type = "d4"
                die_avg = 2.5
                num_dice = int(avg_damage / die_avg)  # Number of d4s
            if num_dice == 0:
                num_dice = 1  # Always roll a minimum of 1 die, and let the modifier be negative
            # print(f"Num dice: {num_dice}")
        if die_type == "":
            die_type = "d6"
        mod = int(avg_damage - num_dice * die_avg)
        # print(f"Stuff: {avg_damage} | {num_dice} | {die_avg} | {mod}")
        if mod == 0:
            return f"{avg_damage} ({num_dice}{die_type})"
        elif mod > 0:
            return f"{avg_damage} ({num_dice}{die_type} + {mod})"
        else:
            return f"{avg_damage} ({num_dice}{die_type} - {abs(mod)})"
    print(f"Invalid damage option: {dmg_option}", file=sys.stderr)
    return None


def myround(n):
    if n * 10 % 10 == 5:
        return ceil(n)
    return round(n)


def avg(t):
    return round((t[0] + t[1]) / 2)


def adjust(value: Any, adjustment: Any) -> Union[str, list, dict]:
    # If adjustment isn't defined, just return value
    if adjustment is None:
        return value
    # If value is a list, assume adjustment is a list and concat them
    if isinstance(value, list):
        return value + adjustment
    # If value is a dict, assume adjustment is a dict and merge them
    if isinstance(value, dict):
        value = value.copy()
        value.update(adjustment)
        return value
    try:
        value = int(value)
    except ValueError:
        pass
    # If the adjustment is a string, try to process it like a number
    if isinstance(adjustment, str):
        if adjustment.startswith("+") or adjustment.startswith("-"):
            return str(value + int(adjustment))
        if adjustment.startswith("x"):
            return str(int(value * float(adjustment[1:])))
        if adjustment.startswith("/"):
            return str(int(value / float(adjustment[1:])))
    if isinstance(adjustment, (int, float)):
        return str(adjustment)
    return adjustment


# Unit Tests

def assertEqual(actual, expected):
    if actual != expected:
        raise AssertionError(f"{actual} (type={type(actual)}) != {expected} (type={type(expected)})")


if __name__ == "__main__":
    assertEqual(adjust_cr(-3, 1), -2)
    assertEqual(adjust_cr(-3, 2), -1)
    assertEqual(adjust_cr(-3, 3), 0)
    assertEqual(adjust_cr(-3, 4), 1)
    assertEqual(adjust_cr(-3, 5), 2)
    assertEqual(adjust_cr(29, 5), 30)
    assertEqual(adjust_cr(2, 0),  2)
    assertEqual(adjust_cr(2, -1), 1)
    assertEqual(adjust_cr(2, -2), 0)
    assertEqual(adjust_cr(2, -3), -1)
    assertEqual(adjust_cr(2, -4), -2)
    assertEqual(adjust_cr(2, -5), -3)
    assertEqual(adjust_cr(2, -6), -3)

    assertEqual(get_normalized_cr("0"), -3)
    assertEqual(get_normalized_cr("1/8"), -2)
    assertEqual(get_normalized_cr("1/4"), -1)
    assertEqual(get_normalized_cr("1/2"), 0)
    assertEqual(get_normalized_cr("1"), 1)
    assertEqual(get_normalized_cr("2"), 2)
    assertEqual(get_normalized_cr("3"), 3)
    assertEqual(get_normalized_cr(None, "1"), -2)
    assertEqual(get_normalized_cr(None, "2"), -1)
    assertEqual(get_normalized_cr(None, "3"), 0)
    assertEqual(get_normalized_cr(None, "4"), 1)

    assertEqual("13", adjust(10, "+3"))
    assertEqual("7", adjust(10, "-3"))
    assertEqual("30", adjust(10, "x3"))
    assertEqual("3", adjust(10, "3"))
    assertEqual("3", adjust(10, +3))
    assertEqual("-3", adjust(10, -3))
    assertEqual([1, 2, 3], adjust(10, [1, 2, 3]))
    assertEqual({"a": 1, "b": 2}, adjust(10, {"a": 1, "b": 2}))
    assertEqual(10, adjust(10, None))
    assertEqual("soup", adjust(10, "soup"))
    assertEqual("13", adjust("10", "+3"))
    assertEqual("soup", adjust("soap", "soup"))
    assertEqual(["a", "b", "c", 1, 2, 3], adjust(["a", "b", "c"], [1, 2, 3]))
    assertEqual({"a": 1, "b": 2, "c": 3, "d": 4}, adjust({"c": 3, "d": 4}, {"a": 1, "b": 2}))

    for i in range(-3, 21):
        print(f"{i}: {get_cr_values(i)}")

    for i in cr_list:
        npc = create_npc(i)
        print(f"{i}: {npc['num_attacks']} / {npc['damage']} / {npc['double_damage']} / {npc['triple_damage']}")
