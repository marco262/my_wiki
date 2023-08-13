import os
import unittest
from unittest import mock

from src.common.markdown_parser import MarkdownParser


class TestMarkdownParser(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.md = MarkdownParser(init_md=False)
        cls.md.namespace = "dnd"

    def test_base_dir(self):
        from src.common.markdown_parser import BASE_DIR
        self.assertEqual("my_wiki", os.path.basename(BASE_DIR))

    @mock.patch("os.path.isfile")
    def test_convert_wiki_links(self, isfile_mock):
        def mock_func(path):
            path = path.replace("\\", "/")  # Normalize OS paths
            if path.endswith(r"my_wiki/data/dnd/class/cleric.md"):
                return True
            if path.endswith(r"my_wiki/data/dnd/mutants.md"):
                return False
            if path.endswith(r"my_wiki/data/dnd/mutants.toml"):
                return False
            if path.endswith(r"my_wiki/data/dnd/spell/enlarge-reduce.md"):
                return False
            if path.endswith(r"my_wiki/data/dnd/spell/enlarge-reduce.toml"):
                return True
            raise ValueError(path)

        isfile_mock.side_effect = mock_func
        pre_markdown = """
        [[[class:cleric#toc|Table of Contents]]]
        [[[class:cleric#domains]]]
        [[[class:cleric]]]
        [[[Mutants]]]
        [[[spell:enlarge/reduce]]]
        """
        expected = """
        <a class="wiki-link" href="/dnd/class/cleric#toc">Table of Contents</a>
        <a class="wiki-link" href="/dnd/class/cleric#domains">domains</a>
        <a class="wiki-link" href="/dnd/class/cleric">cleric</a>
        <a class="wiki-link-broken" href="/dnd/Mutants">Mutants</a>
        <a class="wiki-link" href="/dnd/spell/enlarge-reduce">enlarge/reduce</a>
        """
        actual = self.md.convert_wiki_links(pre_markdown)
        self.assertEqual(expected, actual)

    def test_add_header_links(self):
        pre_markdown = """
Test header 1

# Test 1

## This Is A Test!

### Also a test
        """
        expected = """
<p>Test header 1</p>

<h1 id="test-1">Test 1<a href="#test-1" class="header-link">¶</a></h1>

<h2 id="this-is-a-test">This Is A Test!<a href="#this-is-a-test" class="header-link">¶</a></h2>

<h3 id="also-a-test">Also a test<a href="#also-a-test" class="header-link">¶</a></h3>
        """
        md = MarkdownParser()
        actual = md.parse_md(pre_markdown)
        self.assertEqual(expected.strip(" ").lstrip("\n"), actual)

    def test_parse_accordion(self):
        pre_markdown = """
[[accordion Test Title]]
# Header

* Item 1
* *Item 2*
* **Item 3**

Text block

[[/accordion]]
"""
        expected = """<button class="accordion-button">Test Title</button>
<div class="accordion-panel">

<h1 id="header">Header<a href="#header" class="header-link">¶</a></h1>

<ul>
<li>Item 1</li>
<li><em>Item 2</em></li>
<li><strong>Item 3</strong></li>
</ul>

<p>Text block</p>

</div>
"""
        md = MarkdownParser()
        actual = md.parse_md(pre_markdown)
        self.assertEqual(expected, actual)

    def test_convert_popup_links(self):
        text = """
        * [Ulkoria Stronemarrow](^ulkoria_stronemarrow.jpg), representative for the Watchful Order of Magists and Protectors

        ## [Faction NPCs](Faction NPCs)
        
        ## Enemy NPCs
        * [Kenku](^kenku.jpg)
        * [Gazer](^gazer.jpg)
        
        * [Sword]($load|effect|WARFARE WEAPON SWORD SCRAPE PIRATE CUTLASS CIVIL WAR 01.mp3)
        [Pause All]($pause|all)
        
        [Some visual aids](^some_visual_aids.jpg) all on the [same line](^same-line.jpg).
        
        [Wiki link](/dnd/wiki-link) before a [Visual aid](^visual_aid.jpg).
        """

        expected = """
        * <span class="visual-aid-link" title="visual_aid|ulkoria_stronemarrow.jpg|Ulkoria%20Stronemarrow">Ulkoria Stronemarrow<span class="visual-aid-hover"><img class="visual-aid-hover-img" src="/media/img/visual_aids/ulkoria_stronemarrow.jpg"></span></span>, representative for the Watchful Order of Magists and Protectors

        ## [Faction NPCs](Faction NPCs)
        
        ## Enemy NPCs
        * <span class="visual-aid-link" title="visual_aid|kenku.jpg|Kenku">Kenku<span class="visual-aid-hover"><img class="visual-aid-hover-img" src="/media/img/visual_aids/kenku.jpg"></span></span>
        * <span class="visual-aid-link" title="visual_aid|gazer.jpg|Gazer">Gazer<span class="visual-aid-hover"><img class="visual-aid-hover-img" src="/media/img/visual_aids/gazer.jpg"></span></span>
        
        * <span class="visual-aid-link" title="load|effect|WARFARE WEAPON SWORD SCRAPE PIRATE CUTLASS CIVIL WAR 01.mp3">Sword</span>
        <span class="visual-aid-link" title="pause|all">Pause All</span>
        
        <span class="visual-aid-link" title="visual_aid|some_visual_aids.jpg|Some%20visual%20aids">Some visual aids<span class="visual-aid-hover"><img class="visual-aid-hover-img" src="/media/img/visual_aids/some_visual_aids.jpg"></span></span> all on the <span class="visual-aid-link" title="visual_aid|same-line.jpg|same%20line">same line<span class="visual-aid-hover"><img class="visual-aid-hover-img" src="/media/img/visual_aids/same-line.jpg"></span></span>.
        
        [Wiki link](/dnd/wiki-link) before a <span class="visual-aid-link" title="visual_aid|visual_aid.jpg|Visual%20aid">Visual aid<span class="visual-aid-hover"><img class="visual-aid-hover-img" src="/media/img/visual_aids/visual_aid.jpg"></span></span>.
        """

        md = MarkdownParser()
        actual = md.convert_popup_links(text)
        self.assertEqual(expected, actual)

    def test_convert_simple_links(self):
        text = """
* [Test Link 1]()
* [Test Link 2]()
* [Test Link 3](folder/Test Link)
        """
        expected = """
* [Test Link 1](Test Link 1)
* [Test Link 2](Test Link 2)
* [Test Link 3](folder/Test Link)
        """
        md = MarkdownParser()
        actual = md.convert_simple_links(text)
        self.assertEqual(expected, actual)

    def test_build_bibliography(self):
        text = """
<p><strong>Garrote.</strong>[((bibcite homebrew))] Can only be used on ...</p>

<p><strong>Lance.</strong>[((bibcite errata))] You have disadvantage ...</p>

[[bibliography]]
: errata : <a href="https://media.wizards.com/2018/dnd/downloads/PH-Errata.pdf">2018 PHB Errata</a>
: homebrew : Homebrew
[[/bibliography]]
"""
        expected = """
<p><strong>Garrote.</strong>[<a href="#homebrew">2</a>] Can only be used on ...</p>

<p><strong>Lance.</strong>[<a href="#errata">1</a>] You have disadvantage ...</p>

<p><strong>Bibliography</strong></p>

<ol>
    <li><a id="errata" /><a href="https://media.wizards.com/2018/dnd/downloads/PH-Errata.pdf">2018 PHB Errata</a></li>
    <li><a id="homebrew" />Homebrew</li>
</ol>
"""
        md = MarkdownParser()
        actual = md.build_bibliography(text)
        self.assertEqual(expected, actual)

    def test_convert_wiki_divs(self):
        text = """
[[div class="test"]]

**Test** text

[[/div]]

**Before text** [[span class="test"]]_middle text_[[/span]] *after text*
"""
        expected = """<div class="test">

<p><strong>Test</strong> text</p>

</div>

<p><strong>Before text</strong> <span class="test"><em>middle text</em></span> <em>after text</em></p>
"""
        md = MarkdownParser()
        text = md.parse_md(text)
        actual = md.convert_wiki_divs(text)
        self.assertEqual(expected, actual)

    def test_add_breadcrumbs(self):
        text = """[[breadcrumb /dnd/class/Druid|Druid]]
        
        Fake text"""
        expected = """⟵ [Druid](/dnd/class/Druid)
        
        Fake text"""
        md = MarkdownParser()
        self.assertEqual(expected, md.add_breadcrumbs(text))

    @mock.patch("src.common.markdown_parser.template", return_value="PARSER_MOCK_OUTPUT")
    def test_generate_npc_blocks(self, *m):
        text = """<p>I am a bear</p>
        <p>[[npc cr=2|race=Human]]</p>
        <p>Rawr</p>"""
        expected = """<p>I am a bear</p>
        <p>PARSER_MOCK_OUTPUT</p>
        <p>Rawr</p>"""
        md = MarkdownParser()
        self.assertEqual(expected, md.generate_npc_blocks(text))
        m[0].assert_called_with(
            "dnd/npc-sheet.tpl", cr="2", level=None, race="Human", role="", speed="30 ft.", stat_bonus=2, prof_bonus=3,
            armor_class=13, hit_points=45, damage_resistances="", damage_immunities="", damage_vulnerabilities="",
            senses="", special_abilities="", bonus_actions="",
            actions="<p><strong><em>Weapon attack x2.</em></strong> +5 to hit. <strong>Hit:</strong> 8 (2d6 + 1) damage.</p>\n",
            reactions="", villain_actions="", attack=5, damage="8 (2d6 + 1)", double_damage="30 (8d6 + 2)",
            triple_damage="45 (12d6 + 3)", save_dc=12, num_attacks=2, width="400px", untrained="+2", proficient="+5",
            expertise="+8"
        )

    def test_fancy_text(self):
        md = MarkdownParser()
        text = """
Text--more text -- Yes

+-----------+
-- Yugiri
+-----------+
"""
        expected = """
Text&mdash;more text &mdash; Yes

+-----------+
&mdash; Yugiri
+-----------+
"""
        self.assertEqual(expected, md.fancy_text(text))

    @mock.patch("src.common.markdown_parser.build_magic_item_tracker", return_value="<table>floomp</table>")
    def test_insert_magic_item_trackers(self, *_mocks: mock.MagicMock):
        text = """
I am initial text here I am look at me

[[magic-item-tracker]]
* Illuminator's Tattoo -- Minor Common
* Spell Scroll (Burning Hands) -- Minor Common
* Spell Scroll (Flaming Sphere) -- Minor Uncommon
* Dagger of Returning -- Minor Uncommon
* Wand of Witch Bolt -- Major Uncommon
* Wand of Witch Bolt -- Major Rare
* Wand of Witch Bolt -- Minor Very Rare
* Wand of Witch Bolt -- Major Legendary
* Major Wand of Rare Bolt -- Minor Legendary
[[/magic-item-tracker]]

Here's another tracker doing other things:

[[magic-item-tracker]]
* Illuminator's Tattoo -- Minor Common
* Spell Scroll (Burning Hands) -- Minor Common
[[/magic-item-tracker]]

And here's the ending
        """
        expected = """
I am initial text here I am look at me

* Illuminator's Tattoo -- Minor Common
* Spell Scroll (Burning Hands) -- Minor Common
* Spell Scroll (Flaming Sphere) -- Minor Uncommon
* Dagger of Returning -- Minor Uncommon
* Wand of Witch Bolt -- Major Uncommon
* Wand of Witch Bolt -- Major Rare
* Wand of Witch Bolt -- Minor Very Rare
* Wand of Witch Bolt -- Major Legendary
* Major Wand of Rare Bolt -- Minor Legendary

<table>floomp</table>

Here's another tracker doing other things:

* Illuminator's Tattoo -- Minor Common
* Spell Scroll (Burning Hands) -- Minor Common

<table>floomp</table>

And here's the ending
"""
        print(self.md.insert_magic_item_trackers(text))
