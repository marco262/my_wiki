% include("header.tpl", title="Spell Search")

<h1>Spell Search</h1>

<table>
    <tr>
        <td>Key:</td>
        <td><input type="text" style="width:100px;" id="search_key" value="" /> <input type="button" value="Search" onclick="search()" /></td>
    </tr>
</table>

<p />

<div id="search_results"><i>Search results will appear here</i></div>

<script>

function search() {
    var search_key = document.getElementById("search_key").value;
    get_search_results(search_key);
}

function get_search_results(search_key) {
    var xhttp;
    xhttp=new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            handle_search_results(this);
        }
    };
    xhttp.open("GET", "search_results/" + search_key, true);
    xhttp.send();
}

function handle_search_results(xhttp) {
    var json = JSON.parse(xhttp.responseText);
    console.log(json);
    if (json.length == 0) {
        html = "<i>No Results</i>"
    } else {
        html = "<ul>\n"
        for (i = 0; i < json.length; i++) {
            html += `<li><a href="spell/${json[i][0]}">${json[i][1]}</a></li>\n`;
        }
        html += "</ul>"
    }
    document.getElementById("search_results").innerHTML = html;
}

</script>

% include("footer.tpl")
