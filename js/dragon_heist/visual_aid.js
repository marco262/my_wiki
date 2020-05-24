let websocket_errors = 0;
let max_websocket_errors = 3;
let last_url = "";
let ws_dict = {};

export function init() {
    load_websocket("get_visual_aid", handle_visual_aid);
    window.addEventListener("beforeunload", event => {
        console.log("Closing websockets");
        for (let [key, value] of Object.entries(ws_dict)) {
            value.close();
        }
    });
}

function load_websocket(url, func) {
    let loc = window.location;
    let ws_uri = (loc.protocol === "https:") ? "wss:" : "ws:";
    ws_uri += `//${loc.host}/dragon_heist/${url}`;
    let ws = new WebSocket(ws_uri);
    ws.onmessage = func;
    ws.onerror = on_websocket_error;
    ws_dict[url] = ws;
}

function on_websocket_error(error) {
    console.log("WebSocket error:");
    console.log(error);
    websocket_errors += 1;
    if (websocket_errors >= max_websocket_errors) {
        document.getElementById("page").hidden = true;
        let error_msg = document.getElementById("error-message");
        error_msg.innerText = `Failed to connect to WebSocket after ${websocket_errors} attempts. Please reload page to try again.`;
        error_msg.hidden = false;
        return
    }
    console.log("Reconnecting in 5 seconds...");
    setTimeout(load_websocket, 5000);
}

function handle_visual_aid(msg) {
    // console.log(msg);
    let response = msg.data;
    // console.log(response);
    let json = JSON.parse(response);
    let url = json["url"];
    // console.log(url);
    websocket_errors = 0;
    if (url !== last_url) {
        console.log("Setting img src: " + url);
        document.getElementById("picture").style.backgroundImage = "url('" + url + "')";
        // document.getElementById("picture").src = url;
        last_url = url;
    }
}