import sys
from random import randint

from src.dnd.npc_enums import cr_dict, races, roles, die_types, cr_list

g_hp = "average"
g_dmg = "dice"


def get_options():
    """
    Returns the available CR, Race, and Weapon values, as well as the HP and Damage options.
    """
    return [cr_dict.keys(), races.keys(), roles.keys(), die_types.keys(), g_hp, g_dmg]


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


def create_npc(cr, race="", role="", damage_die_type="", hp_option=None, dmg_option=None, **kwargs):
    if race == "":
        race = "Human"
    if not hp_option:
        hp_option = g_hp
    if not dmg_option:
        dmg_option = g_dmg
    # Allow "hp" as a valid kwarg
    if "hp" in kwargs:
        kwargs["hit_points"] = kwargs["hp"]
    cr_values = cr_dict[cr]
    atk_dict = get_attack(cr, race, role)
    def_dict = get_defense(cr, race, role)
    damage = get_dmg_value(atk_dict["total_damage"], dmg_option, atk_dict["num_attacks"], damage_die_type)
    save_dc = atk_dict["save_dc"]
    return {
        "cr": cr,
        "race": race,
        "role": role,
        "speed": kwargs.get("speed") or get_speed(races[race]),
        "stat_bonus": kwargs.get("stat_bonus") or cr_values["stat_bonus"],
        "prof_bonus": kwargs.get("prof_bonus") or cr_values["prof_bonus"],
        "armor_class": kwargs.get("armor_class") or def_dict["ac"],
        "hit_points": kwargs.get("hit_points") or get_hp_value(def_dict["hp"], hp_option),
        "damage_resistances": kwargs.get("damage_resistances") or get_trait(race, role, "damage_resistances"),
        "damage_immunities": kwargs.get("damage_immunities") or get_trait(race, role, "damage_immunities"),
        "senses": kwargs.get("senses") or get_trait(race, role, "senses"),
        "special_abilities": kwargs.get("special_abilities") or fill_placeholders(get_list(race, role, "special_abilities"), damage, save_dc),
        "actions": kwargs.get("actions") or fill_placeholders(get_list(race, role, "actions"), damage, save_dc),
        "reactions": kwargs.get("reactions") or fill_placeholders(get_list(race, role, "reactions"), damage, save_dc),
        "attack": kwargs.get("attack") or atk_dict["attack"],
        "damage": kwargs.get("damage") or damage,
        "save_dc": kwargs.get("save_dc") or save_dc,
        "num_attacks": kwargs.get("num_attacks") or atk_dict["num_attacks"],
    }


def get_speed(d):
    if "speed" in d:
        return d["speed"]
    return "30 ft."


def get_attack(cr, race, role):
    return get_adjusted_cr_dict(cr, race, role, "atk_cr")


def get_defense(cr, race, role):
    return get_adjusted_cr_dict(cr, race, role, "def_cr")


def get_adjusted_cr_dict(cr, race, role, key):
    d = races[race]
    if key in d:
        cr = adjust_cr(cr, d[key])
    d = roles[role]
    if key in d:
        cr = adjust_cr(cr, d[key])
    return cr_dict[cr]


def adjust_cr(cr, adjustment):
    if adjustment == 0:
        return cr
    index = cr_list.index(str(cr))
    index += adjustment
    index = min(max(index, 0), len(cr_list) - 1)
    return cr_list[index]


def get_hp_value(values, hp_option):
    if hp_option == "average":
        return avg(values)
    elif hp_option == "random":
        return randint(values[0], values[1])
    print(f"Invalid HP option: {hp_option}")
    return None


def get_trait(race, role, key):
    return ",".join(get_list(race, role, key))


def fill_placeholders(ability_list, damage, save_dc):
    for i in range(len(ability_list)):
        # noinspection StrFormat
        ability_list[i] = ability_list[i].format(damage=damage, save_dc=save_dc)
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


def get_dmg_value(values, dmg_option, num_attacks, die_type):
    if dmg_option == "average":
        return round(avg(values) / num_attacks)
    elif dmg_option == "random":
        return round(randint(values[0], values[1]) / num_attacks)
    elif dmg_option == "dice":
        avg_damage = round(avg(values) / num_attacks)
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
                num_dice = round(avg_damage / die_avg)  # Number of d4s
            if num_dice == 0:
                num_dice = 1  # Always roll a minimum of 1 die, and the modifier be negative
            # print(f"Num dice: {num_dice}")
        mod = int(avg_damage - num_dice * die_avg)
        # print(f"Mod: {mod}")
        if die_type == "":
            die_type = "d6"
        if mod == 0:
            return f"{avg_damage} ({num_dice}{die_type})"
        elif mod > 0:
            return f"{avg_damage} ({num_dice}{die_type} + {mod})"
        else:
            return f"{avg_damage} ({num_dice}{die_type} - {abs(mod)})"
    print(f"Invalid damage option: {dmg_option}", file=sys.stderr)
    return None


def avg(t):
    return round((t[0] + t[1]) / 2)


# Unit Tests

def assertEqual(actual, expected):
    if actual != expected:
        print(f"{actual} (type={type(actual)}) != {expected} (type={type(expected)})")


assertEqual(adjust_cr("0", 1),  "1/8")
assertEqual(adjust_cr("0", 2),  "1/4")
assertEqual(adjust_cr("0", 3),  "1/2")
assertEqual(adjust_cr("0", 4),  "1")
assertEqual(adjust_cr("0", 5),  "2")
assertEqual(adjust_cr("29", 5),  "30")
assertEqual(adjust_cr("2", 0),  "2")
assertEqual(adjust_cr("2", -1),  "1")
assertEqual(adjust_cr("2", -2),  "1/2")
assertEqual(adjust_cr("2", -3),  "1/4")
assertEqual(adjust_cr("2", -4),  "1/8")
assertEqual(adjust_cr("2", -5),  "0")
assertEqual(adjust_cr("2", -6),  "0")
