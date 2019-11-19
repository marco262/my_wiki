% include("header.tpl", title="5e Spells Database")
% from data.enums import classes

<h1>5e Spells Database</h1>

<ul>
<li><a href="all_spells_by_name/true">All Spells By Name</a></li>
<li><a href="concentration_spells/true">Concentration Spells</a></li>
<li><a href="ritual_spells/true">Ritual Spells</a></li>
</ul>

<h3>Class Spell Lists</h3>

<ul>
    % for c in classes:
    <li><a href="class_spell_list/{{c.lower()}}/true">{{c.title()}} Spells</a></li>
    % end
</ul>

<p />

<a href="search">Search Spells</a><br>
<a href="spell_filter">Spell Filter</a>

% include("footer.tpl")
