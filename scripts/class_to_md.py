import os
import re
from collections import OrderedDict, defaultdict
from glob import glob
from os.path import basename
from re import search, sub

import toml

for path in glob("../data/class/*.md"):
    new_name = path.replace(r"\class_", r"\\")
    print(new_name)
    os.rename(path, new_name)
