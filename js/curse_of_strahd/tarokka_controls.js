import {ajax_call} from "../common/utils.js";

export function init() {
    document.getElementById("deal-button").onclick = () => { send_to_websocket("deal"); };
    document.getElementById("flip-all-button").onclick = () => { send_to_websocket("flip", "all"); };
    document.getElementById("flip-left-button").onclick = () => { send_to_websocket("flip", 0); };
    document.getElementById("flip-top-button").onclick = () => { send_to_websocket("flip", 1); };
    document.getElementById("flip-right-button").onclick = () => { send_to_websocket("flip", 2); };
    document.getElementById("flip-bottom-button").onclick = () => { send_to_websocket("flip", 3); };
    document.getElementById("flip-middle-button").onclick = () => { send_to_websocket("flip", 4); };
    document.getElementById("reset-button").onclick = () => { send_to_websocket("reset"); };
}

function send_to_websocket(action, target=null) {
    let params = {
        "action": action,
        "target": target
    }
    ajax_call("/curse_of_strahd/play_tarokka", null, params)
}
