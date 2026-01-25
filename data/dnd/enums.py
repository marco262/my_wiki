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
    "2 rounds",
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
    "40 feet",
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
    "Eberron: Forge of the Artificer",
    "Homebrew",
    "Champion's Ascension",
]

source_acronyms = {
    "Player's Handbook": "PHB",
    "Dungeon Master's Guide": "DMG",
    "Eberron: Forge of the Artificer": "EFotA",
    "Homebrew": "Home",
    "Waterdeep: Dragon Heist": "W:DH",
    "Player's Handbook Playtest 7": "PHP7",
    "Champion's Ascension": "CA",
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
    "spellcasting focus":{
        "href": "/dnd/general/Spellcasting Rules##material-m",
        "content": "<p>If a spell doesn't consume its materials and doesn't specify a cost for them, the spellcaster can substitute a Spellcasting Focus if the caster has a feature that allows that substitution. To use a Spellcasting Focus, you must hold it unless its description says otherwise. The type of spellcasting focus you can use depends on your class.</p>",
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
    "spell scroll": {
        "href": "/dnd/general/Equipment",
        "content": ""
    },
}
