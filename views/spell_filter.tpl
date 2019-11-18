% include("header.tpl", title="Spell Filter")
% from utils import ordinal
<h1>Spell Filter</h1>

<table>
    <tr valign="top">
        <td>
        <input type="checkbox" id="checkbox-class-all" checked><i>All/None</i><br>
        % classes = ["bard", "cleric", "druid", "paladin", "ranger", "sorcerer", "warlock", "wizard"]
        % for c in classes:
            <input type="checkbox" name="checkbox-class" value="{{c}}" checked>{{c.title()}} Spells<br>
        % end
        </td>
        <td>
        <input type="checkbox" id="checkbox-level-all" checked><i>All/None</i><br>
        % levels = ["cantrip", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
        % for l in levels:
            <input type="checkbox" name="checkbox-level" value="{{l}}" checked>{{ordinal(l)}}<br>
        % end
        </td>
        <td>
        <input type="checkbox" id="checkbox-school-all" checked><i>All/None</i><br>
        % schools = ["abjuration", "conjuration", "divination", "evocation", "enchantment", "illusion", "necromancy", "transmutation"]
        % for s in schools:
            <input type="checkbox" name="checkbox-school" value="{{s}}" checked>{{s.title()}}<br>
        % end
        </td>
    </tr>
</table>
<br>
<table>
<%
toggles = [
    ("Concentration Spells:", "concentration"),
    ("Ritual Spells:", "ritual"),
    ("Verbal Component:", "verbal"),
    ("Somatic Component:", "somatic"),
    ("Material Component:", "material"),
    ("Expensive Material:", "expensive"),
    ("Material Consumed:", "consumed")
]
for title, name in toggles:
%>
    <tr>
        <td>{{title}}</td>
        <td>
            <input type="radio" name="radio-{{name}}" value="both" checked="true">Both
                <input type="radio" name="radio-{{name}}" value="yes">Yes
                <input type="radio" name="radio-{{name}}" value="no">No
        </td>
    </tr>
% end
</table>

<p />

<input type="button" value="Filter" id="filter_button" />

<p />

<div id="filter_results"><i>Filter results will appear here</i></div>

<script type="module">
    import { init_events } from "/static/js/filter.js";
    init_events();
</script>

% include("footer.tpl")
