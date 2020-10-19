import os
import re
from collections import OrderedDict
from time import sleep

import requests
import toml

from src.common.utils import title_to_page_name

os.makedirs("../data/dnd/equipment/magic-items", exist_ok=True)

with open("magic_items.html") as f:
    for line in f.readlines():
        m = re.match(r"<tr><td>(.*?)</td><td>(.*?)</td><td>(.*?)</td><td>(.*?)</td><td>(.*?)</td><td>(.*?)</td></tr>", line)
        name = m.group(1)
        filename = title_to_page_name(name) + ".toml"
        filepath = os.path.join("../data/dnd/equipment/magic-items", filename)
        print(name)
        if os.path.isfile(filepath):
            continue
        # Get values
        d = OrderedDict([
            ("name", name),
            ("type", m.group(2)),
            ("rarity", m.group(3)),
            ("attunement", True if m.group(4) else False),
            ("notes", m.group(5)),
            ("source", m.group(6))
        ])
        # Get description
        r = requests.get("https://donjon.bin.sh/5e/magic_items/rpc.cgi?name=" + name)
        card = r.json()["card"]
        m = re.match(r'<div><h2>.*?</h2>\n<p class="type">.*?</p>\n<div class="description">(.*?)</div>', card)
        if m is None:
            if "<p>No description available.</p>" in card:
                d["description"] = "No description available."
            else:
                print(card)
                break
        else:
            d["description"] = m.group(1)
        # Save file
        with open(filepath, 'w') as out_f:
            toml.dump(d, out_f)
        sleep(1)
