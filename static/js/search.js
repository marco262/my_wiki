import { ajax_call, spell_table_header, spell_table_row} from "./utils.js";

var key_press_timer;

export function search() {
    let search_key = document.getElementById("search_key").value;
    if (search_key == "") { return; }
    ajax_call("/search_results/" + search_key + "/BRIEF", handle_search_results);
}

export function on_key_press(e) {
    clearTimeout(key_press_timer);
    if (e.key == "Enter") {
        search(this);
        return;
    }
    key_press_timer = setTimeout(search, 1000);
}

function handle_search_results(xhttp) {
    let json = JSON.parse(xhttp.responseText);
    console.log(json);
    let html;
    if (json.length == 0) {
        html = "<i>No Results</i>";
    } else {
        html = "<table border='1'>\n";
        html += spell_table_header();
        for (let i = 0; i < json.length; i++) {
            html += spell_table_row(json[i][0], json[i][1]);
        }
        html += "</table>";
    }
    document.getElementById("search_results").innerHTML = html;
}
