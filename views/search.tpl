% include("header.tpl", title="Spell Search")

<h1>Spell Search</h1>

<table>
    <tr>
        <td>Search Key:</td>
        <td>
            <input type="text" style="width:200px;" id="search_key" />
            <input type="button" value="Search" id="search_button" />
        </td>
    </tr>
</table>

<p />

<div id="search_results"><i>Search results will appear here</i></div>

<script type="module">
    import {search, on_key_press} from "/js/search.js";
    document.getElementById("search_key").onkeypress = on_key_press;
    document.getElementById("search_button").onclick = search;
</script>

% include("footer.tpl")
