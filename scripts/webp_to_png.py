import os
from glob import glob
from os.path import splitext

from PIL import Image

in_ext = ".webp"
out_ext = ".png"

directory = os.environ["PICTURES_DIR"]

print(f'Searching for pictures in {directory} to convert...')
glob_path = directory.rstrip("/") + "/*" + in_ext
for filepath in glob(glob_path):
    print(filepath)
    out_filepath = splitext(filepath)[0] + out_ext
    im = Image.open(filepath)
    if out_ext == ".jpg":
        # Get rid of transparency
        bg = Image.new("RGB", im.size, "WHITE")
        try:
            bg.paste(im, (0, 0), im)
            bg.save(out_filepath)
        except ValueError as e:
            if str(e) == "bad transparency mask":
                # No transparency actually used in file, so don't bother and just save
                im.save(out_filepath)
            else:
                raise
    else:
        im.save(out_filepath)
    os.remove(filepath)
