const card_deal_sfx = document.getElementById("card-deal-effect");
card_deal_sfx.volume = 0.6;
const card_flip_sfx = document.getElementById("card-flip-effect");
card_flip_sfx.volume = 0.6;

let flip_card_inner_elements = {
    "top": document.getElementById("flip-card-inner-top"),
    "left": document.getElementById("flip-card-inner-left"),
    "middle": document.getElementById("flip-card-inner-middle"),
    "right": document.getElementById("flip-card-inner-right"),
    "bottom": document.getElementById("flip-card-inner-bottom")
}

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
    if (json["action"] === "sync") {
        sync_cards(json["data"]);
    } else if (json["action"] === "deal") {
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

function sync_cards(data) {
    console.log(`Syncing cards to ${data}`);
    const json = JSON.parse(data);
    set_cards_inner_func(json);
    for (const [key, card_dict] of Object.entries(json)) {
        let card = flip_card_inner_elements[key];
        card.classList.toggle("off-grid", get_w_default(card_dict, "off-grid", true));
        card.classList.toggle("flipped", get_w_default(card_dict, "flipped", false));
    }
}

function get_w_default(dict, key, def) {
    if (!dict.hasOwnProperty(key))
        return def;
    return dict[key]
}

function set_cards(data) {
    const reset_delay = reset_cards();
    console.log(`Setting cards to ${data}`);
    const json = JSON.parse(data);
    setTimeout(function () {
        set_cards_inner_func(json)
    }, reset_delay);
}

function set_cards_inner_func(json) {
    for (const [key, card_dict] of Object.entries(json)) {
        const card_img = document.getElementById(`card-img-${key}`);
        card_img.src = `/static/img/tarokka/${card_dict["card"]}.png`;
        card_img.classList.toggle("inverted", card_dict["inverted"]);
    }
}

function deal_cards() {
    console.log("Dealing cards");
    let next_delay = 0;
    for (const key of ["top", "left", "middle", "right", "bottom"]) {
        let card = flip_card_inner_elements[key];
        if (card.classList.contains("off-grid")) {
            setTimeout(function () {
                card_deal_sfx.play();
                card.classList.toggle("off-grid", false);
            }, next_delay);
            next_delay += 750;
        }
    }
}

function flip_card(data) {
    console.log(`Flipping card ${data}`);
    let next_delay = 0;
    for (const key of ["top", "left", "middle", "right", "bottom"]) {
        let card = flip_card_inner_elements[key];
        if (data === "all" || data === key) {
            setTimeout(function () {
                card_flip_sfx.play();
                card.classList.toggle("flipped");
            }, next_delay);
            next_delay += 750;
        }
    }
}

function hide_cards() {
    let cards_flipped = false;
    for (const key of ["top", "left", "middle", "right", "bottom"]) {
        let card = flip_card_inner_elements[key];
        if (card.classList.contains("flipped")) {
            cards_flipped = true;
            card.classList.toggle("flipped", false);
        }
    }
    if (cards_flipped) {
        card_flip_sfx.play();
    }
    return cards_flipped;
}

function reset_cards() {
    console.log("Resetting cards");
    let reset_delay = hide_cards() ? 750 : 0;
    setTimeout(function () {
        for (const key of ["top", "left", "middle", "right", "bottom"]) {
            let card = flip_card_inner_elements[key];
            card.classList.toggle("off-grid", true);
        }
    }, reset_delay);
    return reset_delay;
}
