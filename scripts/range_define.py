import re
from collections import OrderedDict, defaultdict
from glob import glob
from os.path import basename
from re import search, sub

import toml

repl = '''range = {r}
target = ""
origin = ""
shape = ""
size = ""
'''

for path in glob("../data/spell/*"):
    with open(path) as f:
        text = f.read()
    if not 'shape = ""' in text:
        continue
    d = toml.loads(text)
    if d["range"] == "Touch":
        # text = text.replace('target = ""', 'target = "Self"')
        text = text.replace('origin = ""', 'origin = "Touch"')
        text = text.replace('shape = ""', 'shape = "None"')
        text = text.replace('size = ""', 'size = "None"')
        print(path)
        with open(path, "w") as f:
            f.write(text)