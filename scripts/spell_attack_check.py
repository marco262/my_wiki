from src.dnd.endpoints import load_spells

spells = load_spells()

spell_levels = ["cantrip", "1"]

for spell in spells.values():
    if spell["level"] in spell_levels and ("sorcerer" in spell["classes"] or "sorcerer" in spell.get("classes_ua", [])):
        if "spell attack" in spell["description"]:
            print(spell["title"])
