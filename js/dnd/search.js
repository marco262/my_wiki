import { ajax_call } from "../common/utils.js";

let key_press_timer;

export function search() {
    clearTimeout(key_press_timer);
    let search_key = document.getElementById("search_key").value;
    if (search_key === "") return;
    ajax_call("/dnd/search_results/" + search_key, handle_search_results);
}

export function on_key_press(e) {
    clearTimeout(key_press_timer);
    if (e.key === "Enter") {
        search(this);
        return;
    }
    key_press_timer = setTimeout(search, 1000);
}

function handle_search_results(xhttp) {
    document.getElementById("search_results").innerHTML = xhttp.responseText;
}
