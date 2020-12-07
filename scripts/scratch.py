import os

from src.dnd.utils import get_magic_item_table

os.chdir("..")

for k, v in get_magic_item_table("Minor", "Uncommon").items():
    print(k, v)
