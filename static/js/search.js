function search() {
    let search_key = document.getElementById("search_key").value;
    if (search_key == "") { return; }
    get_search_results(search_key);
}

function get_search_results(search_key) {
    let xhttp;
    xhttp=new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            handle_search_results(this);
        }
    };
    xhttp.open("GET", "/search_results/" + search_key, true);
    xhttp.send();
}

function handle_search_results(xhttp) {
    let json = JSON.parse(xhttp.responseText);
    console.log(json);
    if (json.length == 0) {
        html = "<i>No Results</i>"
    } else {
        html = "<ul>\n";
        for (i = 0; i < json.length; i++) {
            html += `<li><a href="spell/${json[i][0]}">${json[i][1]}</a></li>\n`;
        }
        html += "</ul>";
    }
    document.getElementById("search_results").innerHTML = html;
}

function on_key_press(e) {
    if (e.key == "Enter") {
        search(this);
    }
}