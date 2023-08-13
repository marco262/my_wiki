import os

from data.dnd.enums import classes, magic_item_types, magic_item_rarities, magic_item_sources
from src.dnd.utils import load_magic_items

if os.path.basename(os.getcwd()) == "scripts":
    os.chdir("..")
print(os.getcwd())

magic_items = load_magic_items()

items_with_missing_classes = []
items_with_missing_type = []
items_with_missing_rarity_type = []
items_with_missing_rarity = []
items_with_missing_source = []

for name, magic_item in magic_items.items():
    # Classes
    for c in magic_item["classes"]:
        if c not in classes:
            items_with_missing_classes.append(magic_item)
    # Type
    if magic_item["type"] not in magic_item_types:
        items_with_missing_type.append(magic_item)
    # Rarity type
    if magic_item["rarity_type"] not in ["Minor", "Major"]:
        items_with_missing_rarity_type.append(magic_item)
    # Type
    if magic_item["rarity"] not in magic_item_rarities:
        items_with_missing_rarity.append(magic_item)
    # Source
    for t in magic_item_sources:
        if t in magic_item["source"]:
            break
    else:
        items_with_missing_source.append(magic_item)

if items_with_missing_type:
    print("\nMagic items with missing type:")
    for s in items_with_missing_type:
        print(f"{s['name']}: {s['type']}")
if items_with_missing_rarity_type:
    print("\nMagic items with missing rarity type:")
    for s in items_with_missing_rarity_type:
        print(f"{s['name']}: {s['rarity_type']}")
if items_with_missing_rarity:
    print("\nMagic items with missing rarity:")
    for s in items_with_missing_rarity:
        print(f"{s['name']}: {s['rarity']}")
if items_with_missing_classes:
    print("\nMagic items with missing classes:")
    for s in items_with_missing_classes:
        print(f"{s['name']}: {s['classes']}")
if items_with_missing_source:
    print("\nMagic items with missing source:")
    for s in items_with_missing_source:
        print(f"{s['name']}: {s['source']}")
