import {get_tarokka_data} from "./tarokka_data.js";
import {ajax_call, get_w_default} from "../common/utils.js";

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
const card_order = ["middle", "bottom", "left", "top", "right"];

let websocket_errors = 0;
let max_websocket_errors = 3;
let ws = null;

let tarokka_data = get_tarokka_data();

export function init() {
    for (const [key, element] of Object.entries(flip_card_inner_elements)) {
        document.getElementById(key).onclick = function (event) {
            send_to_websocket("flip", JSON.stringify({"position": key, "state": !element.classList.contains("flipped")}));
        };
    }
    for (const element of document.getElementsByClassName("card-front")) {
        element.onmouseover = () => { set_info_box(element); };
    }
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
    console.debug(msg);
    let json = JSON.parse(msg.data);
    if (json["action"] === "sync") {
        sync_cards(json["data"]);
    } else if (json["action"] === "deal") {
        deal_cards(json["data"]);
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
        card_img.alt = card_dict["card"];
    }
}

function deal_cards(data) {
    console.log(`Dealing cards ${data}`);
    const json = JSON.parse(data);
    let next_delay = 0;
    for (const key of card_order) {
        let card = flip_card_inner_elements[key];
        if ((json["position"] === "all" || json["position"] === key) && json["state"] !== card.classList.contains("off-grid")) {
            setTimeout(function () {
                card_deal_sfx.play();
                card.classList.toggle("off-grid", json["state"]);
            }, next_delay);
            next_delay += 1000;
        }
    }
}

function flip_card(data) {
    console.log(`Flipping card ${data}`);
    const json = JSON.parse(data);
    let next_delay = 0;
    for (const key of card_order) {
        let card = flip_card_inner_elements[key];
        if ((json["position"] === "all" || json["position"] === key) && json["state"] !== card.classList.contains("flipped")) {
            setTimeout(function () {
                card_flip_sfx.play();
                card.classList.toggle("flipped", json["state"]);
            }, next_delay);
            next_delay += 1000;
        }
    }
}

function hide_cards() {
    let cards_flipped = false;
    for (const key of card_order) {
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
        for (const key of card_order) {
            let card = flip_card_inner_elements[key];
            card.classList.toggle("off-grid", true);
        }
    }, reset_delay);
    return reset_delay;
}

function set_info_box(element) {
    document.getElementById("card-info").hidden = false;
    const card_position = element.id.substring(9);
    document.getElementById("prophecy_summary").innerText = tarokka_data[card_position]["prophecy"];
    document.getElementById("vibe_check_summary").innerText = tarokka_data[card_position]["vibe_check"];
    const card_name = element.alt;
    document.getElementById("card-name").innerText = card_name;
    let suit_description;
    if (card_name.includes("High Deck"))
        suit_description = tarokka_data["High Deck"];
    else if (card_name.includes("of Swords"))
        suit_description = tarokka_data["Swords Suit"];
    else if (card_name.includes("of Stars"))
        suit_description = tarokka_data["Stars Suit"];
    else if (card_name.includes("of Coins"))
        suit_description = tarokka_data["Coins Suit"];
    else if (card_name.includes("of Glyphs"))
        suit_description = tarokka_data["Glyphs Suit"];
    document.getElementById("suit-description").innerText = suit_description;
    document.getElementById("card-description").innerText = tarokka_data[card_name];
}

function send_to_websocket(action, data=null) {
    let params = {
        "action": action,
        "data": data
    }
    ajax_call("/curse_of_strahd/play_tarokka", null, params)
}
