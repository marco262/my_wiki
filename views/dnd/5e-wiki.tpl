% from data.dnd.enums import classes, spell_classes

<h2>Classes</h2>

<ul>
    % for c in classes:
    <li><a href="/dnd/class/{{c.lower()}}">{{c.title()}}</a></li>
    % end
</ul>

<h3>Homebrew classes</h3>

<ul>
    <li><a href="/dnd/class/dragonfire-adept">Dragonfire Adept</a></li>
</ul>

<h2>Spells</h2>

<ul>
<li><a href="/dnd/all_spells_by_name/true">All Spells By Name</a></li>
<li><a href="/dnd/concentration_spells/true">Concentration Spells</a></li>
<li><a href="/dnd/ritual_spells/true">Ritual Spells</a></li>
</ul>

<h3>Class Spell Lists</h3>

<ul>
    % for c in spell_classes:
    <li><a href="/dnd/class_spell_list/{{c.lower()}}/true">{{c.title()}} Spells</a></li>
    % end
</ul>

<p>

<a href="/dnd/search">Search Spells</a><br>
<a href="/dnd/spell_filter">Spell Filter</a>
