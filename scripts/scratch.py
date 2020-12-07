import os

from src.dnd.utils import get_magic_item_table

os.chdir("..")

for k, v in get_magic_item_table("Minor", "Legendary").items():
    print(k, v)
