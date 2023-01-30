import { ajax_call } from "./utils.js";

let player_soundboard = false;

export function set_player_soundboard() {
    player_soundboard = true;
}

export function init_links() {
    let visual_aid_buttons = document.getElementsByClassName("visual-aid-link");
    Array.prototype.forEach.call(visual_aid_buttons, function (link) {
        link.onclick = function (event) {
            set_visual_aid(event, link.title);
        };
    })
}

export function init_visual_aid() {
    document.getElementById("custom_visual_aid_button").onclick = function (event) {
        console.log(document.getElementById("custom_visual_aid_url"));
        set_visual_aid(event, `visual_aid|${document.getElementById("custom_visual_aid_url").value}`);
    }
}

export function init_soundboard() {
    document.getElementById("custom_music_button").onclick = function (event) {
        let url = document.getElementById("custom_soundboard_url").value;
        console.log(url);
        set_visual_aid(event, `load|music|${url}`);
    }

    document.getElementById("custom_ambient_button").onclick = function (event) {
        let url = document.getElementById("custom_soundboard_url").value;
        console.log(url);
        set_visual_aid(event, `load|ambient|${url}`);
    }

    document.getElementById("custom_effect_button").onclick = function (event) {
        let url = document.getElementById("custom_soundboard_url").value;
        console.log(url);
        set_visual_aid(event, `load|effect|${url}`);
    }

    document.getElementById("custom_youtube_button").onclick = function (event) {
        let url = document.getElementById("custom_soundboard_url").value;
        console.log(url);
        set_visual_aid(event, `load|youtube|${url}`);
    }
}

function set_visual_aid(event, value) {
    let array = value.split("|");
    let action = array[0]
    let params = {
        "action": action,
        "player_soundboard": player_soundboard
    };
    if (action === "visual_aid") {
        let url = array[1];
        if (url && !url.startsWith("http")) {
            url = "/media/img/visual_aids/" + url;
        }
        let title = array.length >= 3 ? array[2] : "";
        params["url"] = url;
        params["title"] = event.altKey ? title : "";
    } else if (action === "iframe") {
        params["url"] = array[1];
    } else {
        params["target"] = array[1];
        if (array.length === 3) {
            let url = array[2];
            if (url && !url.startsWith("http")) {
                url = "/media/audio/" + url;
            }
            params["url"] = url;
        }
    }
    console.log(event);
    if (event.ctrlKey || event.metaKey) {
        set_visual_aid_response(params["url"]);
    } else {
        ajax_call("/set_visual_aid", null, params)
    }
}

function set_visual_aid_response(url) {
    console.log(url);
    if (url) {
        window.open(url, "", "");
    }
}
