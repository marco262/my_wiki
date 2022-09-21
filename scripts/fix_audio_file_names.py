import re

import os
from glob import glob

os.chdir("../media/audio/curse_of_strahd")

for filepath in glob("*.mp3"):
    # Replace unallowed characters with spaces
    filename = re.sub(r"[^A-Za-z0-9_'.&]", " ", filepath)
    # Collapse multiple spaces to one
    filename = re.sub(r" +", " ", filename)
    filename = filename.replace("D D", "D&D")
    os.rename(filepath, filename)
