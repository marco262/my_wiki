import {ajax_call} from "../common/utils.js";

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
    ajax_call("/curse_of_strahd/play_tarokka", null, params)
}

function load_websocket() {
    let loc = window.location;
    let ws_uri = (loc.protocol === "https:") ? "wss:" : "ws:";
    ws_uri += `//${loc.host}/curse_of_strahd/tarokka_websocket`;
    ws = new WebSocket(ws_uri);
    ws.onmessage = handle_websocket;
    ws.onerror = on_websocket_error;
    console.log(`Loaded websocket`);
}

function on_websocket_error(error) {
    console.error("WebSocket error:");
    console.error(error);
    websocket_errors += 1;
    if (websocket_errors >= max_websocket_errors) {
        document.getElementById("grid").hidden = true;
        let error_msg = document.getElementById("error-message");
        error_msg.innerText = `Failed to connect to WebSocket after ${websocket_errors} attempts. ` +
            `Please reload page to try again.`;
        error_msg.hidden = false;
        return;
    }
    console.log("Reconnecting in 5 seconds...");
    setTimeout(load_websocket, 5000);
}

function handle_websocket(msg) {
    websocket_errors = 0;
    console.log(msg);
    let json = JSON.parse(msg.data);
    console.log(json);
    if (json["action"] === "deal") {
        deal_cards();
    } else if (json["action"] === "flip") {
        flip_card(json["data"]);
    } else if (json["action"] === "reset") {
        reset_cards();
    } else if (json["action"] === "set") {
        set_cards(json["data"]);
    } else {
        console.error(`Unknown action: ${json["action"]}`);
    }
}
