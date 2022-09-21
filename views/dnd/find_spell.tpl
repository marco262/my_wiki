% rebase("common/base.tpl", title="Find a Spell")

<p>
Spell Name (partial matches allowed):
<input type="text" style="width: 200px;" id="search_key" />
<input type="button" value="Search" id="search_button" />
</p>

<div id="search_results"><i>Search results will appear here</i></div>

<script type="module">
    import {search, on_key_press} from "/static/js/dnd/find_spell.js";
    document.getElementById("search_key").focus();
    document.getElementById("search_key").onkeypress = on_key_press;
    document.getElementById("search_button").onclick = search;
</script>
