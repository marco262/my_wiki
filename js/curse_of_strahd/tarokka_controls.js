import {ajax_call} from "../common/utils.js";

let ws;
let websocket_errors = 0;
const max_websocket_errors = 3;

export function init() {
    document.getElementById("deal-button").onclick = () => { send_to_websocket("deal"); };
    document.getElementById("flip-all-button").onclick = () => { send_to_websocket("flip", "all"); };
    document.getElementById("flip-top-button").onclick = () => { send_to_websocket("flip", "top"); };
    document.getElementById("flip-left-button").onclick = () => { send_to_websocket("flip", "left"); };
    document.getElementById("flip-middle-button").onclick = () => { send_to_websocket("flip", "middle"); };
    document.getElementById("flip-right-button").onclick = () => { send_to_websocket("flip", "right"); };
    document.getElementById("flip-bottom-button").onclick = () => { send_to_websocket("flip", "bottom"); };
    document.getElementById("reset-button").onclick = () => { send_to_websocket("reset"); };
    document.getElementById("set-reading-button").onclick = () => {
        send_to_websocket("set_from_file", document.getElementById("reading-name").value);
    };
    document.getElementById("set-random-reading-button").onclick = () => { send_to_websocket("set_random_reading", null); };
}

function send_to_websocket(action, data=null) {
    let params = {
        "action": action,
        "data": data
    }
    ajax_call("/curse_of_strahd/play_tarokka", handle_sync, params)
}

function handle_sync(data) {
    console.log(data);
}
