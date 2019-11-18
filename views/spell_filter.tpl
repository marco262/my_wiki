% include("header.tpl", title="Spell Search")
% from utils import ordinal
<h1>Spell Filter</h1>

<table border=1>
    <tr valign="top">
        <td>
        % classes = ["bard", "cleric", "druid", "paladin", "ranger", "sorcerer", "warlock", "wizard"]
        % for c in classes:
            <input type="checkbox" id="checkbox-class-{{c}}">{{c.title()}} Spells<br>
        % end
        </td>
        <td>
        % levels = ["cantrip", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
        % for l in levels:
            <input type="checkbox" id="checkbox-level-{{l}}">{{ordinal(l)}}<br>
        % end
        </td>
        <td>
        % schools = ["abjuration", "conjuration", "divination", "evocation", "enchantment", "illusion", "necromancy", "transmutation"]
        % for s in schools:
            <input type="checkbox" id="checkbox-school-{{s}}">{{s.title()}}<br>
        % end
        </td>
        <td>
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
        </td>
    </tr>
</table>

<p />

<input type="button" value="Filter" id="filter_button" />

<p />

<div id="filter_results"><i>Filter results will appear here</i></div>

<script type="module">
    import {filter, on_click} from "/static/js/filter.js";
    document.getElementById("filter_button").onclick = filter;
</script>

% include("footer.tpl")
