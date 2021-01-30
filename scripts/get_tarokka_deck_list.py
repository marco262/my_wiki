import os
from glob import glob

os.chdir("..")

final_list = []
for filepath in glob("static/img/tarokka/*"):
    filename = os.path.basename(filepath)
    if not filename.endswith(".png"):
        continue
    if filename == "__Back.png":
        continue
    final_list.append(os.path.splitext(filename)[0])
print(final_list)
