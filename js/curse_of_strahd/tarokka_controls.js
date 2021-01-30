import {ajax_call, shuffle_array} from "../common/utils.js";

const tarokka_card_list = ['1 of Coins - Swashbuckler', '1 of Glyphs - Monk', '1 of Stars - Transmuter', '1 of Swords - Avenger', '2 of Coins - Philanthropist', '2 of Glyphs - Missionary', '2 of Stars - Diviner', '2 of Swords - Paladin', '3 of Coins - Trader', '3 of Glyphs - Healer', '3 of Stars - Enchanter', '3 of Swords - Soldier', '4 of Coins - Merchant', '4 of Glyphs - Shepherd', '4 of Stars - Abjurer', '4 of Swords - Mercenary', '5 of Coins - Guild Member', '5 of Glyphs - Druid', '5 of Stars - Elementalist', '5 of Swords - Myrmidon', '6 of Coins - Beggar', '6 of Glyphs - Anarchist', '6 of Stars - Evoker', '6 of Swords - Berserker', '7 of Coins - Thief', '7 of Glyphs - Charlatan', '7 of Stars - Illusionist', '7 of Swords - Hooded One', '8 of Coins - Tax Collector', '8 of Glyphs - Bishop', '8 of Stars - Necromancer', '8 of Swords - Dictator', '9 of Coins - Miser', '9 of Glyphs - Traitor', '9 of Stars - Conjurer', '9 of Swords - Torturer', 'High Deck - Artifact', 'High Deck - Beast', 'High Deck - Broken One', 'High Deck - Darklord', 'High Deck - Donjon', 'High Deck - Executioner', 'High Deck - Ghost', 'High Deck - Horseman', 'High Deck - Innocent', 'High Deck - Marionette', 'High Deck - Mists', 'High Deck - Raven', 'High Deck - Seer', 'High Deck - Tempter', 'High Deck - Temptress', 'Master of Coins - Rogue', 'Master of Glyphs - Priest', 'Master of Stars - Wizard', 'Master of Swords - Warrior'];

export function init() {
    document.getElementById("deal-button").onclick = () => { send_to_websocket("deal"); };
    document.getElementById("flip-all-button").onclick = () => { send_to_websocket("flip", "all"); };
    document.getElementById("flip-top-button").onclick = () => { send_to_websocket("flip", "top"); };
    document.getElementById("flip-left-button").onclick = () => { send_to_websocket("flip", "left"); };
    document.getElementById("flip-middle-button").onclick = () => { send_to_websocket("flip", "middle"); };
    document.getElementById("flip-right-button").onclick = () => { send_to_websocket("flip", "right"); };
    document.getElementById("flip-bottom-button").onclick = () => { send_to_websocket("flip", "bottom"); };
    document.getElementById("reset-button").onclick = () => { send_to_websocket("reset"); };
    document.getElementById("set-prophecy-button").onclick = set_prophecy;
    document.getElementById("set-ezmerelda-reading-button").onclick = set_ezmerelda_reading;
    document.getElementById("set-random-reading-button").onclick = set_random_reading;
}

function set_prophecy() {
    send_to_websocket(
        "set",
        JSON.stringify({
            "top": {
                "card": "8 of Coins - Tax Collector",
                "inverted": false
            },
            "left": {
                "card": "Master of Glyphs - Priest",
                "inverted": false
            },
            "middle": {
                "card": "High Deck - Broken One",
                "inverted": false
            },
            "right": {
                "card": "2 of Glyphs - Missionary",
                "inverted": false
            },
            "bottom": {
                "card": "High Deck - Mists",
                "inverted": false
            },
        })
    );
}

function set_ezmerelda_reading() {
    send_to_websocket(
        "set",
        JSON.stringify({
            "top": {
                "card": "9 of Glyphs - Traitor",
                "inverted": true
            },
            "left": {
                "card": "High Deck - Mists",
                "inverted": false
            },
            "middle": {
                "card": "7 of Glyphs - Charlatan",
                "inverted": false
            },
            "right": {
                "card": "4 of Glyphs - Shepherd",
                "inverted": true
            },
            "bottom": {
                "card": "9 of Swords - Torturer",
                "inverted": false
            },
        })
    );
}

function set_random_reading() {
    shuffle_array(tarokka_card_list);
    send_to_websocket(
        "set",
        JSON.stringify({
            "top": {
                "card": tarokka_card_list[0],
                "inverted": Math.random() < 0.5
            },
            "left": {
                "card": tarokka_card_list[1],
                "inverted": Math.random() < 0.5
            },
            "middle": {
                "card": tarokka_card_list[2],
                "inverted": Math.random() < 0.5
            },
            "right": {
                "card": tarokka_card_list[3],
                "inverted": Math.random() < 0.5
            },
            "bottom": {
                "card": tarokka_card_list[4],
                "inverted": Math.random() < 0.5
            },
        })
    );
}

function send_to_websocket(action, data=null) {
    let params = {
        "action": action,
        "data": data
    }
    ajax_call("/curse_of_strahd/play_tarokka", null, params)
}
