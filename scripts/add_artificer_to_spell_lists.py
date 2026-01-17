import os.path
import tomllib
from glob import glob

from src.common.utils import title_to_page_name

# Parse spell names from the provided list
spell_names_raw = """
Acid Splash
Aid
Alarm
Alter Self
Animate Objects
Arcane Eye
Arcane Lock
Arcane Vigor
Bigby's Hand
Blink
Blur
Circle of Power
Continual Flame
Create Food and Water
Creation
Cure Wounds
Dancing Lights
Darkvision
Detect Magic
Disguise Self
Dispel Magic
Dragon's Breath
Elemental Weapon
Elementalism
Enhance Ability
Enlarge/Reduce
Expeditious Retreat
Fabricate
Faerie Fire
False Life
Feather Fall
Fire Bolt
Fly
Freedom of Movement
Glyph of Warding
Grease
Greater Restoration
Guidance
Haste
Heat Metal
Identify
Invisibility
Jump
Leomund's Secret Chest
Lesser Restoration
Levitate
Light
Longstrider
Mage Hand
Magic Mouth
Magic Weapon
Message
Mordenkainen's Faithful Hound
Mordenkainen's Private Sanctum
Otiluke's Resilient Sphere
Poison Spray
Prestidigitation
Protection from Energy
Protection from Poison
Purify Food and Drink
Ray of Frost
Resistance
Revivify
Rope Trick
Sanctuary
See Invisibility
Shocking Grasp
Spare the Dying
Spider Climb
Stone Shape
Stoneskin
Summon Construct
Thorn Whip
Thunderclap
True Strike
Wall of Stone
Water Breathing
Water Walk
Web
"""

spell_names = [name.strip() for name in spell_names_raw.strip().split('\n')]

print(f"\nTotal spells to modify: {len(spell_names)}")

# Process each spell
modified_count = 0
for spell_name in spell_names:
    filename = title_to_page_name(spell_name)
    path = f"../data/dnd/spell/{filename}.toml"

    if not os.path.isfile(path):
        print(f"⚠️  Not found: {spell_name}")
        continue

    with open(path) as f:
        text = f.read()

    text = text.replace("spell_lists = [", 'spell_lists = ["Artificer", ')

    with open(path, 'w') as f:
        f.write(text)
    modified_count += 1


print(f"\nTotal spells modified: {modified_count}")
