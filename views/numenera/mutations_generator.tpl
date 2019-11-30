% include("header.tpl", title="Spell Search")

<h1>Spell Search</h1>

<table border="0">
    <tr>
        <td>Search Key:</td>
        <td>
            <form action="/numenera/mutations_generator_results">
                <input list="browsers">
                <datalist id="browsers">
                    <option value="Internet Explorer">
                    <option value="Firefox">
                    <option value="Chrome">
                    <option value="Opera">
                    <option value="Safari">
                </datalist>
            </form>
            <select>
              <option value="volvo">Volvo</option>
              <option value="saab">Saab</option>
              <option value="mercedes">Mercedes</option>
              <option value="audi">Audi</option>
            </select>
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
