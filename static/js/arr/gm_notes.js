import {ajax_call} from "/static/js/common/utils.js";

export function init_gm_notes_inserts() {
    document.querySelectorAll("details.gm-notes").forEach(e => e.addEventListener(
        "toggle", function() { on_insert_toggle(e) }
    ));
}

function on_insert_toggle(e) {
    console.log(`Toggle! ${e.open} ${e.insert_loaded}`);
    // Only process when the insert is opened
    if (!e.open || e.insert_loaded) {
        return;
    }
    // Set loading text...
    let p = document.createElement("p");
    p.innerHTML = "<i>Loading...</i>";
    e.appendChild(p);
    // Fetch the gm_notes insert
    ajax_call(
        `/arr/gm_notes/insert/${e.id}`,
        function (xhttp){ load_insert(e, xhttp) },
        null,
        function (xhttp) { insert_error(e, xhttp) }
    );
}

function load_insert(e, xhttp) {
    console.log(e, xhttp);
    e.removeChild(e.lastChild);
    e.innerHTML += xhttp.response;
    // Only load the insert once
    e.insert_loaded = true;
}

function insert_error(e, xhttp) {
    console.log(e, xhttp);
    e.lastChild.innerHTML = "<i>You must sign in as a GM to view this content</i>";
}