% include("header.tpl", title="Spell Search")

<h1>Spell Search</h1>

<table>
    <tr>
        <td>
        % classes = ["bard", "cleric", "druid", "paladin", "ranger", "sorcerer", "warlock", "wizard"]
        % for s in spells:
            <li><a href="class_spell_list/{{c.lower()}}">{{c}} Spells</a></li>
        % end
        </td>
    </tr>
</table>

<p />

<div id="search_results"><i>Search results will appear here</i></div>

<script type="module">
    import {search, on_key_press} from "/static/js/search.js";
    document.getElementById("search_key").onkeypress = on_key_press;
    document.getElementById("search_button").onclick = search;
</script>

% include("footer.tpl")
