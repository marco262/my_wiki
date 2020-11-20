from collections import defaultdict

import os

from src.common.utils import ordinal
from src.dnd.endpoints import load_spells

spells = defaultdict(lambda: defaultdict(list))
os.chdir("..")
print(os.getcwd())
spells_dict = load_spells()

for name, s in spells_dict.items():
    if "classes_ua" in s:
        for dnd_class in s["classes_ua"]:
            spells[dnd_class][s["level"]].append(s["title"])

print("")
for dnd_class, d in sorted(spells.items(), key=lambda x: x[0]):
    print(f"## {dnd_class.title()}")
    print("")
    for level, spell_list in sorted(d.items(), key=lambda x: x[0]):
        print(ordinal(level))
        for s in spell_list:
            print(s)
        print("")
    print("")
