import { ajax_call } from "../common/utils.js";

export function generate() {
    let table_name = document.getElementById("magic-item-tables").value;
    if (table_name === "") return;
    ajax_call("/dnd/magic_item_generator_results/" + table_name, handle_generator_results);
}

function handle_generator_results(xhttp) {
    document.getElementById("generator_results").innerHTML = xhttp.responseText;
}
