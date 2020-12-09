import { ajax_call } from "../common/utils.js";

export function generate() {
    let table_name = document.getElementById("magic-item-tables").value;
    if (table_name === "") return;
    let max_items = parseInt(document.getElementById("max_items").value);
    let no_duplicates = document.getElementById("no_duplicates").checked;
    let params = {"table_name": table_name, "max_items": max_items, "no_duplicates": no_duplicates};
    console.log(params);
    ajax_call(
        "/dnd/magic_item_generator_results/", 
        handle_generator_results, 
        params
    );
}

function handle_generator_results(xhttp) {
    document.getElementById("generator_results").innerHTML = xhttp.responseText;
}
