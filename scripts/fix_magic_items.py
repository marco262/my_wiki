import glob
import os
import re

from src.common.utils import title_to_page_name

BASE_DIR = "../data/dnd/equipment/magic-items"

for filepath in glob.glob(os.path.join(BASE_DIR, "*.toml")):
    with open(filepath, "rb") as f:
        old_file_contents = f.read().decode("utf-8").replace("\r", "")
    
    file_contents = old_file_contents
    
    if "subtype = " not in file_contents:
        file_contents = re.sub(r"type = (.*)", r'type = \1\nsubtype = ""', file_contents)
    
    if "classes = " not in file_contents:
        file_contents = re.sub(r"attunement = (.*)", r'attunement = \1\nclasses = []', file_contents)
    
    if file_contents != old_file_contents:
        print(filepath)
        with open(filepath, 'wb') as f:
            f.write(file_contents.encode("utf-8"))
