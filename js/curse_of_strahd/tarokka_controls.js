import {ajax_call, get_w_default} from "../common/utils.js";
import {get_tarokka_data} from "./tarokka_data.js";

let tarokka_data = get_tarokka_data();

export function init() {
    send_to_websocket("get_sync_data");
    for (const element of document.getElementsByClassName("inverted-checkbox")) {
        element.onclick = function() { handle_checkbox(element, "invert"); };
    }
    for (const element of document.getElementsByClassName("off-grid-checkbox")) {
        element.onclick = function() { handle_checkbox(element, "deal"); };
    }
    for (const element of document.getElementsByClassName("flipped-checkbox")) {
        element.onclick = function() { handle_checkbox(element, "flip"); };
    }
    document.getElementById("deal-button").onclick = function() {
        send_to_websocket("deal", JSON.stringify({"position": "all", "state": false}));  // Sets 'off-grid' value
    };
    document.getElementById("show-all-button").onclick = function() {
        send_to_websocket("flip", JSON.stringify({"position": "all", "state": true}));
    };
    document.getElementById("hide-all-button").onclick = function() {
        send_to_websocket("flip", JSON.stringify({"position": "all", "state": false}));
    };
    document.getElementById("reset-button").onclick = function() { send_to_websocket("reset"); };

    document.getElementById("set-reading-button").onclick = function() {
        send_to_websocket("set_from_file", document.getElementById("reading-name").value);
    };

    document.getElementById("set-random-reading-button").onclick = function() {
        send_to_websocket("set_random_reading", "{}");
    };
    document.getElementById("set-random-reading-w-force-button").onclick = function() {
        send_to_websocket("set_random_reading", JSON.stringify(get_forced_cards()));
    };
    document.getElementById("force-cards-button").onclick = function() {
        send_to_websocket("force_cards", JSON.stringify(get_forced_cards()));
    };
    document.getElementById("clear-forced-cards").onclick = clear_forced_cards;

    document.getElementById("sync-button").onclick = function() { send_to_websocket("sync"); };

    add_dropdown_options();
}

function handle_checkbox(element, action) {
    send_to_websocket(action, JSON.stringify({"position": element.value, "state": element.checked}));
}

function send_to_websocket(action, data=null) {
    let params = {
        "action": action,
        "data": data
    }
    console.debug(params);
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

function add_dropdown_options() {
    let dropdown_elements = document.getElementsByClassName("force-card-set");
    for (const [key, description] of Object.entries(tarokka_data["cards"])) {
        for (const element of dropdown_elements) {
            let option = document.createElement("option");
            option.text = `${key} | ${description}`;
            option.value = key;
            element.add(option);
        }
    }
}

function get_forced_cards() {
    let forced_cards = {};
    for (const position of ["top", "left", "middle", "right", "bottom"]) {
        let card = document.getElementById(`force-card-set-${position}`).value;
        if (card !== "") {
            forced_cards[position] = {
                "card": card,
                "inverted": document.getElementById(`inverted-${position}`).checked
            };
        }
    }
    return forced_cards;
}

function clear_forced_cards() {
    let dropdown_elements = document.getElementsByClassName("force-card-set");
    for (const element of dropdown_elements) {
        element.value = "";
    }
}