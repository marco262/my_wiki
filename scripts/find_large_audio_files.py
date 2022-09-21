from pathlib import Path

import re

import os
from glob import glob

os.chdir("../media/audio/curse_of_strahd")


def human_readable_size(size, decimal_places=2):
    for unit in ['B', 'KiB', 'MiB', 'GiB', 'TiB', 'PiB']:
        if size < 1024.0 or unit == 'PiB':
            break
        size /= 1024.0
    return f"{size:.{decimal_places}f} {unit}"


for filepath in glob("*.mp3"):
    file_size = Path(filepath).stat().st_size
    if file_size > 1e6:
        # print("{} ({})".format(filepath, human_readable_size(file_size)))
        print(filepath)
