import os

from data.dnd.enums import casting_times, durations
from src.dnd.endpoints import load_spells

print(os.getcwd())
print(os.chdir(".."))
print(os.getcwd())

spells = load_spells()

con_consistent = []
con_inconsistent = []
no_con_consistent = []
no_con_inconsistent = []
for k, spell in spells.items():
    if spell["concentration_spell"]:
        if "Concentration" in spell["duration"]:
            con_consistent.append(spell)
        else:
            con_inconsistent.append(spell)
    else:
        if "Concentration" in spell["duration"]:
            no_con_inconsistent.append(spell)
        else:
            no_con_consistent.append(spell)

print("Con consistent: {}".format(len(con_consistent)))
print("Con inconsistent: {}".format(len(con_inconsistent)))
print("No con consistent: {}".format(len(no_con_consistent)))
print("No con inconsistent: {}".format(len(no_con_inconsistent)))

for spell in con_inconsistent:
    print(spell["title"])

for spell in no_con_inconsistent:
    print(spell["title"])
