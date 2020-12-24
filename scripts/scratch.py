import os
from glob import glob

os.chdir("..")

for filepath in glob("data/dnd/subclass/*"):
    with open(filepath) as f:
        if not f.readline().startswith("[[breadcrumb"):
            print(filepath)
