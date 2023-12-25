% rebase("common/base.tpl", title="Spell Filter")
% from src.common.utils import ordinal
% from data.onednd.enums import spell_classes, spell_levels, schools, casting_times, ranges, durations, sources
<table border="0">
    <tr valign="top">
        <td>
            <b>Class:</b><br>
            <input type="checkbox" name="checkbox-all" value="class" checked><i>All/None</i><br>
            % for c in spell_classes:
                <input type="checkbox" name="checkbox-class" value="{{c}}" checked>{{c.title()}} Spells<br>
            % end
        </td>
        <td>
            <b>Level:</b><br>
            <input type="checkbox" name="checkbox-all" value="level" checked><i>All/None</i><br>
            % for l in spell_levels:
                % if l == "0":
                %   level_name = "Cantrip"
                % else:
                %   level_name = ordinal(l) + " Level"
                % end
                <input type="checkbox" name="checkbox-level" value="{{l}}" checked>{{level_name}}<br>
            % end
        </td>
        <td>
            <b>School:</b><br>
            <input type="checkbox" name="checkbox-all" value="school" checked><i>All/None</i><br>
            % for s in schools:
                <input type="checkbox" name="checkbox-school" value="{{s}}" checked>{{s.title()}}<br>
            % end
        </td>
        <td>
            <b>Casting Time:</b><br>
            <input type="checkbox" name="checkbox-all" value="casting-time" checked><i>All/None</i><br>
            % for t in casting_times:
                <input type="checkbox" name="checkbox-casting-time" value="{{t}}" checked>{{t}}<br>
            % end
        </td>
        <td>
            <b>Range:</b><br>
            <input type="checkbox" name="checkbox-all" value="range" checked><i>All/None</i><br>
            % for t in ranges:
                <input type="checkbox" name="checkbox-range" value="{{t}}" checked>{{t}}<br>
            % end
        </td>
        <td>
            <b>Duration:</b><br>
            <input type="checkbox" name="checkbox-all" value="duration" checked><i>All/None</i><br>
            % for t in durations:
                <input type="checkbox" name="checkbox-duration" value="{{t}}" checked>{{t}}<br>
            % end
        </td>
        <td>
            <b>Source:</b><br>
            <input type="checkbox" name="checkbox-all" value="source" checked><i>All/None</i><br>
            % for o in sources:
                <input type="checkbox" name="checkbox-source" value="{{o}}" checked>{{o}}<br>
            % end
        </td>
    </tr>
</table>
<br>
<div id="show-advanced-block">Show advanced filter options</div>
<div id="advanced-block" style="display: none">
    <table border="0">
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
    <div id="hide-advanced-block">Hide advanced filter options</div>
</div>

<p>

<input type="button" value="Filter" id="filter_button" />
<input type="button" value="Reset" id="reset_button" />

<p>

<div id="filter_results"><i>Filter results will appear here</i></div>

<script type="module">
    import { init_events } from "/static/js/onednd/spell_filter.js";
    init_events();
</script>
