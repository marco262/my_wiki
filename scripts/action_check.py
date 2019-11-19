import re
from collections import OrderedDict, defaultdict
from glob import glob
from os.path import basename
from re import search, sub

import toml

duration_list = []
casting_time_list = []
range_list = []
shape_list = []

for path in glob("../data/spell/*"):
    with open(path) as f:
        d = toml.loads(f.read(), _dict=OrderedDict)
    # duration = d["duration"]
    # duration = duration.replace("Concentration, up to ", "")
    # duration = duration.replace("Up to ", "")
    # if not duration in duration_list:
    #     duration_list.append(duration)
    #
    # casting_time = d["casting_time"]
    # if "1 reaction" in casting_time:
    #     casting_time = "1 reaction"
    # if not casting_time in casting_time_list:
    #     casting_time_list.append(casting_time)

    # range = d["range"]
    # m = re.match(r"^Self \((.*)\)$", range)
    # if m:
    #     range = m.group(1)
    #     range = re.sub(r"[\- ]radius", "", range)
    #     range = range.split(" ")[0]
    #     range = range.replace("-foot", " feet")
    # if range == "5-mile":
    #     print(path)
    # if not range in range_list:
    #     range_list.append(range)

    shape = d["range"]
    if "Self (" in shape:
        print(path, shape)
    # if shape not in ["Self", "Sight", "Unlimited", "Special", "Touch"] and not shape.endswith("feet") \
    #         and not shape.endswith("miles") and not shape.endswith("mile") and not shape.endswith("radius)"):
    #     if not shape in shape_list:
    #         shape_list.append(shape)

# print(duration_list)
# print(casting_time_list)
# print(range_list)
print(shape_list)