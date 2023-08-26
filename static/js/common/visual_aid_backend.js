import { ajax_call } from "./utils.js";

let player_soundboard = false;
let volume_change_lock = false;
let volume_slider_timer = null;

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

    ajax_call("/get_volume_settings", set_volume_controls);
    let volume_sliders = document.getElementsByClassName("volume_slider");
    Array.prototype.forEach.call(volume_sliders, function (e) {
        console.log(e);
        e.addEventListener("input", handle_volume_change);
    });
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

function set_volume_controls(xhttp) {
    console.log(xhttp);
    const volume_settings = JSON.parse(xhttp.response);
    console.log(volume_settings);
    let highest_value = 0;
    volume_change_lock = true;
    for (const [target, value] of Object.entries(volume_settings)) {
        let e = document.getElementById(`${target}_volume`);
        if (e !== null) {
            e.value = value * 1000;
            if (value > highest_value)
                highest_value = value;
        }
    }
    let e = document.getElementById(`all_volume`);
    e.value = highest_value * 1000;
    // Reset the lock after a short delay
    setTimeout(() => {volume_change_lock = false;}, 100);
}

function handle_volume_change(event) {
    if (event.target.attributes["target"].value === "all") {
        document.getElementById("music_volume").value = event.target.value;
        document.getElementById("ambience_volume").value = event.target.value;
        document.getElementById("effect_volume").value = event.target.value;
    }
    clearTimeout(volume_slider_timer);
    volume_slider_timer = setTimeout(() => { send_volume_change(event) }, 1000);
}

function send_volume_change(event) {
    if (volume_change_lock) return;
    console.log(event);
    let params = {
        "music": document.getElementById("music_volume").value / 1000,
        "ambience": document.getElementById("ambience_volume").value / 1000,
        "effect": document.getElementById("effect_volume").value / 1000,
    }
    ajax_call("/set_volume", set_volume_controls, params)
}
