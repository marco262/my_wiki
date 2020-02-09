import { ajax_call } from "../../js/utils.js";

let key_press_timer;

export function generate() {
    clearTimeout(key_press_timer);
    let selected = document.getElementById("selected_mutation").value;
    if (selected === "") return;
    ajax_call("/numenera/mutations_generator_results", handle_generator_results, {"selected": selected});
}

export function on_key_press(e) {
    clearTimeout(key_press_timer);
    if (e.key === "Enter") {
        search(this);
        return;
    }
    key_press_timer = setTimeout(search, 1000);
}

function handle_generator_results(xhttp) {
    document.getElementById("generator_results").innerHTML = xhttp.responseText;
}
