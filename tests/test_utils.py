import os
import unittest

from src.common.utils import better_title, list_media_files, check_for_media_file


class TestUtils(unittest.TestCase):

    def test_better_title(self):
        data = "a player's guide and an equal treatment of the sexes"
        expected = "A Player's Guide and an Equal Treatment of the Sexes"
        self.assertEqual(expected, better_title(data))

    def test_list_media_files(self):
        os.chdir("..")
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
        os.chdir("..")
        self.assertTrue(check_for_media_file("media/img/tarokka/Master of Coins - Rogue.png"))
        self.assertFalse(check_for_media_file("media/img/tarokka/Master of Hats - Jester.png"))
