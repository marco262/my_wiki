import os

from data.dnd.enums import spell_classes, spell_levels, schools, casting_times, ranges, durations, sources
from src.dnd.utils import load_spells

if os.path.basename(os.getcwd()) == "scripts":
    os.chdir("..")
print(os.getcwd())

spells = load_spells()

spells_with_missing_classes = []
spells_with_missing_level = []
spells_with_missing_school = []
spells_with_missing_casting_time = []
spells_with_missing_range = []
spells_with_missing_duration = []
spells_with_missing_source = []

for title, spell in spells.items():
    # Classes
    for c in spell["classes"]:
        if c not in spell_classes:
            spells_with_missing_classes.append(spell)
    # Level
    if spell["level"] not in spell_levels:
        spells_with_missing_level.append(spell)
    # School
    if spell["school"] not in schools:
        spells_with_missing_school.append(spell)
    # Casting time
    for t in casting_times:
        if t in spell["casting_time"]:
            break
    else:
        spells_with_missing_casting_time.append(spell)
    # Range
    for t in ranges:
        if t in spell["range"]:
            break
    else:
        spells_with_missing_range.append(spell)
    # Duration
    for t in durations:
        if t in spell["duration"]:
            break
    else:
        spells_with_missing_duration.append(spell)
    # Source
    for t in sources:
        if t in spell["source"]:
            break
    else:
        spells_with_missing_source.append(spell)

if spells_with_missing_classes:
    print("\nSpells with missing classes:")
    for s in spells_with_missing_classes:
        print(f"{s['title']}: {s['classes']}")
if spells_with_missing_level:
    print("\nSpells with missing level:")
    for s in spells_with_missing_level:
        print(f"{s['title']}: {s['level']}")
if spells_with_missing_school:
    print("\nSpells with missing school:")
    for s in spells_with_missing_school:
        print(f"{s['title']}: {s['school']}")
if spells_with_missing_casting_time:
    print("\nSpells with missing casting time:")
    for s in spells_with_missing_casting_time:
        print(f"{s['title']}: {s['casting_time']}")
if spells_with_missing_range:
    print("\nSpells with missing range:")
    for s in spells_with_missing_range:
        print(f"{s['title']}: {s['range']}")
if spells_with_missing_duration:
    print("\nSpells with missing duration:")
    for s in spells_with_missing_duration:
        print(f"{s['title']}: {s['duration']}")
if spells_with_missing_source:
    print("\nSpells with missing source:")
    for s in spells_with_missing_source:
        print(f"{s['title']}: {s['source']}")
