from glob import glob
from os.path import basename
from re import search

for path in glob("../data/spell/*"):
    with open(path) as f:
        contents = f.read()
    if 'material = ""' in contents:
        print(path)
        break