% rebase("common/base.tpl", title="Magic Item Generator")
% from math import ceil
% from data.dnd.enums import classes, magic_item_types, magic_item_rarities, magic_item_sources

<p>
<label for="magic-item-tables">Select a magic item table:</label>
<select name="magic-item-tables" id="magic-item-tables">
    <option value="A">Magic Item Table A (Common)</option>
    <option value="B">Magic Item Table B (Minor Uncommon)</option>
    <option value="C">Magic Item Table C (Minor Rare)</option>
    <option value="D">Magic Item Table D (Minor Very Rare)</option>
    <option value="E">Magic Item Table E (Minor Legendary)</option>
    <option value="F">Magic Item Table F (Major Uncommon)</option>
    <option value="G">Magic Item Table G (Major Rare)</option>
    <option value="H">Magic Item Table H (Major Very Rare)</option>
    <option value="I">Magic Item Table I (Major Legendary)</option>
</select>
<label for="max_items"># Items:</label>
<input type="number" id="max_items" min="1" max="20" value="6" size="4" />
<label for="no_duplicates">No duplicates:</label>
<input type="checkbox" id="no_duplicates" value="false"/>
<input type="button" value="Generate" id="generate_button" />
</p>

<div id="show-advanced-block">Show advanced options</div>
<div id="advanced-block" style="display: none">
    <div id="hide-advanced-block">Hide advanced options</div>
    <table>
        <tr valign="top">
            <td>
                <b>Type:</b><br>
                <input type="checkbox" name="checkbox-all" value="type" checked><i>(All/None)</i><br>
                % for t in magic_item_types:
                    <input type="checkbox" name="checkbox-type" value="{{t}}" checked>{{t}}<br>
                % end
            </td>
            <td hidden>
                <b>Rarity:</b><br>
                <input type="checkbox" name="checkbox-all" value="rarity" checked><i>(All/None)</i><br>
                % for r in magic_item_rarities:
                    <input type="checkbox" name="checkbox-rarity" value="{{r}}" checked>{{r}}<br>
                % end
            </td>
            <td hidden>
                <b>Minor/Major:</b><br>
                <input type="checkbox" name="checkbox-all" value="minor-major" checked><i>(All/None)</i><br>
                <input type="checkbox" name="checkbox-minor-major" value="Minor" checked>Minor<br>
                <input type="checkbox" name="checkbox-minor-major" value="Major" checked>Major<br>
            </td>
            <td>
                <b>Requires<br>attunement?:</b><br>
                <input type="radio" name="radio-attunement" value="yes">Yes<br>
                <input type="radio" name="radio-attunement" value="no">No<br>
                <input type="radio" name="radio-attunement" value="both" checked>Both
            </td>
            <td>
                <b>Class Restrictions:</b><br>
                <input type="checkbox" name="checkbox-all" value="classes" checked><i>(All/None)</i><br>
                <input type="checkbox" name="checkbox-classes" value="no-restrictions" checked>(no restrictions)<br>
                % for c in classes:
                    <input type="checkbox" name="checkbox-classes" value="{{c}}" checked>{{c.title()}}<br>
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
    <input type="button" value="Reset" id="reset_button" />
</div>

<div id="generator_results">
    <p><i>Magic items will appear here</i></p>
</div>

<hr>

<p>
    See <a href="/dnd/general/Downtime Activities#buying-a-magic-item">Buying a Magic Item</a> for prices for buying magic items.<br>
    See <a href="/dnd/general/Downtime Activities#scribing-a-spell-scroll">Scribing a Spell Scroll</a> for Spell Scroll costs.
    I recommend rounding up to the next whole magnitude (e.g. 2,500gp -> 3,000gp) to cover the seller's profit margin.
</p>

<script type="module">
    import { init } from "/static/js/dnd/magic_item_generator.js";
    init();
</script>
