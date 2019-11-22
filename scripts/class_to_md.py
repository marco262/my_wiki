import os
import re
from collections import OrderedDict, defaultdict
from glob import glob
from os.path import basename
from re import search, sub

import toml


def main():
    for directory in ["advancement", "background", "equipment", "general", "monster", "race"]:
        g_path = f"../data/{directory}/{directory}_*.txt"
        print(g_path)
        for path in glob(g_path):
            new_name = os.path.splitext(path.replace(f"{directory}_", r""))[0] + ".md"
            print(new_name)
            os.rename(path, new_name)


main()