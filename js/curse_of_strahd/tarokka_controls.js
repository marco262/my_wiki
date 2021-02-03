import {ajax_call, get_w_default} from "../common/utils.js";

export function init() {
    document.getElementById("deal-button").onclick = () => { send_to_websocket("deal"); };
    document.getElementById("flip-all-button").onclick = () => { send_to_websocket("flip", "all"); };
    document.getElementById("reset-button").onclick = () => { send_to_websocket("reset"); };
    document.getElementById("set-reading-button").onclick = () => {
        send_to_websocket("set_from_file", document.getElementById("reading-name").value);
    };
    document.getElementById("set-random-reading-button").onclick = () => { send_to_websocket("set_random_reading", null); };
    send_to_websocket("get_sync_data");
}

function send_to_websocket(action, data=null) {
    let params = {
        "action": action,
        "data": data
    }
    ajax_call("/curse_of_strahd/play_tarokka", handle_sync, params)
}

function handle_sync(data) {
    console.log(JSON.parse(data.response));
    for (const [key, card_dict] of Object.entries(JSON.parse(data.response))) {
        console.log(key);
        const card = document.getElementById(key);
        card.src = `/static/img/tarokka/${card_dict["card"]}.png`;
        document.getElementById(`inverted-${key}`).checked = get_w_default(card_dict, "inverted", false);
        document.getElementById(`off-grid-${key}`).checked = get_w_default(card_dict, "off-grid", true);
        document.getElementById(`flipped-${key}`).checked = get_w_default(card_dict, "flipped", false);
    }
}
