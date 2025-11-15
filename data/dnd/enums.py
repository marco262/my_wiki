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

tooltips = {
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
    # Simple Weapons
    "dagger": {
        "href": "/dnd/general/Equipment#dagger",
        "content": "",
    },
    "handaxe": {
        "href": "/dnd/general/Equipment#handaxe",
        "content": "",
    },
    "mace": {
        "href": "/dnd/general/Equipment#mace",
        "content": "",
    },
    "quarterstaff": {
        "href": "/dnd/general/Equipment#quarterstaff",
        "content": "",
    },
    "sap": {
        "href": "/dnd/general/Equipment#sap",
        "content": "",
    },
    "sickle": {
        "href": "/dnd/general/Equipment#sickle",
        "content": "",
    },
    "spear": {
        "href": "/dnd/general/Equipment#spear",
        "content": "",
    },
    # Martial Weapons
    "flail": {
        "href": "/dnd/general/Equipment#flail",
        "content": "",
    },
    "greataxe": {
        "href": "/dnd/general/Equipment#greataxe",
        "content": "",
    },
    "greatsword": {
        "href": "/dnd/general/Equipment#greatsword",
        "content": "",
    },
    "javelin": {
        "href": "/dnd/general/Equipment#javelin",
        "content": "",
    },
    "longsword": {
        "href": "/dnd/general/Equipment#longsword",
        "content": "",
    },
    "scimitar": {
        "href": "/dnd/general/Equipment#scimitar",
        "content": "",
    },
    "shortsword": {
        "href": "/dnd/general/Equipment#shortsword",
        "content": "",
    },
    "longbow": {
        "href": "/dnd/general/Equipment#longbow",
        "content": "",
    },
    "shortbow": {
        "href": "/dnd/general/Equipment#shortbow",
        "content": "",
    },
    # Armor
    "leather armor": {
        "href": "/dnd/general/Equipment#leather-armor",
        "content": "",
    },
    "studded leather armor": {
        "href": "/dnd/general/Equipment#studded-leather-armor",
        "content": "",
    },
    "chain shirt": {
        "href": "/dnd/general/Equipment#chain-shirt",
        "content": "",
    },
    "chain mail": {
        "href": "/dnd/general/Equipment#chain-mail",
        "content": "",
    },
    "shield": {
        "href": "/dnd/general/Equipment#shield",
        "content": "",
    },
    # Packs
    "burglar's pack": {
        "href": "/dnd/general/Equipment#burglar-s-pack",
        "content": "",
    },
    "dungeoneer's pack": {
        "href": "/dnd/general/Equipment#dungeoneer-s-pack",
        "content": "",
    },
    "entertainer's pack": {
        "href": "/dnd/general/Equipment#entertainer-s-pack",
        "content": "",
    },
    "explorer's pack": {
        "href": "/dnd/general/Equipment#explorer-s-pack",
        "content": "",
    },
    "priest's pack": {
        "href": "/dnd/general/Equipment#priest-s-pack",
        "content": "",
    },
    "scholar's pack": {
        "href": "/dnd/general/Equipment#scholar-s-pack",
        "content": "",
    },
    # Items
    "arcane focus": {
        "href": "/dnd/general/Equipment#arcane-focus",
        "content": "",
    },
    "arrow": {
        "href": "/dnd/general/Equipment#arrow",
        "content": "",
    },
    "disguise kit": {
        "href": "/dnd/general/Equipment#disguise-kit",
        "content": "",
    },
    "druidic focus": {
        "href": "/dnd/general/Equipment#druidic-focus",
        "content": "",
    },
    "holy symbol": {
        "href": "/dnd/general/Equipment#holy-symbol",
        "content": "",
    },
    "herbalism kit": {
        "href": "/dnd/general/Equipment#herbalism-kit",
        "content": "",
    },
    "poisoner's kit": {
        "href": "/dnd/general/Equipment#poisoner-s-kit",
        "content": "",
    },
    "quiver": {
        "href": "/dnd/general/Equipment#quiver",
        "content": "",
    },
    "sprig of mistletoe": {
        "href": "/dnd/general/Equipment#sprig-of-mistletoe",
        "content": "",
    },
    "thieves' tools": {
        "href": "/dnd/general/Equipment#thieves-tools",
        "content": "",
    },
    # Magic Items
    "spell scroll": {
        "href": "/dnd/general/Equipment#spell-scroll",
        "content": "",
    },
    # Weapon Properties
    "finesse": {
        "href": "/dnd/general/Equipment#finesse",
        "content": "",
    },
    "heavy": {
        "href": "/dnd/general/Equipment#heavy",
        "content": "",
    },
    "light": {
        "href": "/dnd/general/Equipment#light",
        "content": "",
    },
    "push": {
        "href": "/dnd/general/Equipment#push",
        "content": "",
    },
    "slow": {
        "href": "/dnd/general/Equipment#slow",
        "content": "",
    },
    "thrown": {
        "href": "/dnd/general/Equipment#thrown",
        "content": "",
    },
    "topple": {
        "href": "/dnd/general/Equipment#topple",
        "content": "",
    },
    "versatile": {
        "href": "/dnd/general/Equipment#versatile",
        "content": "",
    },
    "vex": {
        "href": "/dnd/general/Equipment#vex",
        "content": "",
    },
}
