import { ajax_call } from "../common/utils.js";

let timer;

export function generate() {
    clearTimeout(timer);
    let table_name = document.getElementById("magic-item-tables").value;
    if (table_name === "") return;
    let max_items = parseInt(document.getElementById("max_items").value);
    let no_duplicates = document.getElementById("no_duplicates").checked;
    let params = {"table_name": table_name, "max_items": max_items, "no_duplicates": no_duplicates};
    console.log(params);
    ajax_call(
        "/dnd/equipment/magic_item_generator_results/",
        handle_generator_results, 
        params
    );
    timer = setTimeout(set_loading_text, 500);
}

function set_loading_text() {
    document.getElementById("generator_results").innerHTML = "<p><i>Loading results... This will take several seconds the first time this is run because the server hasn't loaded the magic items and spells into memory yet.</i></p>";
}

function handle_generator_results(xhttp) {
    clearTimeout(timer);
    document.getElementById("generator_results").innerHTML = xhttp.responseText;
}
