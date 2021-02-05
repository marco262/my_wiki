import {ajax_call, get_w_default} from "../common/utils.js";

export function init() {
    for (const element of document.getElementsByClassName("inverted-checkbox")) {
        element.onclick = () => { handle_checkbox(element, "invert"); };
    }
    for (const element of document.getElementsByClassName("off-grid-checkbox")) {
        element.onclick = () => { handle_checkbox(element, "deal"); };
    }
    for (const element of document.getElementsByClassName("flipped-checkbox")) {
        element.onclick = () => { handle_checkbox(element, "flip"); };
    }
    document.getElementById("deal-button").onclick = () => {
        send_to_websocket("deal", JSON.stringify({"position": "all", "state": false}));  // Sets 'off-grid' value
    };
    document.getElementById("show-all-button").onclick = () => {
        send_to_websocket("flip", JSON.stringify({"position": "all", "state": true}));
    };
    document.getElementById("hide-all-button").onclick = () => {
        send_to_websocket("flip", JSON.stringify({"position": "all", "state": false}));
    };
    document.getElementById("reset-button").onclick = () => { send_to_websocket("reset"); };
    document.getElementById("set-reading-button").onclick = () => {
        send_to_websocket("set_from_file", document.getElementById("reading-name").value);
    };
    document.getElementById("set-random-reading-button").onclick = () => { send_to_websocket("set_random_reading"); };
    document.getElementById("sync-button").onclick = () => { send_to_websocket("get_sync_data"); };
    send_to_websocket("get_sync_data");
}

function handle_checkbox(element, action) {
    send_to_websocket(action, JSON.stringify({"position": element.value, "state": element.checked}));
}

function send_to_websocket(action, data=null) {
    let params = {
        "action": action,
        "data": data
    }
    ajax_call("/curse_of_strahd/play_tarokka", handle_sync, params)
}

function handle_sync(data) {
    console.debug(JSON.parse(data.response));
    for (const [key, card_dict] of Object.entries(JSON.parse(data.response))) {
        const card = document.getElementById(key);
        card.src = `/static/img/tarokka/${card_dict["card"]}.png`;
        document.getElementById(`inverted-${key}`).checked = get_w_default(card_dict, "inverted", false);
        document.getElementById(`off-grid-${key}`).checked = get_w_default(card_dict, "off-grid", true);
        document.getElementById(`flipped-${key}`).checked = get_w_default(card_dict, "flipped", false);
    }
}
