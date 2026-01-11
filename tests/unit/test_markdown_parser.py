import os
import unittest
from unittest import mock

from src.common.markdown_parser import MarkdownParser
from src.dnd.utils import clean_custom_markdown
from tests.unit import find_root_directory


class TestMarkdownParser(unittest.TestCase):

    md: MarkdownParser = None

    @classmethod
    def setUpClass(cls):
        find_root_directory()
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
        [[[class:cleric#TOC|Table of Contents]]]
        [[[class:cleric#Domains]]]
        [[[class:cleric#Lots of Words]]]
        [[[class:cleric]]]
        [[[Mutants]]]
        [[[spell:enlarge/reduce]]]
        """
        expected = """
        <a class="wiki-link class" href="/dnd/class/cleric#toc">Table of Contents</a>
        <a class="wiki-link class" href="/dnd/class/cleric#domains">Domains</a>
        <a class="wiki-link class" href="/dnd/class/cleric#lots-of-words">Lots of Words</a>
        <a class="wiki-link class" href="/dnd/class/cleric">cleric</a>
        <a class="wiki-link-broken" href="/dnd/Mutants">Mutants</a>
        <a class="wiki-link spell" href="/dnd/spell/enlarge-reduce">enlarge/reduce</a>
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
        
        [Some "visual" aids](^some_visual_aids.jpg) all on the [same line](^same-line.jpg).
        
        [Wiki link](/dnd/wiki-link) before a [Visual aid](^visual_aid.jpg).
        """

        expected = """
        * <span class="visual-aid-link" title="visual_aid|ulkoria_stronemarrow.jpg|Ulkoria Stronemarrow">Ulkoria Stronemarrow<span class="visual-aid-hover"><img class="visual-aid-hover-img" src="/media/img/visual_aids/ulkoria_stronemarrow.jpg"></span></span>, representative for the Watchful Order of Magists and Protectors

        ## [Faction NPCs](Faction NPCs)
        
        ## Enemy NPCs
        * <span class="visual-aid-link" title="visual_aid|kenku.jpg|Kenku">Kenku<span class="visual-aid-hover"><img class="visual-aid-hover-img" src="/media/img/visual_aids/kenku.jpg"></span></span>
        * <span class="visual-aid-link" title="visual_aid|gazer.jpg|Gazer">Gazer<span class="visual-aid-hover"><img class="visual-aid-hover-img" src="/media/img/visual_aids/gazer.jpg"></span></span>
        
        * <span class="visual-aid-link" title="load|effect|WARFARE WEAPON SWORD SCRAPE PIRATE CUTLASS CIVIL WAR 01.mp3">Sword</span>
        <span class="visual-aid-link" title="pause|all">Pause All</span>
        
        <span class="visual-aid-link" title="visual_aid|some_visual_aids.jpg|Some %22visual%22 aids">Some "visual" aids<span class="visual-aid-hover"><img class="visual-aid-hover-img" src="/media/img/visual_aids/some_visual_aids.jpg"></span></span> all on the <span class="visual-aid-link" title="visual_aid|same-line.jpg|same line">same line<span class="visual-aid-hover"><img class="visual-aid-hover-img" src="/media/img/visual_aids/same-line.jpg"></span></span>.
        
        [Wiki link](/dnd/wiki-link) before a <span class="visual-aid-link" title="visual_aid|visual_aid.jpg|Visual aid">Visual aid<span class="visual-aid-hover"><img class="visual-aid-hover-img" src="/media/img/visual_aids/visual_aid.jpg"></span></span>.
        """

        md = MarkdownParser()
        actual = md.convert_popup_links(text)
        self.assertEqual(expected, actual)

    def test_convert_simple_links(self):
        text = """
* [Test Link 1]()
* [Test Link 2]()
* [Test Link 3](#)
* [Test Link 4](folder/Test Link)
* [[glossary:D20 Tests]] and [Test Link 5](#)
        """
        expected = """
* [Test Link 1](Test Link 1)
* [Test Link 2](Test Link 2)
* [Test Link 3](#test-link-3)
* [Test Link 4](folder/Test Link)
* [[glossary:D20 Tests]] and [Test Link 5](#test-link-5)
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

    def test_add_breadcrumbs(self):
        text = """
[[breadcrumb /dnd/class/Paladin|Paladin]]

<div class="phb-sidebar" markdown="1">"""
        expected = """
⟵ [Paladin](/dnd/class/Paladin)

<div class="phb-sidebar" markdown="1">"""
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

    def test_add_rules_glossary_tooltips(self):
        text = "***Armor Training.*** When you gain your first Barbarian level, you gain [[glossary:armor training]] with Shields."
        expected = """***Armor Training.*** When you gain your first Barbarian level, you gain <dfn name="armor training"><button class="dfn-tooltip" href="/dnd/general/Rules Glossary#armor-training"><p>Armor training allows you to use armor of a certain category without the following drawbacks. If you wear Light, Medium, or Heavy armor and lack training with it, you have Disadvantage on any <a href="#d20-test">D20 Test</a> that involves Strength or Dexterity, and you can't cast spells. If you use a Shield and lack training with it, you don't gain its AC bonus. <em>See also</em> <a href="#disadvantage">Disadvantage</a> and <em>Armor</em>.</p></button></dfn> with Shields."""
        actual = self.md.add_rules_glossary_tooltips(text)
        self.assertEqual(expected, actual)
        text = "**Bardic Damage.** You can use Dexterity instead of Strength for the attack rolls of your [[glossary:Unarmed Strike|Unarmed Strikes]], and"
        expected = """**Bardic Damage.** You can use Dexterity instead of Strength for the attack rolls of your <dfn name="Unarmed Strikes"><button class="dfn-tooltip" href="/dnd/general/Rules Glossary#unarmed-strike"><p>Instead of using a weapon to make a melee attack, you can use a punch, kick, headbutt, or similar forceful blow. In game terms, this is an Unarmed Strike -- a melee attack that involves you using your body to damage, grapple, or shove a target within 5 feet of you.</p>

<p>Whenever you use your Unarmed Strike, choose one of the following options for its effect.</p>

<p><strong><em>Damage.</em></strong> You make an <a href="#attack-roll">attack roll</a> against the target. Your bonus to the roll equals your Strength modifier plus your Prof ... <em>[more]</em></p></button></dfn>, and"""
        actual = self.md.add_rules_glossary_tooltips(text)
        self.assertEqual(expected, actual)

    def test_include_monster_sheet(self):
        input_text = """<div class="monster-float">

[[include dnd/monster-sheet.tpl]]
width = 500px
name = Fey Spirit
size = Small
type = fey
alignment = 
armor_class = 12 + the level of the spell (natural armor)
hit_points = 30 + 10 for each spell level above 3rd
speed = 40 ft.
strength = 13
dexterity = 16
constitution = 14
intelligence = 14
wisdom = 11
charisma = 16
condition_immunities = charmed
senses = darkvision 60 ft., passive Perception 10
languages = Sylvan, understands the languages you speak
proficiency_bonus = equals your bonus
actions = !!!
***Multiattack.*** The elemental makes a number of attacks equal to half this spell's level (rounded down).

***Shortsword.*** _Melee Weapon Attack:_ your spell attack modifier to hit, reach 5 ft., one target. _Hit:_ 1d6 + 3 + the spell's level piercing damage and 1d6 force damage.
!!!
bonus_actions = !!!
***Fey Step.*** The fey magically teleports up to 30 feet to an unoccupied space it can see. Then one of the following effects occurs, based on the fey's chosen mood:

* **Fuming.** The fey has advantage on the next attack roll it makes before the end of this turn.
* **Mirthful.** The fey can force one creature it can see within 10 feet of it to make a Wisdom saving throw against your spell save DC. Unless the save succeeds, the target is
charmed by you and the fey for 1 minute or until the target takes any damage.
* **Tricksy.** The fey can fill a 5-foot cube within 5 feet of it with magical darkness, which lasts until the end of its next turn.
!!!
[[/include]]

</div>

You call forth a fey spirit. It manifests in an unoccupied space that you can see within range. This corporeal form uses the Fey Spirit stat block. When you cast the spell, choose a mood: Fuming, Mirthful, or Tricksy. The creature resembles a fey creature of your choice marked by the chosen mood, which determines one of the traits in its stat block. The creature disappears when it drops to 0 hit points or when the spell ends.

The creature is an ally to you and your companions. In combat, the creature shares your initiative count, but it takes its turn immediately after yours. It obeys your verbal commands (no action required by you). If you don't issue any, it takes the Dodge action and uses its move to avoid danger.
"""
        expected = """<div class="monster-float">

<link rel="stylesheet" type="text/css" href="/static/css/monster-sheet.css">
<div class="monster-sheet" style="max-width: 500px;">
    <div class="top-bottom-bar"></div>
    <h1 class="name">Fey Spirit</h1>
    <div class="type">Small fey</div>
    <div class="red-bar"></div>
    <div class="text"><strong>Armor Class</strong> 12 + the level of the spell (natural armor)</div>
    <div class="text"><strong>Hit Points</strong> 30 + 10 for each spell level above 3rd</div>
    <div class="text"><strong>Speed</strong> 40 ft.</div>
    <div class="red-bar"></div>
    <div class="ability-scores">
        <span class="ability-score-name">STR</span>
        <span class="ability-score-name">DEX</span>
        <span class="ability-score-name">CON</span>
        <span class="ability-score-name">INT</span>
        <span class="ability-score-name">WIS</span>
        <span class="ability-score-name">CHA</span>
        <span class="ability-score-value">13 (+1)</span>
        <span class="ability-score-value">16 (+3)</span>
        <span class="ability-score-value">14 (+2)</span>
        <span class="ability-score-value">14 (+2)</span>
        <span class="ability-score-value">11 (+0)</span>
        <span class="ability-score-value">16 (+3)</span>
    </div>
    <div class="red-bar"></div>
    <div class="text"><strong>Condition Immunities</strong> charmed</div>
    <div class="text"><strong>Senses</strong> darkvision 60 ft., passive Perception 10</div>
    <div class="text"><strong>Languages</strong> Sylvan, understands the languages you speak</div>
    <div class="text"><strong>Proficiency Bonus</strong> equals your bonus</div>
    <div class="red-bar"></div>
    <h2 class="actions-header">Actions</h2>
    <div class="text-black">
        <p><strong><em>Multiattack.</em></strong> The elemental makes a number of attacks equal to half this spell's level (rounded down).</p>

<p><strong><em>Shortsword.</em></strong> <em>Melee Weapon Attack:</em> your spell attack modifier to hit, reach 5 ft., one target. <em>Hit:</em> 1d6 + 3 + the spell's level piercing damage and 1d6 force damage.</p>

    </div>
    <h2 class="actions-header">Bonus Actions</h2>
    <div class="text-black">
        <p><strong><em>Fey Step.</em></strong> The fey magically teleports up to 30 feet to an unoccupied space it can see. Then one of the following effects occurs, based on the fey's chosen mood:</p>

<ul>
<li><strong>Fuming.</strong> The fey has advantage on the next attack roll it makes before the end of this turn.</li>
<li><strong>Mirthful.</strong> The fey can force one creature it can see within 10 feet of it to make a Wisdom saving throw against your spell save DC. Unless the save succeeds, the target is
charmed by you and the fey for 1 minute or until the target takes any damage.</li>
<li><strong>Tricksy.</strong> The fey can fill a 5-foot cube within 5 feet of it with magical darkness, which lasts until the end of its next turn.</li>
</ul>

    </div>
    <div class="top-bottom-bar"></div>
</div>


</div>

<p>You call forth a fey spirit. It manifests in an unoccupied space that you can see within range. This corporeal form uses the Fey Spirit stat block. When you cast the spell, choose a mood: Fuming, Mirthful, or Tricksy. The creature resembles a fey creature of your choice marked by the chosen mood, which determines one of the traits in its stat block. The creature disappears when it drops to 0 hit points or when the spell ends.</p>

<p>The creature is an ally to you and your companions. In combat, the creature shares your initiative count, but it takes its turn immediately after yours. It obeys your verbal commands (no action required by you). If you don't issue any, it takes the Dodge action and uses its move to avoid danger.</p>
"""
        md = MarkdownParser()
        actual = md.parse_md(input_text, namespace="dnd", with_metadata=False)
        self.assertEqual(expected, actual.replace("\r\n", "\n"))

    def test_glossary_tooltips(self):
        input_text = """
[[glossary:Unarmed Strike]]
"""
        expected = """<p><dfn name="Unarmed Strike"><button class="dfn-tooltip" href="/dnd/general/Rules Glossary#unarmed-strike"><p>Instead of using a weapon to make a melee attack, you can use a punch, kick, headbutt, or similar forceful blow. In game terms, this is an Unarmed Strike -- a melee attack that involves you using your body to damage, grapple, or shove a target within 5 feet of you.</p>

<p>Whenever you use your Unarmed Strike, choose one of the following options for its effect.</p>

<p><strong><em>Damage.</em></strong> You make an <a href="#attack-roll">attack roll</a> against the target. Your bonus to the roll equals your Strength modifier plus your Prof ... <em>[more]</em></p></button></dfn></p>
"""
        md = MarkdownParser()
        actual = md.parse_md(input_text, namespace="dnd", with_metadata=False)
        self.assertEqual(expected, actual)

    def test_equipment_tooltips(self):
        input_text = """
[[tooltip:Leather Armor]]

[[tooltip:Scale Mail]]

[[tooltip:Plate Armor]]

[[tooltip:Club]]

[[tooltip:Finesse]]

[[tooltip:Push]]

[[tooltip:Cartographer's Tools]]

[[tooltip:Poisoner's Kit]]

[[tooltip:Backpack]]

[[tooltip:Arcane Focus]]
"""
        expected = """<p><dfn name="Leather Armor"><button class="dfn-tooltip" href="/dnd/general/Equipment#/dnd/general/Equipment#armor"><p><strong>AC:</strong> 11 + Dex modifier<br />
<strong>Weight:</strong> 10 lb.  <strong>Cost:</strong> 10 GP</p></button></dfn></p>

<p><dfn name="Scale Mail"><button class="dfn-tooltip" href="/dnd/general/Equipment#/dnd/general/Equipment#armor"><p><strong>AC:</strong> 14 + Dex modifier (max 2)<br />
<strong>Weight:</strong> 45 lb.  <strong>Cost:</strong> 50 GP<br />
Disadvantage on Stealth</p></button></dfn></p>

<p><dfn name="Plate Armor"><button class="dfn-tooltip" href="/dnd/general/Equipment#/dnd/general/Equipment#armor"><p><strong>AC:</strong> 18<br />
<strong>Weight:</strong> 65 lb.  <strong>Cost:</strong> 1,500 GP<br />
<strong>Strength Required:</strong> Str 15<br />
Disadvantage on Stealth</p></button></dfn></p>

<p><dfn name="Club"><button class="dfn-tooltip" href="/dnd/general/Equipment#/dnd/general/Equipment#weapons"><p><strong>Damage:</strong> 1d4 Bludgeoning  <strong>Mastery:</strong> <em>Slow</em><br />
<strong>Weight:</strong> 2 lb.  <strong>Cost:</strong> 1 SP<br />
<strong>Properties:</strong> <em>Light</em></p></button></dfn></p>

<p><dfn name="Finesse"><button class="dfn-tooltip" href="/dnd/general/Equipment#finesse"><p>When making an attack with a Finesse weapon, use your choice of your Strength or Dexterity modifier for the attack and damage rolls. You must use the same modifier for both rolls.</p></button></dfn></p>

<p><dfn name="Push"><button class="dfn-tooltip" href="/dnd/general/Equipment#push"><p>If you hit a creature with this weapon, you can push the creature up to 10 feet straight away from yourself if it is Large or smaller.</p></button></dfn></p>

<p><dfn name="Cartographer's Tools"><button class="dfn-tooltip" href="/dnd/general/Equipment#cartographers-tools"><p><strong>Ability:</strong> Wisdom <strong>Weight:</strong> 6 lb. <strong>Cost:</strong> 15 GP</p>

<p><strong>Utilize:</strong> Draft a map of a small area (DC 15)</p>

<p><strong>Craft:</strong> <em>Map</em></p></button></dfn></p>

<p><dfn name="Poisoner's Kit"><button class="dfn-tooltip" href="/dnd/general/Equipment#poisoners-kit"><p><strong>Ability:</strong> Intelligence <strong>Weight:</strong> 2 lb. <strong>Cost:</strong> 50 GP</p>

<p><strong>Utilize:</strong> Detect a poisoned object (DC 10)</p>

<p><strong>Craft:</strong> <em>Basic Poison</em></p></button></dfn></p>

<p><dfn name="Backpack"><button class="dfn-tooltip" href="/dnd/general/Equipment#backpack"><p><strong>Cost:</strong> 2 GP</p>

<p>A Backpack holds up to 30 pounds within 1 cubic foot. It can also serve as a saddlebag.</p></button></dfn></p>

<p><dfn name="Arcane Focus"><button class="dfn-tooltip" href="/dnd/general/Equipment#arcane-focus"><p><strong>Cost:</strong> Varies</p>

<p>An Arcane Focus takes one of the forms in the Arcane Focuses table and is bejeweled or carved to channel arcane magic. A Sorcerer, Warlock, or Wizard can use such an item as a Spellcasting Focus.</p></button></dfn></p>
"""
        md = MarkdownParser()
        actual = md.parse_md(input_text, namespace="dnd", with_metadata=False)
        self.assertEqual(expected, actual)

    def test_too_long_tooltip(self):
        input_text = "[[tooltip:Manacles]]"
        expected = """<p><dfn name="Manacles"><button class="dfn-tooltip" href="/dnd/general/Equipment#manacles"><p><strong>Cost:</strong> 2 GP</p>
<p>As a <em>Utilize</em> action, you can use Manacles to bind an unwilling Small or Medium creature within 5 feet of yourself that has the <em>Grappled</em>, <em>Incapacitated</em>, or <em>Restrained</em> condition if you succeed on a DC 13 Dexterity (<em>Sleight of Hand</em>) check. While bound, a creature has <em>Disadvantage</em> on attack rolls, and the creature is <em>Restrained</em> if the Manacles are attached to a chain or hook that is fixed in place. Escaping the Manacles requires a successful DC 20 Dexterity (<em>Sleight of Hand</em>) check as an a</p> ... <em>[more]</em></button></dfn></p>
"""
        md = MarkdownParser()
        actual = md.parse_md(input_text, namespace="dnd", with_metadata=False)
        self.assertEqual(expected, actual)

    def test_clean_custom_markdown(self):
        input_text = "The [[glossary:Magic]] action can be used on [[tooltip:Manacles]] to cast _[[[spell:Arcane Lock]]]_."
        expected = "The _Magic_ action can be used on _Manacles_ to cast _Arcane Lock_."
        self.assertEqual(expected, clean_custom_markdown(input_text))
