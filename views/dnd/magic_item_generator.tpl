% rebase("common/base.tpl", title="Magic Item Generator")

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
<input type="number" id="max_items" min="1" max="20" value="6" size="2" />
<label for="no_duplicates">No duplicates:</label>
<input type="checkbox" id="no_duplicates" value="false"/>
<input type="button" value="Generate" id="generate_button" />
</p>

<div id="generator_results"><i>Magic items will appear here</i></div>

<script type="module">
    import {generate} from "/js/dnd/magic_item_generator.js";
    document.getElementById("generate_button").onclick = generate;
</script>
