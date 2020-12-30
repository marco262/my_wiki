const card_deal_sfx = document.getElementById("card-deal-effect");
card_deal_sfx.volume = 0.6;
const card_flip_sfx = document.getElementById("card-flip-effect");
card_flip_sfx.volume = 0.6;

let flip_card_inner_elements = [
    document.getElementById("flip-card-inner-left"),
    document.getElementById("flip-card-inner-top"),
    document.getElementById("flip-card-inner-right"),
    document.getElementById("flip-card-inner-bottom"),
    document.getElementById("flip-card-inner-middle")
]

let websocket_errors = 0;
let max_websocket_errors = 3;
let ws = null;

export function init() {
    // Array.prototype.forEach.call(flip_card_inner_elements, function (element) {
    //     element.onclick = function (event) {
    //         card_flip_sfx.play();
    //         element.classList.toggle("flipped");
    //     };
    // });
    load_websocket();
}

function load_websocket() {
    let loc = window.location;
    let ws_uri = (loc.protocol === "https:") ? "wss:" : "ws:";
    ws_uri += `//${loc.host}/curse_of_strahd/tarokka_websocket`;
    ws = new WebSocket(ws_uri);
    ws.onmessage = handle_websocket;
    ws.onerror = on_websocket_error;
    console.log(`Loaded websocket`)
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
    if (json["action"] === "deal") {
        deal_cards();
    } else if (json["action"] === "flip") {
        flip_card(json["target"]);
    } else if (json["action"] === "reset") {
        reset_cards();
    } else {
        console.error(json);
    }
}

function deal_cards() {
    console.log("Dealing cards");
    let next_delay = 0;
    for (let i = 0; i < flip_card_inner_elements.length; i++) {
        if (flip_card_inner_elements[i].classList.contains("off-grid")) {
            setTimeout(function () {
                card_deal_sfx.play();
                flip_card_inner_elements[i].classList.toggle("off-grid", false);
            }, next_delay);
            next_delay += 750;
        }
    }
}

function flip_card(target) {
    console.log(`Flipping card ${target}`);
    let next_delay = 0;
    for (let i = 0; i < flip_card_inner_elements.length; i++) {
        if (target === "all" || target === i.toString()) {
            setTimeout(function () {
                card_flip_sfx.play();
                flip_card_inner_elements[i].classList.toggle("flipped");
            }, next_delay);
            next_delay += 750;
        }
    }
}

function reset_cards() {
    console.log("Resetting cards");
    let reset_delay = 0;
    for (let i=0; i < flip_card_inner_elements.length; i++) {
        if (flip_card_inner_elements[i].classList.contains("flipped")) {
            reset_delay = 750;
            flip_card_inner_elements[i].classList.toggle("flipped", false);
        }
    }
    if (reset_delay > 0) {
        card_flip_sfx.play();
    }
    setTimeout(function () {
        for (let i = 0; i < flip_card_inner_elements.length; i++) {
            flip_card_inner_elements[i].classList.toggle("off-grid", true);
        }
    }, reset_delay);
}
