import os
from collections import defaultdict
from glob import glob
import re

import toml

CR = "15"

while not os.getcwd().endswith("my_wiki"):
    os.chdir("..")

multi_attack_numbers = defaultdict(int)
total = 0

for filepath in glob("data/dnd/monster/*.toml"):
    with open(filepath) as f:
        t = toml.load(f)
    # if "humanoid" not in t["type"]:
    #     continue
    if not t["challenge"].split(" ")[0] == str(CR):
        continue
    total += 1
    if "Multiattack" in t["actions"]:
        m = re.search("makes ((.*?) (attacks|strikes))", t["actions"])
        if not m:
            if "attacks twice" in t["actions"]:
                match = "makes two attacks"
            else:
                print(t["actions"])
                raise Exception
        else:
            match = m.group(1)
        print(f"{t['name']} ({match})")
        for num in ["two", "three", "four", "five"]:
            if num in match:
                multi_attack_numbers[num] += 1
                break
        else:
            if "makes as many" in t["actions"]:
                continue
            print(f"FUCK! {t['actions']}")
            raise Exception
    else:
        print(f"{t['name']}")

print("")
print(f"Total: {sum(multi_attack_numbers.values())} / {total}")
for num in ["two", "three", "four", "five"]:
    if num in multi_attack_numbers:
        print(f"  {num}: {multi_attack_numbers[num]}")
