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


races = {
    "Human": {},
    "Dwarf": {
        "speed": "25 ft.",
        "damage_resistances": ["poison"],
        "senses": ["darkvision 60 ft."],
        "special_abilities": [
            "***Dwarven Resilience.*** The dwarf has advantage on saving throws against poison, and has "
            "resistance against poison damage."
        ]
    },
    "Elf": {
        "senses": ["darkvision 60 ft."],
        "special_abilities": [
            "***Fey Ancestry.*** The elf has advantage on saving throws against being charmed, and magic "
            "can't put him to sleep."
        ]
    },
    "Halfling": {
        "speed": "25 ft.",
        "senses": ["darkvision 60 ft."],
        "special_abilities": [
            "***Brave.*** The halfling has advantage on any saving throws against being frightened.",
            "***Halfling Nimbleness.*** The halfling can move through the space of a medium or larger "
            "creature."
        ]
    },
    "Dragonborn": {
        # "atk_cr": 1,
        "damage_resistances": ["fire"],
        "actions": [
            "***Breath Weapon (Recharge 5-6).*** The dragonborn can use his action to exhale a 15-foot "
            "cone of fire. Each creature in the cone must make a DC {save_dc} Dexterity saving throw, taking {damage} "
            "fire damage on a failed save, or half as much damage on a successful one."
        ]
    },
    "Gnome": {
        # "def_cr": 1,
        "speed": "25 ft.",
        "senses": ["darkvision 60 ft."],
        "special_abilities": [
            "***Gnome Cunning.*** The gnome has advantage on all Intelligence, Wisdom, and Charisma saving "
            "throws against magic."
        ],
    },
    "Half-elf": {
        "senses": ["darkvision 60 ft."],
        "special_abilities": [
            "***Fey Ancestry.*** {name} has advantage on saving throws against being charmed, and "
            "magic can't put him to sleep."
        ],
    },
    "Half-orc": {
        # "def_cr": 1,
        "senses": ["darkvision 60 ft."],
        "special_abilities": [
            "***Relentless Endurance.*** When reduced to 0 hit points, the half-orc drops to 1 hit point "
            "instead (but can't do this again until he finishes a long rest).",
            "***Savage Attacks.*** When he scores a critical hit, the half-orc can roll one of the weapon's "
            "damage dice and add it to the extra damage of the critical hit."
        ],
    },
    "Tiefling": {
        # "atk_cr": 1,
        "damage_resistances": ["fire"],
        "senses": ["darkvision 60 ft."],
        "reactions": [
            "***Hellish Rebuke (1/day).*** When the tiefling takes damage from a creature within 60 feet "
            "that he can see, he can lash out with hellish flames. The creature must make a Dexterity saving throw "
            "(DC {save_dc}). It takes {damage} fire damage on a failed save, or half as much damage on a successful "
            "one."
        ]
    },
    "Aarakocra": {
        # "atk_cr": 1,
        "speed": "20 ft., fly 50 ft.",
        "special_abilities": [
            "***Dive Attack.*** If the aarakocra is flying and dives at least 30 feet straight toward a "
            "target and then hits it with a melee weapon attack, the attack deals an extra 3 (1d6) damage to the "
            "target."
        ]
    },
    "Deep Gnome": {
        # "def_cr": 1,
        "speed": "20 ft.",
        "senses": ["darkvision 120 ft."],
        "special_abilities": [
            "***Gnome Cunning.*** The deep gnome has advantage on all Intelligence, Wisdom, and Charisma "
            "saving throws against magic."
        ],
    },
    "Goliath": {
        # "def_cr": 1,
        "reactions": [
            "***Stone's Endurance (Recharge 5-6).*** When the goliath takes damage, he can use his reaction "
            "to reduce the damage taken by {damage}."
        ],
    },
    "Kenku": {
        # "atk_cr": 1,
        "special_abilities": [
            "***Ambusher.*** In the first round of a combat, the kenku has advantage on attack rolls "
            "against any creature it surprised.",
            "***Mimicry.*** The kenku can mimic any sounds it has heard, including voices. A creature that "
            "hears the sounds can tell they are imitations with a successful DC {save_dc} Wisdom (Insight) check."
        ]
    },
    "Tabaxi": {
        "speed": "30 ft., climb 20 ft.",
        "senses": ["darkvision 60 ft."],
        "special_abilities": [
            "***Feline Agility.*** When the tabaxi moves on its turn in combat, it can double its speed "
            "until the end of the turn. Once it uses this ability, the tabaxi can't use it again until it moves 0 "
            "feet on one of its turns."
        ],
    },
    "Bugbear": {
        # "atk_cr": 2,
        "atk_cr": -1,
        "special_abilities": [
            "***Brute.*** A melee weapon deals one extra die of its damage when the bugbear hits with it.",
            "***Surprise Attack.*** If the bugbear surprises a creature and hits it with an attack during "
            "the first round of combat, the target takes an extra {damage} damage from the attack."
        ]
    },
    "Goblin": {
        "def_cr": -1,
        "reactions": [
            "***Painful Tumble.*** When {name} is hit by an attack, it may gain resistance to the attack's damage, "
            "move up to half its speed away from the attacker without provoking opportunity attacks, and land prone.",
        ]
    },
    "Hobgoblin": {
        # "atk_cr": 1,
        "special_abilities": [
            "***Martial Advantage.*** Once per turn, the hobgoblin can deal an extra {damage} damage to "
            "a creature it hits with a weapon attack if that creature is within 5 feet of an ally of the hobgoblin "
            "that isn't incapacitated."
        ]
    },
    "Kobold": {
        # "atk_cr": 1,
        "special_abilities": [
            "***Sunlight Sensitivity.*** While in sunlight, the kobold has disadvantage on attack rolls, "
            "as well as on Wisdom (Perception) checks that rely on sight.",
            "***Pack Tactics.*** The kobold has advantage on an attack roll against a creature if at least "
            "one of the kobold's allies is within 5 feet of the creature and the ally isn't incapacitated."
        ]
    },
    "Orc": {
        # "atk_cr": 1,
        "special_abilities": [
            "***Aggressive.*** As a bonus action, the orc can move up to its speed toward a hostile creature "
            "that it can see."
        ]
    },
    "Duergar": {
        # "atk_cr": 2,  # +1 for Enlarge, +1 for Invisibility
        # "def_cr": 2,  # +1 for Duergar Resilience, +1 for Invisibility
        "atk_cr": -1,
        "def_cr": -1,
        "speed": "25 ft.",
        "special_abilities": [
            "***Duergar Resilience.*** The duergar has advantage on saving throws against poison, spells, "
            "and illusions, as well as to resist being charmed or paralyzed.",
            "***Sunlight Sensitivity.*** While in sunlight, the duergar has disadvantage on attack rolls, "
            "as well as on Wisdom (Perception) checks that rely on sight."
        ],
        "actions": [
            "***Enlarge.*** For 1 minute, the duergar magically increases in size, along with anything it "
            "is wearing or carrying. While enlarged, the duergar is Large, doubles its damage dice on Strength-based "
            "weapon attacks (included in the attacks), and makes Strength checks and Strength saving throws with "
            "advantage. If the duergar lacks the room to become Large, it attains the maximum size possible in the "
            "space available.",
            "***Invisibility.*** The duergar magically turns invisible until it attacks, casts a spell, or "
            "uses its Enlarge, or until its concentration is broken, up to 1 hour (as if concentrating on a spell). "
            "Any equipment the duergar wears or carries is invisible with it."
        ]
    },
    "Gnoll": {
        # "atk_cr": 1,
        "special_abilities": [
            "***Rampage.*** When the gnoll reduces a creature to 0 hit points with a melee attack on its "
            "turn, the gnoll can take a bonus action to move up to half its speed and make an attack."
        ]
    },
    "Wolf": {
        "atk_cr": -1,
        "special_abilities": [
            "***Keen Hearing and Smell.*** The wolf has advantage on Wisdom (Perception) checks that rely "
            "on hearing or smell.",
            "***Pack Tactics.*** The wolf has advantage on an attack roll against a creature if at least "
            "one of the wolf's allies is within 5 feet of the creature and the ally isn't incapacitated.",
        ]
    },
    "Boar": {
        "special_abilities": [
            "***Charge.*** If the boar moves up to 10 feet before attacking, it can do a single weapon attack that "
            "does double damage. If it hits, the enemy must make a DC {save_dc} Strength saving throw or be knocked "
            "prone.",
        ]
    },
    "Skeleton": {
        "damage_vulnerabilities": ["bludgeoning"],
    },
    "Elezen": {
        "speed": "35 ft.",
    },
    "Moogle": {
        "atk_cr": -1,
        "speed": "0 ft., fly 40 ft.",
        "actions": [
            "***Invisibility.*** The moogle magically turns invisible until it attacks, casts a spell, "
            "or until its concentration is broken, up to 1 hour (as if concentrating on a spell). "
            "Any equipment the moogle wears or carries is invisible with it."
        ]
    }
}
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
roles = {
    "": {},
    "Mage": {
        "atk_cr": +1,
        "def_cr": -1,
        "num_attacks": 1,
        "actions": [
            "***Close Range AoE (roll 1-2).*** 15-foot cone. {double_damage} damage "
            "(save for half, Dex DC {save_dc}).",
            "***Long Range AoE (roll 3).*** 30-foot range, 10-foot radius sphere. {triple_damage} damage "
            "(save for half, Dex DC {save_dc})."
        ]
    },
    "Healer": {
        "bonus_actions": [
            "***Quick Heal (roll 1).*** Heal 1 ally within 30 feet for {damage}.",
        ],
        "actions": [
            "***Mass Heal (roll 2).*** Heal all allies within 30 feet for {damage}.",
            "***Remove Condition (roll 3).*** Removes 1 condition from ally within 30 feet.",
            "***Inflict Condition (roll 4).*** Inflicts 1 condition (Blinded, Charmed, Deafened, Frightened, "
            "Poisoned, or Prone) to enemy within 30 feet. DC {save_dc} Wisdom save to negate.",
        ]
    },
    "Tank": {
        "def_cr": +1,
        "ac": "+2",
        "reactions": [
            # "***Shield Block.*** Give disadvantage on melee attack from adjacent enemy against an ally.",
            "***Intercept.*** Take a hit meant for another ally from adjacent enemy. Resistance to that damage.",
        ],
    },
    "Soldier": {
        "actions": [
            "***Reposition (roll 4-6).*** Make an attack, and shove an enemy 10 feet (4), pull 10 feet (5), "
            "or shift 5 feet (6). DC {save_dc} Str save to resist."
        ]
    },
    "Skirmisher": {
        "special_abilities": [
            "***Evasion.*** Half damage on a failed Dex save, no damage on a success.",
        ],
        "bonus_actions": [
            "***Nimble Escape.*** Disengage as a bonus action.",
        ]
    },
    "Bard": {
        "bonus_actions": [
            "***Inspire Courage***. The bard gives an ally advantage on their next attack roll."
        ],
        "reactions": [
            "***Inspire Heroism***. When an ally would make a saving throw, the bard gives them advantage."
        ]
    },
    "Yendan": {
        "special_abilities": [
            "***All Hands On Deck!*** On initiative count 20, after the first round, 2-4 pirates emerge from below "
            "decks, or swing in from the rigging.",
        ],
        "bonus_actions": [
            "***Avast Ye Scurvy Dogs!*** The captain barks an order and one pirate gets to make a basic attack.",
        ],
        "reactions": [
            "***Eek!*** When an enemy would hit Yendan with an attack, he swaps places with an adjacent pirate, "
            "causing them to take the hit instead. He can then move up to his speed."
        ]
    },
    "Mama Moogle": {
        "special_abilities": [
            "***Fly My Pretties!*** On initiative count 20, after the first round, 1d4 - 1 (minimum 1) "
            "moogle minions appear.",
        ],
        "bonus_actions": [
            "***Kick Them In The Kupo!*** Mama Moogle commands a moogle she can see to make a weapon attack.",
        ],
        "reactions": [
            "***Eek!*** When an enemy would hit Mama Moogle with an attack, they have to make a "
            "Wisdom saving throw (DC {save_dc}) or be forced to give up their attack, as they are awestruck by Mama's "
            "magnificence."
        ]
    },
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
