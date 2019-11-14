import { ajax_call, title_case } from "./utils.js";

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
        html += spell_header();
        for (let i = 0; i < json.length; i++) {
            html += spell_row(json[i][0], json[i][1]);
        }
        html += "</table>";
    }
    document.getElementById("search_results").innerHTML = html;
}

function spell_header() {
    return `<tr>
        <th>Spell Name</th>
        <th>School</th>
        <th>Bard</th>
        <th>Cleric</th>
        <th>Druid</th>
        <th>Paladin</th>
        <th>Ranger</th>
        <th>Sorcerer</th>
        <th>Warlock</th>
        <th>Wizard</th>
        <th>Source</th>
    </tr>\n`
}

function spell_row(url, dict) {
    let ar = ["bard", "cleric", "druid", "paladin", "ranger", "sorcerer", "warlock", "wizard"];
    ar = ar.map(classname => `<td>${dict["classes"].includes(classname) ? "X" : ""}</td>`);
    return `<tr>
        <td><a href="spell/${url}">${dict["title"]}</a></td>
        <td>${title_case(dict["school"])}</td>
        ${ar.join("\n")}
        <td>${dict["source"]}</td>
    </tr>\n`;
}
