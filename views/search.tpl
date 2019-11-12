% include("header.tpl", title="Spell Search")

<script type="application/javascript" src="/static/js/search.js"></script>

<h1>Spell Search</h1>

<table>
    <tr>
        <td>Search Key:</td>
        <td>
            <input type="text" style="width:200px;" id="search_key" onkeypress="on_key_press(event)"/>
            <input type="button" value="Search" onclick="search()" />
        </td>
    </tr>
</table>

<p />

<div id="search_results"><i>Search results will appear here</i></div>

% include("footer.tpl")
