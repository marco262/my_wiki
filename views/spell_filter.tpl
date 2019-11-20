% include("header.tpl", title="Spell Filter")
% from utils import ordinal
% from data.enums import classes, spell_levels, schools
<h1>Spell Filter</h1>

<table>
    <tr valign="top">
        <td>
        <input type="checkbox" id="checkbox-class-all" checked><i>All/None</i><br>
        % for c in classes:
            <input type="checkbox" name="checkbox-class" value="{{c}}" checked>{{c.title()}} Spells<br>
        % end
        <br>
        <input type="checkbox" id="checkbox-ua-spells" checked>Include Expanded<br>
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;spell lists from<br>
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Unearthed Arcana
        </td>
        <td>
        <input type="checkbox" id="checkbox-level-all" checked><i>All/None</i><br>
        % for l in spell_levels:
            <input type="checkbox" name="checkbox-level" value="{{l}}" checked>{{ordinal(l)}}<br>
        % end
        </td>
        <td>
        <input type="checkbox" id="checkbox-school-all" checked><i>All/None</i><br>
        % for s in schools:
            <input type="checkbox" name="checkbox-school" value="{{s}}" checked>{{s.title()}}<br>
        % end
        </td>
    </tr>
</table>
<br>
<div id="show-advanced-block" style="font-size: small"><a href="#">Show advanced filter options</a></div>
<div id="advanced-block" style="display: none">
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
                <input type="radio" name="radio-{{name}}" value="both" checked>Both
                    <input type="radio" name="radio-{{name}}" value="yes">Yes
                    <input type="radio" name="radio-{{name}}" value="no">No
            </td>
        </tr>
    % end
    </table>
    <div id="hide-advanced-block" style="font-size: small"><a href="#">Hide advanced filter options</a></div>
</div>

<p />

<input type="button" value="Filter" id="filter_button" />

<p />

<div id="filter_results"><i>Filter results will appear here</i></div>

<script type="module">
    import { init_events } from "/js/filter.js";
    init_events();
</script>

% include("footer.tpl")
