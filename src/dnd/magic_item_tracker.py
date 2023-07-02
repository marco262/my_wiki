import sys
from copy import deepcopy
from typing import Dict, List
import re

TierDict = Dict[str, Dict[str, Dict[str, int]]]


TIER_DICTS = {
    "1—4": {
        "Minor": {
            "Common": {"current": 0, "max": 6},
            "Uncommon": {"current": 0, "max": 2},
            "Rare": {"current": 0, "max": 1},
            "Very Rare": {"current": 0, "max": 0},
            "Legendary": {"current": 0, "max": 0},
        },
        "Major": {
            "Uncommon": {"current": 0, "max": 2},
            "Rare": {"current": 0, "max": 0},
            "Very Rare": {"current": 0, "max": 0},
            "Legendary": {"current": 0, "max": 0},
        },
    },
    "5—10": {
        "Minor": {
            "Common": {"current": 0, "max": 10},
            "Uncommon": {"current": 0, "max": 12},
            "Rare": {"current": 0, "max": 5},
            "Very Rare": {"current": 0, "max": 1},
            "Legendary": {"current": 0, "max": 0},
        },
        "Major": {
            "Uncommon": {"current": 0, "max": 5},
            "Rare": {"current": 0, "max": 1},
            "Very Rare": {"current": 0, "max": 0},
            "Legendary": {"current": 0, "max": 0},
        },
    },
    "11—16": {
        "Minor": {
            "Common": {"current": 0, "max": 3},
            "Uncommon": {"current": 0, "max": 6},
            "Rare": {"current": 0, "max": 9},
            "Very Rare": {"current": 0, "max": 5},
            "Legendary": {"current": 0, "max": 1},
        },
        "Major": {
            "Uncommon": {"current": 0, "max": 1},
            "Rare": {"current": 0, "max": 2},
            "Very Rare": {"current": 0, "max": 2},
            "Legendary": {"current": 0, "max": 1},
        },
    },
    "17+": {
        "Minor": {
            "Common": {"current": 0, "max": 0},
            "Uncommon": {"current": 0, "max": 0},
            "Rare": {"current": 0, "max": 4},
            "Very Rare": {"current": 0, "max": 9},
            "Legendary": {"current": 0, "max": 6},
        },
        "Major": {
            "Uncommon": {"current": 0, "max": 0},
            "Rare": {"current": 0, "max": 1},
            "Very Rare": {"current": 0, "max": 2},
            "Legendary": {"current": 0, "max": 3},
        },
    },
}
TOTALS = {
    "Minor": {
        "Common": {"current": 0, "max": 19},
        "Uncommon": {"current": 0, "max": 20},
        "Rare": {"current": 0, "max": 19},
        "Very Rare": {"current": 0, "max": 15},
        "Legendary": {"current": 0, "max": 7},
    },
    "Major": {
        "Uncommon": {"current": 0, "max": 8},
        "Rare": {"current": 0, "max": 4},
        "Very Rare": {"current": 0, "max": 4},
        "Legendary": {"current": 0, "max": 4},
    },
}


def build_magic_item_tracker(text: str) -> str:
    totals = count_magic_items(text.split("\n"))
    tier_dicts = count_magic_item_tiers(totals)
    return build_magic_item_tracker_table(tier_dicts, totals)


def count_magic_items(magic_item_list: List[str]) -> TierDict:
    """
    Takes in a list of magic items of the format "<name> -- <major/minor> <rarity>" and creates a TierDict counting
    the total magic items.
    """
    totals = deepcopy(TOTALS)
    for magic_item in magic_item_list:
        if not magic_item.strip():
            # Handle blank lines gracefully
            continue
        m = re.match(r".* -- (Major|Minor) (.*)", magic_item, re.I)
        if not m:
            print(f"Not a valid magic item string: {magic_item}", file=sys.stderr)
            continue
        major_minor = str(m.group(1)).strip().title()
        rarity = str(m.group(2)).strip().title()
        try:
            totals[major_minor][rarity]["current"] += 1
        except KeyError:
            print(f"{m.group(1)} {m.group(2)} is not a valid rarity", file=sys.stderr)
            continue
    return totals


def count_magic_item_tiers(totals: TierDict) -> Dict[str, TierDict]:
    tier_dicts = deepcopy(TIER_DICTS)
    for mm, rarity_dict in totals.items():
        for rarity, d in rarity_dict.items():
            current = d["current"]
            for tier in ["1—4", "5—10", "11—16", "17+"]:
                td = tier_dicts[tier][mm][rarity]
                td["current"] = min(current, td["max"])
                current -= td["max"]
                if current <= 0:
                    break
            else:
                print(f"Too goddamn many {mm} {rarity} items: {d['current']}", file=sys.stderr)
    return tier_dicts


# noinspection StrFormat
def get_cell_text(current: int, max_items: int) -> str:
    if current == 0 and max_items == 0:
        return '        <td class="faded-out">--</td>'
    if current == max_items:
        cell_class = "faded-out"
    elif current > max_items:
        cell_class = "error-text"
    else:
        cell_class = ""
    cell_template = '        <td class="{}">{} / {}</td>'
    return cell_template.format(cell_class, current, max_items)


# noinspection StrFormat
def build_magic_item_tracker_table(tier_dicts: Dict[str, TierDict], totals: TierDict) -> str:
    table_template = """<table>
    <tr>
        <th></th>
        <th colspan="5">Minor Magic Items</th>
        <th colspan="4">Major Magic Items</th>
    </tr>
    <tr>
        <th>Level/CR</th>
        <th>Common</th>
        <th>Uncommon</th>
        <th>Rare</th>
        <th>Very Rare</th>
        <th>Legendary</th>
        <th>Uncommon</th>
        <th>Rare</th>
        <th>Very Rare</th>
        <th>Legendary</th>
    </tr>{}
</table>"""
    row_template = """
    <tr style="text-align: center">
        <td>{header}</td>
{rows}
    </tr>"""
    total_row_template = """
    <tr style="text-align: center; font-weight: bold">
        <td>Totals</td>
{rows}
    </tr>"""
    output = ""
    for tier, mm_dicts in tier_dicts.items():
        rows = []
        for mm, rarity_dicts in mm_dicts.items():
            for rarity, d in rarity_dicts.items():
                rows.append(get_cell_text(d["current"], d["max"]))
        output += row_template.format(header=tier, rows="\n".join(rows))
    # Totals
    rows = []
    for mm, rarity_dicts in totals.items():
        for rarity, d in rarity_dicts.items():
            rows.append(get_cell_text(d["current"], d["max"]))
    output += total_row_template.format(rows="\n".join(rows))
    return table_template.format(output)
