from distutils.sysconfig import customize_compiler

classes = [
    "Artificer",
    "Barbarian",
    "Bard",
    "Cleric",
    "Druid",
    "Fighter",
    "Monk",
    "Paladin",
    "Ranger",
    "Rogue",
    "Sorcerer",
    "Warlock",
    "Wizard",
]

spell_classes = [
    "Artificer",
    "Bard",
    "Cleric",
    "Druid",
    "Paladin",
    "Ranger",
    "Sorcerer",
    "Warlock",
    "Wizard",
]

spell_levels = [
    "0",
    "1",
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8",
    "9"
]

schools = [
    "Abjuration",
    "Conjuration",
    "Divination",
    "Evocation",
    "Enchantment",
    "Illusion",
    "Necromancy",
    "Transmutation"
]

casting_times = [
    "Action",
    "Bonus Action",
    "Reaction",
    "1 minute",
    "10 minutes",
    "1 hour",
    "8 hours", 
    "12 hours", 
    "24 hours"
]

durations = [
    "Instantaneous", 
    "1 round",
    "6 rounds",
    "1 minute",
    "10 minutes",
    "1 hour",
    "2 hours",
    "6 hours",
    "8 hours",
    "24 hours",
    "1 day",
    "7 days",
    "10 days",
    "30 days",
    "Until dispelled",
    "Special"
]

ranges = [
    "Self",
    "Touch",
    "5 feet",
    "10 feet",
    "15 feet",
    "20 feet",
    "30 feet",
    "60 feet",
    "90 feet",
    "100 feet",
    "120 feet",
    "150 feet",
    "300 feet",
    "500 feet",
    "1 mile",
    "5 miles",
    "500 miles",
    "Sight",
    "Unlimited",
    "Special"
]

shapes = [
    "Line",
    "Cone",
    "Cube",
    "Sphere",
    "Hemisphere"
]

sources = [
    "Player's Handbook",
    "Elemental Evil",
    "Xanathar's Guide to Everything",
    "Lost Laboratory of Kwalish",
    "Explorer's Guide to Wildemount",
    "Tasha's Cauldron of Everything",
    "Guildmaster's Guide to Ravnica",
    "Homebrew",
    "Cleric and Revised Species",
    "Druid and Paladin",
    "Player's Handbook Playtest 6",
    "Player's Handbook Playtest 7",
    "Bastions and Cantrips",
    "Player's Handbook Playtest 8",
]

source_acronyms = {
    "Player's Handbook": "PHB",
    "Dungeon Master's Guide": "DMG",
    "Elemental Evil": "EE",
    "Sword Coast Adventurer's Guide": "SCAG",
    "Xanathar's Guide to Everything": "XGtE",
    "Lost Laboratory of Kwalish": "LLoK",
    "Explorer's Guide to Wildemount": "EGtW",
    "Tasha's Cauldron of Everything": "TCoE",
    "Waterdeep: Dragon Heist": "WDH",
    "Guildmaster's Guide to Ravnica": "GGR",
    "Homebrew": "Home",
    "Cleric and Revised Species": "CaRS",
    "Druid and Paladin": "DaP",
    "Player's Handbook Playtest 6": "PHP6",
    "Player's Handbook Playtest 7": "PHP7",
    "Bastions and Cantrips": "BaC",
    "Player's Handbook Playtest 8": "PHP8",
}

ability_scores = [
    "Strength",
    "Dexterity",
    "Constitution",
    "Intelligence",
    "Wisdom",
    "Charisma"
]

skills = [
    ("Acrobatics", "Dexterity"),
    ("Animal Handling", "Wisdom"),
    ("Arcana", "Intelligence"),
    ("Athletics", "Strength"),
    ("Deception", "Charisma"),
    ("History", "Intelligence"),
    ("Insight", "Wisdom"),
    ("Intimidation", "Charisma"),
    ("Investigation", "Intelligence"),
    ("Medicine", "Wisdom"),
    ("Nature", "Intelligence"),
    ("Perception", "Wisdom"),
    ("Performance", "Charisma"),
    ("Persuasion", "Charisma"),
    ("Religion", "Intelligence"),
    ("Sleight of Hand", "Dexterity"),
    ("Stealth", "Dexterity"),
    ("Survival", "Wisdom")
]

magic_item_types = [
    "Armor",
    "Potion",
    "Ring",
    "Rod",
    "Scroll",
    "Staff",
    "Wand",
    "Weapon",
    "Wondrous Item"
]

magic_item_rarities = [
    "Common",
    "Uncommon",
    "Rare",
    "Very Rare",
    "Legendary",
    "Artifact"
]

magic_item_sources = [
    "Dungeon Master's Guide",
    "Xanathar's Guide to Everything",
    "Tasha's Cauldron of Everything",
    "Waterdeep: Dragon Heist",
    "Homebrew"
]

custom_tooltips = {
    "acrobatics": {
        "href": "/dnd/general/Playing the Game#skill-list",
        "content": "<p>Dexterity (Acrobatics) allows you to stay on your feet in a tricky situation, or perform an acrobatic stunt.</p>",
    },
    "animal handling": {
        "href": "/dnd/general/Playing the Game#skill-list",
        "content": "<p>Wisdom (Animal Handling) allows you to calm or train an animal, or get an animal to behave in a certain way.</p>",
    },
    "arcana": {
        "href": "/dnd/general/Playing the Game#skill-list",
        "content": "<p>Intelligence (Arcana) allows you to recall lore about spells, magic items, and the planes of existence.</p>",
    },
    "athletics": {
        "href": "/dnd/general/Playing the Game#skill-list",
        "content": "<p>Strength (Athletics) allows you to jump farther than normal, stay afloat in rough water, or break something.</p>",
    },
    "deception": {
        "href": "/dnd/general/Playing the Game#skill-list",
        "content": "<p>Charisma (Deception) allows you to tell a convincing lie, or wear a disguise convincingly.</p>",
    },
    "history": {
        "href": "/dnd/general/Playing the Game#skill-list",
        "content": "<p>Intelligence (History) allows you to recall lore about historical events, people, nations, and cultures.</p>",
    },
    "insight": {
        "href": "/dnd/general/Playing the Game#skill-list",
        "content": "<p>Wisdom (Insight) allows you to discern a person's mood and intentions.</p>",
    },
    "intimidation": {
        "href": "/dnd/general/Playing the Game#skill-list",
        "content": "<p>Charisma (Intimidation) allows you to awe or threaten someone into doing what you want.</p>",
    },
    "investigation": {
        "href": "/dnd/general/Playing the Game#skill-list",
        "content": "<p>Intelligence (Investigation) allows you to find obscure information in books, or deduce how something works.</p>",
    },
    "medicine": {
        "href": "/dnd/general/Playing the Game#skill-list",
        "content": "<p>Wisdom (Medicine) allows you to diagnose an illness, or determine what killed the recently slain.</p>",
    },
    "nature": {
        "href": "/dnd/general/Playing the Game#skill-list",
        "content": "<p>Intelligence (Nature) allows you to recall lore about terrain, plants, animals, and weather.</p>",
    },
    "perception": {
        "href": "/dnd/general/Playing the Game#skill-list",
        "content": "<p>Wisdom (Perception) allows you to use a combination of senses to notice something that's easy to miss.</p>",
    },
    "performance": {
        "href": "/dnd/general/Playing the Game#skill-list",
        "content": "<p>Charisma (Performance) allows you to act, tell a story, perform music, or dance.</p>",
    },
    "persuasion": {
        "href": "/dnd/general/Playing the Game#skill-list",
        "content": "<p>Charisma (Persuasion) allows you to honestly and graciously convince someone of something.</p>",
    },
    "religion": {
        "href": "/dnd/general/Playing the Game#skill-list",
        "content": "<p>Intelligence (Religion) allows you to recall lore about gods, religious rituals, and holy symbols.</p>",
    },
    "sleight of hand": {
        "href": "/dnd/general/Playing the Game#skill-list",
        "content": "<p>Dexterity (Sleight of Hand) allows you to pick a pocket, conceal a handheld object, or perform legerdemain.</p>",
    },
    "stealth": {
        "href": "/dnd/general/Playing the Game#skill-list",
        "content": "<p>Dexterity (Stealth) allows you to escape notice by moving quietly and hiding behind things.</p>",
    },
    "survival": {
        "href": "/dnd/general/Playing the Game#skill-list",
        "content": "<p>Wisdom (Survival) allows you to follow tracks, forage, find a trail, or avoid natural hazards.</p>",
    },
    "half cover": {
        "href": "/dnd/general/Rules Glossary#cover",
        "content": "<p>Half Cover gives you +2 bonus to AC and Dexterity saving throws.</p>",
    },
    "three-quarters cover": {
        "href": "/dnd/general/Rules Glossary#cover",
        "content": "<p>Three-Quarters Cover gives you +5 bonus to AC and Dexterity saving throws.</p>",
    },
    "total cover": {
        "href": "/dnd/general/Rules Glossary#cover",
        "content": "<p>Total Cover means you can't be targeted directly, by attacks or spells that require a target.</p>",
    },
    "arrows": {
        "href": "/dnd/general/Equipment#ammunition",
        "content": "<p>Arrows are used with a weapon that has the ammunition property to make a ranged attack. Each time you attack with the weapon, you expend one piece of ammunition. Drawing the ammunition from a quiver, case, or other container is part of the attack (you need a free hand to load a one-handed weapon). At the end of the battle, you can recover half your expended ammunition by taking a minute to search the battlefield.</p>"
    },
    "bolts": {
        "href": "/dnd/general/Equipment#ammunition",
        "content": "<p>Crossbow bolts are used with a weapon that has the ammunition property to make a ranged attack. Each time you attack with the weapon, you expend one piece of ammunition. Drawing the ammunition from a quiver, case, or other container is part of the attack (you need a free hand to load a one-handed weapon). At the end of the battle, you can recover half your expended ammunition by taking a minute to search the battlefield.</p>"
    },
    "bullets, firearm": {
        "href": "/dnd/general/Equipment#ammunition",
        "content": "<p>Firearm Bullets are destroyed upon use in a modern firearm.</p>"
    },
    "bullets, sling": {
        "href": "/dnd/general/Equipment#ammunition",
        "content": "<p>Sling bullets are used with a weapon that has the ammunition property to make a ranged attack. Each time you attack with the weapon, you expend one piece of ammunition. Drawing the ammunition from a quiver, case, or other container is part of the attack (you need a free hand to load a one-handed weapon). At the end of the battle, you can recover half your expended ammunition by taking a minute to search the battlefield.</p>"
    },
    "needles": {
        "href": "/dnd/general/Equipment#ammunition",
        "content": "<p>Blowgun needles are used with a weapon that has the ammunition property to make a ranged attack. Each time you attack with the weapon, you expend one piece of ammunition. Drawing the ammunition from a quiver, case, or other container is part of the attack (you need a free hand to load a one-handed weapon). At the end of the battle, you can recover half your expended ammunition by taking a minute to search the battlefield.</p>"
    },
    "dice": {
        "href": "/dnd/general/Equipment#gaming-set",
        "content": "<p><strong>Ability:</strong> Wisdom<br/>\n<strong>Utilize:</strong> Discern whether someone is cheating (DC 10), or win the game (DC 20)</p>"
    },
    "dragonchess": {
        "href": "/dnd/general/Equipment#gaming-set",
        "content": "<p><strong>Ability:</strong> Wisdom<br/>\n<strong>Utilize:</strong> Discern whether someone is cheating (DC 10), or win the game (DC 20)</p>"
    },
    "playing cards": {
        "href": "/dnd/general/Equipment#gaming-set",
        "content": "<p><strong>Ability:</strong> Wisdom<br/>\n<strong>Utilize:</strong> Discern whether someone is cheating (DC 10), or win the game (DC 20)</p>"
    },
    "three-dragon ante": {
        "href": "/dnd/general/Equipment#gaming-set",
        "content": "<p><strong>Ability:</strong> Wisdom<br/>\n<strong>Utilize:</strong> Discern whether someone is cheating (DC 10), or win the game (DC 20)</p>"
    },
    "bagpipes": {
        "href": "/dnd/general/Equipment#musical-instrument",
        "content": "<p><strong>Ability:</strong> Wisdom<br/>\n<strong>Utilize:</strong> Discern whether someone is cheating (DC 10), or win the game (DC 20)</p>"
    },
    "drum": {
        "href": "/dnd/general/Equipment#musical-instrument",
        "content": "<p><strong>Ability:</strong> Wisdom<br/>\n<strong>Utilize:</strong> Discern whether someone is cheating (DC 10), or win the game (DC 20)</p>"
    },
    "dulcimer": {
        "href": "/dnd/general/Equipment#musical-instrument",
        "content": "<p><strong>Ability:</strong> Wisdom<br/>\n<strong>Utilize:</strong> Discern whether someone is cheating (DC 10), or win the game (DC 20)</p>"
    },
    "flute": {
        "href": "/dnd/general/Equipment#musical-instrument",
        "content": "<p><strong>Ability:</strong> Wisdom<br/>\n<strong>Utilize:</strong> Discern whether someone is cheating (DC 10), or win the game (DC 20)</p>"
    },
    "horn": {
        "href": "/dnd/general/Equipment#musical-instrument",
        "content": "<p><strong>Ability:</strong> Wisdom<br/>\n<strong>Utilize:</strong> Discern whether someone is cheating (DC 10), or win the game (DC 20)</p>"
    },
    "lute": {
        "href": "/dnd/general/Equipment#musical-instrument",
        "content": "<p><strong>Ability:</strong> Wisdom<br/>\n<strong>Utilize:</strong> Discern whether someone is cheating (DC 10), or win the game (DC 20)</p>"
    },
    "lyre": {
        "href": "/dnd/general/Equipment#musical-instrument",
        "content": "<p><strong>Ability:</strong> Wisdom<br/>\n<strong>Utilize:</strong> Discern whether someone is cheating (DC 10), or win the game (DC 20)</p>"
    },
    "pan flute": {
        "href": "/dnd/general/Equipment#musical-instrument",
        "content": "<p><strong>Ability:</strong> Wisdom<br/>\n<strong>Utilize:</strong> Discern whether someone is cheating (DC 10), or win the game (DC 20)</p>"
    },
    "shawm": {
        "href": "/dnd/general/Equipment#musical-instrument",
        "content": "<p><strong>Ability:</strong> Wisdom<br/>\n<strong>Utilize:</strong> Discern whether someone is cheating (DC 10), or win the game (DC 20)</p>"
    },
    "viol": {
        "href": "/dnd/general/Equipment#musical-instrument",
        "content": "<p><strong>Ability:</strong> Wisdom<br/>\n<strong>Utilize:</strong> Discern whether someone is cheating (DC 10), or win the game (DC 20)</p>"
    },
    "ring of feather falling": {
        "href": "/dnd/general/Equipment",
        "content": ""
    },
    "ring of swimming": {
        "href": "/dnd/general/Equipment",
        "content": ""
    },
    "ring of protection": {
        "href": "/dnd/general/Equipment",
        "content": ""
    },
    "boots of striding and springing": {
        "href": "/dnd/general/Equipment",
        "content": ""
    },
    "boots of elvenkind": {
        "href": "/dnd/general/Equipment",
        "content": ""
    },
    # Simple Weapons
    # "club": {
    #     "href": "/dnd/general/Equipment#club",
    #     "content": "",
    # },
    # "dagger": {
    #     "href": "/dnd/general/Equipment#dagger",
    #     "content": "",
    # },
    # "greatclub": {
    #     "href": "/dnd/general/Equipment#greatclub",
    #     "content": "",
    # },
    # "handaxe": {
    #     "href": "/dnd/general/Equipment#handaxe",
    #     "content": "",
    # },
    # "light hammer": {
    #     "href": "/dnd/general/Equipment#light-hammer",
    #     "content": "",
    # },
    # "mace": {
    #     "href": "/dnd/general/Equipment#mace",
    #     "content": "",
    # },
    # "quarterstaff": {
    #     "href": "/dnd/general/Equipment#quarterstaff",
    #     "content": "",
    # },
    # "sap": {
    #     "href": "/dnd/general/Equipment#sap",
    #     "content": "",
    # },
    # "sickle": {
    #     "href": "/dnd/general/Equipment#sickle",
    #     "content": "",
    # },
    # "spear": {
    #     "href": "/dnd/general/Equipment#spear",
    #     "content": "",
    # },
    # "dart": {
    #     "href": "/dnd/general/Equipment#dart",
    #     "content": "",
    # },
    # "light crossbow": {
    #     "href": "/dnd/general/Equipment#light-crossbow",
    #     "content": "",
    # },
    # "sling": {
    #     "href": "/dnd/general/Equipment#sling",
    #     "content": "",
    # },
    # # Martial Weapons
    # "battleaxe": {
    #     "href": "/dnd/general/Equipment#battleaxe",
    #     "content": "",
    # },
    # "flail": {
    #     "href": "/dnd/general/Equipment#flail",
    #     "content": "",
    # },
    # "glaive": {
    #     "href": "/dnd/general/Equipment#glaive",
    #     "content": "",
    # },
    # "greataxe": {
    #     "href": "/dnd/general/Equipment#greataxe",
    #     "content": "",
    # },
    # "greatsword": {
    #     "href": "/dnd/general/Equipment#greatsword",
    #     "content": "",
    # },
    # "javelin": {
    #     "href": "/dnd/general/Equipment#javelin",
    #     "content": "",
    # },
    # "longsword": {
    #     "href": "/dnd/general/Equipment#longsword",
    #     "content": "",
    # },
    # "scimitar": {
    #     "href": "/dnd/general/Equipment#scimitar",
    #     "content": "",
    # },
    # "shortsword": {
    #     "href": "/dnd/general/Equipment#shortsword",
    #     "content": "",
    # },
    # "longbow": {
    #     "href": "/dnd/general/Equipment#longbow",
    #     "content": "",
    # },
    # "shortbow": {
    #     "href": "/dnd/general/Equipment#shortbow",
    #     "content": "",
    # },
    # # Armor
    # "leather armor": {
    #     "href": "/dnd/general/Equipment#leather-armor",
    #     "content": "",
    # },
    # "studded leather armor": {
    #     "href": "/dnd/general/Equipment#studded-leather-armor",
    #     "content": "",
    # },
    # "chain shirt": {
    #     "href": "/dnd/general/Equipment#chain-shirt",
    #     "content": "",
    # },
    # "chain mail": {
    #     "href": "/dnd/general/Equipment#chain-mail",
    #     "content": "",
    # },
    # "shield": {
    #     "href": "/dnd/general/Equipment#shield",
    #     "content": "",
    # },
    # # Packs
    # "burglar's pack": {
    #     "href": "/dnd/general/Equipment#burglar-s-pack",
    #     "content": "",
    # },
    # "dungeoneer's pack": {
    #     "href": "/dnd/general/Equipment#dungeoneer-s-pack",
    #     "content": "",
    # },
    # "entertainer's pack": {
    #     "href": "/dnd/general/Equipment#entertainer-s-pack",
    #     "content": "",
    # },
    # "explorer's pack": {
    #     "href": "/dnd/general/Equipment#explorer-s-pack",
    #     "content": "",
    # },
    # "priest's pack": {
    #     "href": "/dnd/general/Equipment#priest-s-pack",
    #     "content": "",
    # },
    # "scholar's pack": {
    #     "href": "/dnd/general/Equipment#scholar-s-pack",
    #     "content": "",
    # },
    # # Tools
    # "calligrapher's supplies": {
    #     "href": "/dnd/general/Equipment#calligrapher-s-supplies",
    #     "content": "",
    # },
    # "carpenter's tools": {
    #     "href": "/dnd/general/Equipment#carpenter-s-tools",
    #     "content": "",
    # },
    # "cartographer's tools": {
    #     "href": "/dnd/general/Equipment#cartographer-s-tools",
    #     "content": "",
    # },
    # "disguise kit": {
    #     "href": "/dnd/general/Equipment#disguise-kit",
    #     "content": "",
    # },
    # "forgery kit": {
    #     "href": "/dnd/general/Equipment#forgery-kit",
    #     "content": "",
    # },
    # "healer's kit": {
    #     "href": "/dnd/general/Equipment#healer-s-kit",
    #     "content": "",
    # },
    # "herbalism kit": {
    #     "href": "/dnd/general/Equipment#herbalism-kit",
    #     "content": "",
    # },
    # "navigator's tools": {
    #     "href": "/dnd/general/Equipment#navigator-s-tools",
    #     "content": "",
    # },
    # "poisoner's kit": {
    #     "href": "/dnd/general/Equipment#poisoner-s-kit",
    #     "content": "",
    # },
    # "thieves' tools": {
    #     "href": "/dnd/general/Equipment#thieves-tools",
    #     "content": "",
    # },
    # # Items
    # "arcane focus": {
    #     "href": "/dnd/general/Equipment#arcane-focus",
    #     "content": "",
    # },
    # "arrow": {
    #     "href": "/dnd/general/Equipment#arrow",
    #     "content": "",
    # },
    # "basket": {
    #     "href": "/dnd/general/Equipment#basket",
    #     "content": "",
    # },
    # "ball bearings": {
    #     "href": "/dnd/general/Equipment#ball-bearings",
    #     "content": "",
    # },
    # "bedroll": {
    #     "href": "/dnd/general/Equipment#bedroll",
    #     "content": "",
    # },
    # "bell": {
    #     "href": "/dnd/general/Equipment#bucket",
    #     "content": "",
    # },
    # "block and tackle": {
    #     "href": "/dnd/general/Equipment#block-and-tackle",
    #     "content": "",
    # },
    # "bolt": {
    #     "href": "/dnd/general/Equipment#bolt",
    #     "content": "",
    # },
    # "book": {
    #     "href": "/dnd/general/Equipment#book",
    #     "content": "",
    # },
    # "bucket": {
    #     "href": "/dnd/general/Equipment#bucket",
    #     "content": "",
    # },
    # "caltrops": {
    #     "href": "/dnd/general/Equipment#caltrops",
    #     "content": "",
    # },
    # "costume": {
    #     "href": "/dnd/general/Equipment#costume",
    #     "content": "",
    # },
    # "crossbow bolt case": {
    #     "href": "/dnd/general/Equipment#crossbow-bolt-case",
    #     "content": "",
    # },
    # "crowbar": {
    #     "href": "/dnd/general/Equipment#crowbar",
    #     "content": "",
    # },
    # "druidic focus": {
    #     "href": "/dnd/general/Equipment#druidic-focus",
    #     "content": "",
    # },
    # "fine clothes": {
    #     "href": "/dnd/general/Equipment#fine-clothes",
    #     "content": "",
    # },
    # "grappling hook": {
    #     "href": "/dnd/general/Equipment#grappling-hook",
    #     "content": "",
    # },
    # "holy symbol": {
    #     "href": "/dnd/general/Equipment#holy-symbol",
    #     "content": "",
    # },
    # "hooded lantern": {
    #     "href": "/dnd/general/Equipment#hooded-lantern",
    #     "content": "",
    # },
    # "iron pot": {
    #     "href": "/dnd/general/Equipment#iron-pot",
    #     "content": "",
    # },
    # "jug": {
    #     "href": "/dnd/general/Equipment#jug",
    #     "content": "",
    # },
    # "ladder": {
    #     "href": "/dnd/general/Equipment#ladder",
    #     "content": "",
    # },
    # "lamp": {
    #     "href": "/dnd/general/Equipment#lamp",
    #     "content": "",
    # },
    # "manacles": {
    #     "href": "/dnd/general/Equipment#manacles",
    #     "content": "",
    # },
    # "map": {
    #     "href": "/dnd/general/Equipment#map",
    #     "content": "",
    # },
    # "mirror": {
    #     "href": "/dnd/general/Equipment#mirror",
    #     "content": "",
    # },
    # "net": {
    #     "href": "/dnd/general/Equipment#net",
    #     "content": "",
    # },
    # "oil": {
    #     "href": "/dnd/general/Equipment#oil",
    #     "content": "",
    # },
    # "parchment": {
    #     "href": "/dnd/general/Equipment#parchment",
    #     "content": "",
    # },
    # "perfume": {
    #     "href": "/dnd/general/Equipment#perfume",
    #     "content": "",
    # },
    # "pouch": {
    #     "href": "/dnd/general/Equipment#pouch",
    #     "content": "",
    # },
    # "quiver": {
    #     "href": "/dnd/general/Equipment#quiver",
    #     "content": "",
    # },
    # "robe": {
    #     "href": "/dnd/general/Equipment#robe",
    #     "content": "",
    # },
    # "rope": {
    #     "href": "/dnd/general/Equipment#rope",
    #     "content": "",
    # },
    # "scroll case": {
    #     "href": "/dnd/general/Equipment#scroll-case",
    #     "content": "",
    # },
    # "shovel": {
    #     "href": "/dnd/general/Equipment#shovel",
    #     "content": "",
    # },
    # "spellbook": {
    #     "href": "/dnd/general/Equipment#spellbook",
    #     "content": "",
    # },
    # "sprig of mistletoe": {
    #     "href": "/dnd/general/Equipment#sprig-of-mistletoe",
    #     "content": "",
    # },
    # "tent": {
    #     "href": "/dnd/general/Equipment#tent",
    #     "content": "",
    # },
    # "tinderbox": {
    #     "href": "/dnd/general/Equipment#tinderbox",
    #     "content": "",
    # },
    # "torch": {
    #     "href": "/dnd/general/Equipment#torch",
    #     "content": "",
    # },
    # "traveler's clothes": {
    #     "href": "/dnd/general/Equipment#traveler-s-clothes",
    #     "content": "",
    # },
    # # Magic Items
    # "spell scroll": {
    #     "href": "/dnd/general/Equipment#spell-scroll",
    #     "content": "",
    # },
    # # Weapon Properties
    # "ammunition": {
    #     "href": "/dnd/general/Equipment#ammunition",
    #     "content": "",
    # },
    # "finesse": {
    #     "href": "/dnd/general/Equipment#finesse",
    #     "content": "",
    # },
    # "graze": {
    #     "href": "/dnd/general/Equipment#graze",
    #     "content": "",
    # },
    # "heavy": {
    #     "href": "/dnd/general/Equipment#heavy",
    #     "content": "",
    # },
    # "light": {
    #     "href": "/dnd/general/Equipment#light",
    #     "content": "",
    # },
    # "loading": {
    #     "href": "/dnd/general/Equipment#loading",
    #     "content": "",
    # },
    # "nick": {
    #     "href": "/dnd/general/Equipment#nick",
    #     "content": "",
    # },
    # "push": {
    #     "href": "/dnd/general/Equipment#push",
    #     "content": "",
    # },
    # "reach": {
    #     "href": "/dnd/general/Equipment#reach",
    #     "content": "",
    # },
    # "slow": {
    #     "href": "/dnd/general/Equipment#slow",
    #     "content": "",
    # },
    # "thrown": {
    #     "href": "/dnd/general/Equipment#thrown",
    #     "content": "",
    # },
    # "topple": {
    #     "href": "/dnd/general/Equipment#topple",
    #     "content": "",
    # },
    # "two-handed": {
    #     "href": "/dnd/general/Equipment#two-handed",
    #     "content": "",
    # },
    # "versatile": {
    #     "href": "/dnd/general/Equipment#versatile",
    #     "content": "",
    # },
    # "vex": {
    #     "href": "/dnd/general/Equipment#vex",
    #     "content": "",
    # },
}
