import glob
from json import load

cr_list = [
    "0", "1/8", "1/4", "1/2", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14",
    "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30"
]
# cr_dict = {
#     "0": {"stat_bonus": 0, "prof_bonus": 2, "ac": 10, "hp": [1, 6], "attack": 2, "total_damage": [0, 1], "save_dc": 12, "num_attacks": 1},
#     "1/8": {"stat_bonus": 1, "prof_bonus": 2, "ac": 11, "hp": [7, 23], "attack": 3, "total_damage": [2, 3], "save_dc": 13, "num_attacks": 1},
#     "1/4": {"stat_bonus": 1, "prof_bonus": 2, "ac": 12, "hp": [24, 49], "attack": 3, "total_damage": [4, 5], "save_dc": 13, "num_attacks": 1},
#     "1/2": {"stat_bonus": 1, "prof_bonus": 2, "ac": 13, "hp": [50, 70], "attack": 3, "total_damage": [6, 8], "save_dc": 13, "num_attacks": 1},
#     "1": {"stat_bonus": 1, "prof_bonus": 2, "ac": 13, "hp": [71, 85], "attack": 3, "total_damage": [9, 14], "save_dc": 13, "num_attacks": 2},
#     "2": {"stat_bonus": 1, "prof_bonus": 2, "ac": 13, "hp": [86, 100], "attack": 3, "total_damage": [15, 20], "save_dc": 13, "num_attacks": 2},
#     "3": {"stat_bonus": 2, "prof_bonus": 2, "ac": 13, "hp": [101, 115], "attack": 4, "total_damage": [21, 26], "save_dc": 13, "num_attacks": 2},
#     "4": {"stat_bonus": 2, "prof_bonus": 2, "ac": 14, "hp": [116, 130], "attack": 5, "total_damage": [27, 32], "save_dc": 14, "num_attacks": 2},
#     "5": {"stat_bonus": 2, "prof_bonus": 3, "ac": 15, "hp": [131, 145], "attack": 6, "total_damage": [33, 38], "save_dc": 15, "num_attacks": 2},
#     "6": {"stat_bonus": 2, "prof_bonus": 3, "ac": 15, "hp": [146, 160], "attack": 6, "total_damage": [39, 44], "save_dc": 15, "num_attacks": 3},
#     "7": {"stat_bonus": 2, "prof_bonus": 3, "ac": 15, "hp": [161, 175], "attack": 6, "total_damage": [45, 50], "save_dc": 15, "num_attacks": 3},
#     "8": {"stat_bonus": 3, "prof_bonus": 3, "ac": 16, "hp": [176, 190], "attack": 7, "total_damage": [51, 56], "save_dc": 16, "num_attacks": 3},
#     "9": {"stat_bonus": 3, "prof_bonus": 4, "ac": 17, "hp": [191, 205], "attack": 7, "total_damage": [57, 62], "save_dc": 16, "num_attacks": 3},
#     "10": {"stat_bonus": 3, "prof_bonus": 4, "ac": 17, "hp": [206, 220], "attack": 7, "total_damage": [63, 68], "save_dc": 16, "num_attacks": 3},
#     "11": {"stat_bonus": 3, "prof_bonus": 4, "ac": 17, "hp": [221, 235], "attack": 8, "total_damage": [69, 74], "save_dc": 17, "num_attacks": 4},
#     "12": {"stat_bonus": 3, "prof_bonus": 4, "ac": 17, "hp": [236, 250], "attack": 8, "total_damage": [75, 80], "save_dc": 17, "num_attacks": 4},
#     "13": {"stat_bonus": 4, "prof_bonus": 5, "ac": 18, "hp": [251, 265], "attack": 8, "total_damage": [81, 86], "save_dc": 18, "num_attacks": 4},
#     "14": {"stat_bonus": 4, "prof_bonus": 5, "ac": 18, "hp": [266, 280], "attack": 8, "total_damage": [87, 92], "save_dc": 18, "num_attacks": 4},
#     "15": {"stat_bonus": 4, "prof_bonus": 5, "ac": 18, "hp": [281, 295], "attack": 8, "total_damage": [93, 98], "save_dc": 18, "num_attacks": 4},
#     "16": {"stat_bonus": 4, "prof_bonus": 5, "ac": 18, "hp": [296, 310], "attack": 9, "total_damage": [99, 104], "save_dc": 18, "num_attacks": 5},
#     "17": {"stat_bonus": 4, "prof_bonus": 6, "ac": 19, "hp": [311, 325], "attack": 10, "total_damage": [105, 110], "save_dc": 19, "num_attacks": 5},
#     "18": {"stat_bonus": 4, "prof_bonus": 6, "ac": 19, "hp": [326, 340], "attack": 10, "total_damage": [111, 116], "save_dc": 19, "num_attacks": 5},
#     "19": {"stat_bonus": 4, "prof_bonus": 6, "ac": 19, "hp": [341, 355], "attack": 10, "total_damage": [117, 122], "save_dc": 19, "num_attacks": 5},
#     "20": {"stat_bonus": 4, "prof_bonus": 6, "ac": 19, "hp": [356, 400], "attack": 10, "total_damage": [123, 140], "save_dc": 19, "num_attacks": 6},
#     "21": {"stat_bonus": 4, "prof_bonus": 7, "ac": 19, "hp": [401, 445], "attack": 11, "total_damage": [141, 158], "save_dc": 20, "num_attacks": 6},
#     "22": {"stat_bonus": 4, "prof_bonus": 7, "ac": 19, "hp": [446, 490], "attack": 11, "total_damage": [159, 176], "save_dc": 20, "num_attacks": 6},
#     "23": {"stat_bonus": 4, "prof_bonus": 7, "ac": 19, "hp": [491, 535], "attack": 11, "total_damage": [177, 194], "save_dc": 20, "num_attacks": 6},
#     "24": {"stat_bonus": 5, "prof_bonus": 7, "ac": 19, "hp": [536, 580], "attack": 12, "total_damage": [195, 212], "save_dc": 21, "num_attacks": 6},
#     "25": {"stat_bonus": 5, "prof_bonus": 8, "ac": 19, "hp": [581, 625], "attack": 12, "total_damage": [213, 230], "save_dc": 21, "num_attacks": 6},
#     "26": {"stat_bonus": 5, "prof_bonus": 8, "ac": 19, "hp": [626, 670], "attack": 12, "total_damage": [231, 248], "save_dc": 21, "num_attacks": 6},
#     "27": {"stat_bonus": 5, "prof_bonus": 8, "ac": 19, "hp": [671, 715], "attack": 13, "total_damage": [249, 266], "save_dc": 22, "num_attacks": 6},
#     "28": {"stat_bonus": 5, "prof_bonus": 8, "ac": 19, "hp": [716, 760], "attack": 13, "total_damage": [267, 284], "save_dc": 22, "num_attacks": 6},
#     "29": {"stat_bonus": 5, "prof_bonus": 9, "ac": 19, "hp": [761, 805], "attack": 13, "total_damage": [285, 302], "save_dc": 22, "num_attacks": 6},
#     "30": {"stat_bonus": 5, "prof_bonus": 9, "ac": 19, "hp": [806, 850], "attack": 14, "total_damage": [303, 320], "save_dc": 23, "num_attacks": 6},
# }
# Uses adjusted CR
total_damage_dict = {
    -3: 1,
    -2: 3,
    -1: 5,
    0: 8,
}


def build_enum_dict(enum_type: str):
    d = {}
    for filepath in glob.glob(f"data/dnd/npc/npc_{enum_type}_*.json"):
        print(f"Loading {filepath} into NPC {enum_type} enum...")
        with open(filepath) as f:
            d.update(load(f))
    return d


races = build_enum_dict("races")
roles = build_enum_dict("roles")


die_types = {
    "d2": 1.5,
    "d3": 2,
    "d4": 2.5,
    "d6": 3.5,
    "d8": 4.5,
    "d10": 5.5,
    "d12": 6.5,
    "d20": 10.5,
}

npc_gender = [
    "Male",
    "Female",
]
npc_appearance = [
    "Distinctive jewelry: earrings, necklace, circlet, bracelets",
    "Piercings",
    "Flamboyant or outlandish clothes",
    "Formal, clean clothes",
    "Ragged, dirty clothes",
    "Pronounced scar",
    "Missing teeth",
    "Missing fingers",
    "Unusual eye color (or two different colors)",
    "Tattoos",
    "Birthmark",
    "Unusual skin color",
    "Bald",
    "Braided beard or hair",
    "Unusual hair color",
    "Nervous eye twitch",
    "Distinctive nose",
    "Distinctive posture (crooked or rigid)",
    "Exceptionally beautiful",
    "Exceptionally ugly",
]
npc_high_ability = [
    "Strength -- powerful, brawny, strong as an ox",
    "Dexterity -- lithe, agile, graceful",
    "Constitution -- hardy, hale, healthy",
    "Intelligence -- studious, learned, inquisitive",
    "Wisdom -- perceptive, spiritual, insightful",
    "Charisma -- persuasive, forceful, born leader",
    "Nothing notable"
]
npc_low_ability = [
    "Strength -- feeble, scrawny",
    "Dexterity -- clumsy, fumbling",
    "Constitution -- sickly, pale",
    "Intelligence -- dim-witted, slow",
    "Wisdom -- oblivious, absentminded",
    "Charisma -- dull, boring",
]
npc_talent = [
    "Plays a musical instrument",
    "Speaks several languages fluently",
    "Unbelievably lucky",
    "Perfect memory",
    "Great with animals",
    "Great with children",
    "Great at solving puzzles",
    "Great at one game",
    "Great at impersonations",
    "Draws beautifully",
    "Paints beautifully",
    "Sings beautifully",
    "Drinks everyone under the table",
    "Expert carpenter",
    "Expert cook",
    "Expert dart thrower and rock skipper",
    "Expert juggler",
    "Skilled actor and master of disguise",
    "Skilled dancer",
    "Knows Thieves' Cant",
]
npc_mannerisms = [
    "Prone to singing, whistling, or humming quietly",
    "Speaks in rhyme or some other peculiar way",
    "Particularly low or high voice",
    "Slurs words, lisps, or stutters",
    "Enunciates overly clearly",
    "Speaks loudly",
    "Whispers",
    "Uses flowery speech or long words",
    "Frequently uses the wrong word",
    "Uses colorful oaths and exclamations",
    "Makes constant jokes or puns",
    "Prone to predictions of doom",
    "Fidgets",
    "Squints",
    "Stares into the distance",
    "Chews something",
    "Paces",
    "Taps fingers",
    "Bites fingernails",
    "Twirls hair or tugs beard",
]
npc_interaction_trait = [
    "Argumentative",
    "Arrogant",
    "Blustering",
    "Rude",
    "Curious",
    "Friendly",
    "Honest",
    "Hot tempered",
    "Irritable",
    "Ponderous",
    "Quiet",
    "Suspicious",
]
npc_good_ideals = [
    "Beauty",
    "Charity",
    "Greater good",
    "Life",
    "Respect",
    "Self-sacrifice",
]
npc_evil_ideals = [
    "Domination",
    "Greed",
    "Might",
    "Pain",
    "Retribution",
    "Slaughter",
]
npc_lawful_ideals = [
    "Community",
    "Fairness",
    "Honor",
    "Logic",
    "Responsibility",
    "Tradition",
]
npc_chaotic_ideals = [
    "Change",
    "Creativity",
    "Freedom",
    "Independence",
    "No limits",
    "Whimsy",
]
npc_neutral_ideals = [
    "Balance",
    "Knowledge",
    "Live and let live",
    "Moderation",
    "Neutrality",
    "People",
]
npc_other_ideals = [
    "Aspiration",
    "Discovery",
    "Glory",
    "Nation",
    "Redemption",
    "Self-knowledge",
]
npc_bonds = [
    "Dedicated to fulfilling a personal life goal",
    "Protective of close family members",
    "Protective of colleagues or compatriots",
    "Loyal to a benefactor, patron, or employer",
    "Captivated by a romantic interest",
    "Drawn to a special place",
    "Protective of a sentimental keepsake",
    "Protective of a va luable possession",
    "Out for revenge",
    "Roll twice, ignoring results of10",
]
npc_flaws_and_secrets = [
    "Forbidden love or susceptibility to romance",
    "Enjoys decadent pleasures",
    "Arrogance",
    "Envies another creature's possessions or station",
    "Overpowering greed",
    "Prone to rage",
    "Has a powerful enemy",
    "Specific phobia",
    "Shameful or scandalous history",
    "Secret crime or misdeed",
    "Possession of forbidden lore",
    "Foolhardy bravery",
]
