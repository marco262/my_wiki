% rebase("common/base.tpl", title="Magic Item Filter")
% from math import ceil
% from src.common.utils import ordinal
% from data.dnd.enums import classes, magic_item_types, magic_item_rarities, magic_item_sources
<table>
    <tr valign="top">
        <td>
            <b>Type:</b><br>
            <input type="checkbox" name="checkbox-all" value="type" checked><i>(All/None)</i><br>
            % for t in magic_item_types:
                <input type="checkbox" name="checkbox-type" value="{{t.lower()}}" checked>{{t}}<br>
            % end
        </td>
        <td>
            <b>Rarity:</b><br>
            <input type="checkbox" name="checkbox-all" value="rarity" checked><i>(All/None)</i><br>
            % for r in magic_item_rarities:
                <input type="checkbox" name="checkbox-rarity" value="{{r.lower()}}" checked>{{r}}<br>
            % end
        </td>
        <td>
            <b>Minor/Major:</b><br>
            <input type="checkbox" name="checkbox-all" value="minor-major" checked><i>(All/None)</i><br>
            <input type="checkbox" name="checkbox-minor-major" value="minor" checked>Minor<br>
            <input type="checkbox" name="checkbox-minor-major" value="major" checked>Major<br>
        </td>
        <td>
            <b>Requires<br>attunement?:</b><br>
            <input type="radio" name="radio-attunement" value="true">Yes<br>
            <input type="radio" name="radio-attunement" value="false">No<br>
            <input type="radio" name="radio-attunement" value="both" checked>Both
        </td>
        <td>
            <b>Class Restrictions:</b><br>
            <input type="checkbox" name="checkbox-all" value="classes" checked><i>(All/None)</i><br>
            <input type="checkbox" name="checkbox-classes" value="no-restrictions" checked>(no restrictions)<br>
            <input type="checkbox" name="checkbox-classes" value="spellcaster" checked>(spellcaster)<br>
            % for c in classes:
                <input type="checkbox" name="checkbox-classes" value="{{c.lower()}}" checked>{{c.title()}}<br>
            % end
        </td>
        <td>
            <b>Source:</b><br>
            <input type="checkbox" name="checkbox-all" value="source" checked><i>(All/None)</i><br>
            % for o in magic_item_sources:
                <input type="checkbox" name="checkbox-source" value="{{o}}" checked>{{o}}<br>
            % end
        </td>
    </tr>
</table>

<div id="show-advanced-block">Show subtype options</div>
<div id="advanced-block" style="display: none">
    <div id="hide-advanced-block">Hide subtype options</div>
    <b>Subtype:</b><br>
    <table class="no-border">
        <tr>
            <td>
                <input type="checkbox" name="checkbox-all" value="subtype" checked><i>(All/None)</i><br>
                <input type="checkbox" name="checkbox-subtype" value="no-subtype" checked>(no subtype)<br>
                % subtypes = ["", ""] + subtypes  # Account for the (All/None) and (no subtype) checkboxes
                % sublist_length = ceil(len(subtypes) / 3)
                % for s in subtypes[2:sublist_length]:
                    <input type="checkbox" name="checkbox-subtype" value="{{s}}" checked>{{s}}<br>
                % end
            </td>
            <td>
                % for s in subtypes[sublist_length:sublist_length * 2]:
                    <input type="checkbox" name="checkbox-subtype" value="{{s}}" checked>{{s}}<br>
                % end
            </td>
            <td>
                % for s in subtypes[sublist_length * 2:]:
                    <input type="checkbox" name="checkbox-subtype" value="{{s}}" checked>{{s}}<br>
                % end
            </td>
        </tr>
    </table>
</div>

<p>

<input type="button" value="Filter" id="filter_button" />
<input type="button" value="Reset" id="reset_button" />

<p>

<div id="filter_results"><i>Filter results will appear here</i></div>

<script type="module">
    import { init } from "/static/js/dnd/magic_item_filter.js";
    init();
</script>
