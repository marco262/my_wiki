% include("header.tpl", title="5e Spells Database")

<h1>5e Spells Database</h1>

<ul>
<li><a href="all_spells_by_name">All Spells By Name</a></li>
<li><a href="concentration_spells">Concentration Spells</a></li>
<li><a href="ritual_spells">Ritual Spells</a></li>
</ul>

<h3>Class Spell Lists</h3>

<ul>
    % for c in ['Bard', 'Cleric', 'Druid', 'Paladin', 'Ranger', 'Sorcerer', 'Warlock', 'Wizard']:
    <li><a href="class_spell_list/{{c.lower()}}">{{c}} Spells</a></li>
    % end
</ul>

<p />

<a href="search">Search Spells</a>

% include("footer.tpl")
