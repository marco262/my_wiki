import os

from data.dnd.enums import casting_times, durations
from src.dnd.endpoints import load_spells

print(os.getcwd())
print(os.chdir(".."))
print(os.getcwd())

spells = load_spells()

print("Spells with unhandled casting times:")
for k, v in spells.items():
    for t in casting_times:
        if t in v["casting_time"]:
            break
    else:
        print(v["title"], v["casting_time"])

print("")
print("Spells with unhandled durations:")
for k, v in spells.items():
    for t in durations:
        if t in v["duration"]:
            break
    else:
        print(v["title"], v["duration"])
