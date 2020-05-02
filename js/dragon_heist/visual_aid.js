let websocket_errors = 0;
let max_websocket_errors = 3;
let last_url = "";
let ws;

export function init() {
    load_websocket();
    window.addEventListener("beforeunload", event => { ws.close() });
}

function load_websocket() {
    let loc = window.location;
    let ws_uri = (loc.protocol === "https:") ? "wss:" : "ws:";
    ws_uri += "//" + loc.host + "/dragon_heist/get_visual_aid";
    ws = new WebSocket(ws_uri);
    ws.onmessage = handle_visual_aid;
    ws.onerror = on_websocket_error;
}

function on_websocket_error(error) {
    console.log("WebSocket error:");
    console.log(error);
    websocket_errors += 1;
    if (websocket_errors >= max_websocket_errors) {
        document.getElementById("picture").hidden = true;
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