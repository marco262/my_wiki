import unittest
from json import dumps

from src.dnd.magic_item_tracker import build_magic_item_tracker, count_magic_items, count_magic_item_tiers, \
    build_magic_item_tracker_table


class TestMagicItemTracker(unittest.TestCase):

    def test_build_magic_item_tracker(self):
        magic_items = """
        * Illuminator's Tattoo -- Minor Common
        * Spell Scroll (Burning Hands) -- Minor Common
        * Spell Scroll (Flaming Sphere) -- Minor Uncommon
        * Dagger of Returning -- Minor Uncommon
        * Wand of Witch Bolt -- Major Uncommon
        * Wand of Witch Bolt -- Major Rare
        * Wand of Witch Bolt -- Minor Very Rare
        * Wand of Witch Bolt -- Major Legendary
        * Major Wand of Rare Bolt -- Minor Legendary
        """
        expected = """<table>
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
    </tr>
    <tr style="text-align: center">
        <td>1—4</td>
        <td class="">2 / 6</td>
        <td class="faded-out">2 / 2</td>
        <td class="">0 / 1</td>
        <td class="faded-out">0 / 0</td>
        <td class="faded-out">0 / 0</td>
        <td class="">1 / 2</td>
        <td class="faded-out">0 / 0</td>
        <td class="faded-out">0 / 0</td>
        <td class="faded-out">0 / 0</td>
    </tr>
    <tr style="text-align: center">
        <td>5—10</td>
        <td class="">0 / 10</td>
        <td class="">0 / 12</td>
        <td class="">0 / 5</td>
        <td class="faded-out">1 / 1</td>
        <td class="faded-out">0 / 0</td>
        <td class="">0 / 5</td>
        <td class="faded-out">1 / 1</td>
        <td class="faded-out">0 / 0</td>
        <td class="faded-out">0 / 0</td>
    </tr>
    <tr style="text-align: center">
        <td>11—16</td>
        <td class="">0 / 3</td>
        <td class="">0 / 6</td>
        <td class="">0 / 9</td>
        <td class="">0 / 5</td>
        <td class="faded-out">1 / 1</td>
        <td class="">0 / 1</td>
        <td class="">0 / 2</td>
        <td class="">0 / 2</td>
        <td class="faded-out">1 / 1</td>
    </tr>
    <tr style="text-align: center">
        <td>17+</td>
        <td class="faded-out">0 / 0</td>
        <td class="faded-out">0 / 0</td>
        <td class="">0 / 4</td>
        <td class="">0 / 9</td>
        <td class="">0 / 6</td>
        <td class="faded-out">0 / 0</td>
        <td class="">0 / 1</td>
        <td class="">0 / 2</td>
        <td class="">0 / 3</td>
    </tr>
    <tr style="text-align: center; font-weight: bold">
        <td>Totals</td>
        <td class="">2 / 19</td>
        <td class="">2 / 20</td>
        <td class="">0 / 19</td>
        <td class="">1 / 15</td>
        <td class="">1 / 7</td>
        <td class="">1 / 8</td>
        <td class="">1 / 4</td>
        <td class="">0 / 4</td>
        <td class="">1 / 4</td>
    </tr>
</table>"""
        self.assertEqual(expected, build_magic_item_tracker(magic_items))

    def test_count_magic_items(self):
        magic_items = """
        * Illuminator's Tattoo -- Minor Common
        * Spell Scroll (Burning Hands) -- Minor Common
        * Spell Scroll (Flaming Sphere) -- Minor Uncommon
        * Dagger of Returning -- Minor Uncommon
        * Wand of Witch Bolt -- Major Uncommon
        * Wand of Witch Bolt -- Major Rare
        * Wand of Witch Bolt -- Minor Very Rare
        * Wand of Witch Bolt -- Major Legendary
        * Major Wand of Rare Bolt -- Minor Legendary
        """
        expected = {
            "Minor": {
                "Common": {
                    "current": 2,
                    "max": 19
                },
                "Uncommon": {
                    "current": 2,
                    "max": 20
                },
                "Rare": {
                    "current": 0,
                    "max": 19
                },
                "Very Rare": {
                    "current": 1,
                    "max": 15
                },
                "Legendary": {
                    "current": 1,
                    "max": 7
                }
            },
            "Major": {
                "Uncommon": {
                    "current": 1,
                    "max": 8
                },
                "Rare": {
                    "current": 1,
                    "max": 4
                },
                "Very Rare": {
                    "current": 0,
                    "max": 4
                },
                "Legendary": {
                    "current": 1,
                    "max": 4
                }
            }
        }
        self.assertEqual(expected, count_magic_items(magic_items.split("\n")))

    def test_count_magic_item_tiers(self):
        totals = {
            "Minor": {
                "Common": {
                    "current": 10,
                    "max": 19
                },
                "Uncommon": {
                    "current": 15,
                    "max": 20
                },
                "Rare": {
                    "current": 18,
                    "max": 19
                },
                "Very Rare": {
                    "current": 8,
                    "max": 15
                },
                "Legendary": {
                    "current": 5,
                    "max": 7
                }
            },
            "Major": {
                "Uncommon": {
                    "current": 2,
                    "max": 8
                },
                "Rare": {
                    "current": 1,
                    "max": 4
                },
                "Very Rare": {
                    "current": 0,
                    "max": 4
                },
                "Legendary": {
                    "current": 1,
                    "max": 4
                }
            }
        }
        print(dumps(count_magic_item_tiers(totals), indent=4))

    def test_build_magic_item_tracker_table(self):
        tier_dicts = {
            "1—4": {
                "Minor": {
                    "Common": {"current": 1, "max": 6},
                    "Uncommon": {"current": 2, "max": 2},
                    "Rare": {"current": 3, "max": 1},
                    "Very Rare": {"current": 4, "max": 0},
                    "Legendary": {"current": 5, "max": 0},
                },
                "Major": {
                    "Uncommon": {"current": 6, "max": 2},
                    "Rare": {"current": 7, "max": 0},
                    "Very Rare": {"current": 8, "max": 0},
                    "Legendary": {"current": 9, "max": 0},
                },
            },
            "5—10": {
                "Minor": {
                    "Common": {"current": 10, "max": 10},
                    "Uncommon": {"current": 11, "max": 12},
                    "Rare": {"current": 12, "max": 5},
                    "Very Rare": {"current": 13, "max": 1},
                    "Legendary": {"current": 14, "max": 0},
                },
                "Major": {
                    "Uncommon": {"current": 15, "max": 5},
                    "Rare": {"current": 16, "max": 1},
                    "Very Rare": {"current": 17, "max": 0},
                    "Legendary": {"current": 18, "max": 0},
                },
            },
            "11—16": {
                "Minor": {
                    "Common": {"current": 19, "max": 3},
                    "Uncommon": {"current": 20, "max": 6},
                    "Rare": {"current": 21, "max": 9},
                    "Very Rare": {"current": 22, "max": 5},
                    "Legendary": {"current": 23, "max": 1},
                },
                "Major": {
                    "Uncommon": {"current": 24, "max": 1},
                    "Rare": {"current": 25, "max": 2},
                    "Very Rare": {"current": 26, "max": 2},
                    "Legendary": {"current": 27, "max": 1},
                },
            },
            "17+": {
                "Minor": {
                    "Common": {"current": 28, "max": 0},
                    "Uncommon": {"current": 29, "max": 0},
                    "Rare": {"current": 30, "max": 4},
                    "Very Rare": {"current": 31, "max": 9},
                    "Legendary": {"current": 32, "max": 6},
                },
                "Major": {
                    "Uncommon": {"current": 33, "max": 0},
                    "Rare": {"current": 34, "max": 1},
                    "Very Rare": {"current": 35, "max": 2},
                    "Legendary": {"current": 36, "max": 3},
                },
            },
        }
        totals = {
            "Minor": {
                "Common": {"current": 37, "max": 19},
                "Uncommon": {"current": 38, "max": 20},
                "Rare": {"current": 39, "max": 19},
                "Very Rare": {"current": 40, "max": 15},
                "Legendary": {"current": 41, "max": 7},
            },
            "Major": {
                "Uncommon": {"current": 42, "max": 8},
                "Rare": {"current": 43, "max": 4},
                "Very Rare": {"current": 44, "max": 4},
                "Legendary": {"current": 45, "max": 4},
            },
        }
        expected = """<table>
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
    </tr>
    <tr style="text-align: center">
        <td>1—4</td>
        <td class="">1 / 6</td>
        <td class="faded-out">2 / 2</td>
        <td class="error-text">3 / 1</td>
        <td class="error-text">4 / 0</td>
        <td class="error-text">5 / 0</td>
        <td class="error-text">6 / 2</td>
        <td class="error-text">7 / 0</td>
        <td class="error-text">8 / 0</td>
        <td class="error-text">9 / 0</td>
    </tr>
    <tr style="text-align: center">
        <td>5—10</td>
        <td class="faded-out">10 / 10</td>
        <td class="">11 / 12</td>
        <td class="error-text">12 / 5</td>
        <td class="error-text">13 / 1</td>
        <td class="error-text">14 / 0</td>
        <td class="error-text">15 / 5</td>
        <td class="error-text">16 / 1</td>
        <td class="error-text">17 / 0</td>
        <td class="error-text">18 / 0</td>
    </tr>
    <tr style="text-align: center">
        <td>11—16</td>
        <td class="error-text">19 / 3</td>
        <td class="error-text">20 / 6</td>
        <td class="error-text">21 / 9</td>
        <td class="error-text">22 / 5</td>
        <td class="error-text">23 / 1</td>
        <td class="error-text">24 / 1</td>
        <td class="error-text">25 / 2</td>
        <td class="error-text">26 / 2</td>
        <td class="error-text">27 / 1</td>
    </tr>
    <tr style="text-align: center">
        <td>17+</td>
        <td class="error-text">28 / 0</td>
        <td class="error-text">29 / 0</td>
        <td class="error-text">30 / 4</td>
        <td class="error-text">31 / 9</td>
        <td class="error-text">32 / 6</td>
        <td class="error-text">33 / 0</td>
        <td class="error-text">34 / 1</td>
        <td class="error-text">35 / 2</td>
        <td class="error-text">36 / 3</td>
    </tr>
    <tr style="text-align: center; font-weight: bold">
        <td>Totals</td>
        <td class="error-text">37 / 19</td>
        <td class="error-text">38 / 20</td>
        <td class="error-text">39 / 19</td>
        <td class="error-text">40 / 15</td>
        <td class="error-text">41 / 7</td>
        <td class="error-text">42 / 8</td>
        <td class="error-text">43 / 4</td>
        <td class="error-text">44 / 4</td>
        <td class="error-text">45 / 4</td>
    </tr>
</table>"""
        self.assertEqual(expected, build_magic_item_tracker_table(tier_dicts, totals))
