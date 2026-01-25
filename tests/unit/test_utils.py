import unittest
from unittest.mock import patch

from src.common.utils import better_title, list_media_files, check_for_media_file
from src.dnd.utils import split_rules_glossary, generate_magic_items
from tests.unit import find_root_directory


MUT = "src.dnd.utils."


class TestUtils(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        find_root_directory()

    def test_better_title(self):
        data = "a player's guide and an equal treatment of the sexes"
        expected = "A Player's Guide and an Equal Treatment of the Sexes"
        self.assertEqual(expected, better_title(data))

    def test_list_media_files(self):
        self.assertEqual(
            [
                "media/img/tarokka\\Master of Coins - Rogue.png",
                "media/img/tarokka\\Master of Glyphs - Priest.png",
                "media/img/tarokka\\Master of Stars - Wizard.png",
                "media/img/tarokka\\Master of Swords - Warrior.png",
            ],
            list_media_files("media/img/tarokka/Master*"),
        )

    def test_check_for_media_file(self):
        self.assertTrue(check_for_media_file("media/img/tarokka/Master of Coins - Rogue.png"))
        self.assertFalse(check_for_media_file("media/img/tarokka/Master of Hats - Jester.png"))

    def test_split_rules_glossary(self):
        glossary = split_rules_glossary()
        self.assertEqual(
            {
                "anchor": "armor-training",
                "content": "<p>Armor training is the new name for armor proficiency. Any existing rule that involves "
                           "armor proficiency now applies to armor training.</p>\n\n<p>If you wear Light, Medium, "
                           "or Heavy Armor and lack armor training with that type of armor, you have Disadvantage "
                           "on any d20 Test you make that involves Strength or Dexterity, and you can't cast "
                           "spells.</p>\n\n<p>If you equip a Shield and lack armor training with it, you don't gain "
                           "the Armor Class bonus of the Shield.</p>",
            },
            glossary["armor training"],
        )
        self.assertEqual(
            {
                "anchor": "unconscious-condition",
                "content": "<p>While Unconscious, you experience the following effects:</p>\n\n<p><strong>Inert."
                           "</strong> You have the Incapacitated and Prone conditions, and you drop whatever you're "
                           "holding. When this condition ends, you remain Prone. <br />\n<strong>Speed 0.</strong> "
                           "Your Speed is 0 and can't change. <br />\n<strong>Attacks Affected.</strong> Attack rolls "
                           "against you have Advantage. <br />\n<strong>Fail Str. and Dex. Saves.</strong> You "
                           "automatically fail Strength and Dexterity saving throws. <br />\n<strong>Critical Hits."
                           "</strong> Any attack roll that hits you is a critical hit if the attacker is with ... "
                           "<em>[more]</em></p>",
            },
            glossary["unconscious"],
        )

    @patch(MUT + "filter_magic_items", return_value={"spell-scroll-cantrip": {"name": "Spell Scroll (Cantrip)"}})
    @patch(MUT + "load_spells_by_level", return_value={0: [("elementalism", {"title": "Elementalism"})]})
    def test_generate_magic_items_spell_scroll(self, *_mocks):
        filter_keys = {"table_name": "Arcana", "type": ["Scroll"], "rarity": ["Common"]}
        self.assertEqual(
            [("Spell Scroll (Cantrip)", "Elementalism")],
            generate_magic_items(filter_keys, 1, False),
        )

    @patch(MUT + "filter_magic_items", return_value={"enspelled-staff-level-5": {"name": "Enspelled Staff (Level 5)"}})
    @patch(MUT + "load_spells_by_level", return_value={5: [("yolande-s-regal-presence", {"title": "Yolande's Regal Presence"})]})
    def test_generate_magic_items_enspelled_staff(self, *_mocks):
        filter_keys = {"table_name": "Arcana", "type": ["Staff"], "rarity": ["Very Rare"]}
        self.assertEqual(
            [("Enspelled Staff (Level 5)", "Yolande's Regal Presence")],
            generate_magic_items(filter_keys, 1, False),
        )
