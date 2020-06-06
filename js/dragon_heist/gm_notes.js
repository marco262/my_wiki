import { ajax_call } from "../common/utils.js";

export function init() {
    let visual_aid_buttons = document.getElementsByClassName("visual-aid-button");
    Array.prototype.forEach.call(visual_aid_buttons, function (button) {
        button.onclick = function (event) { set_visual_aid(event, button.value); };
    })
}

function set_visual_aid(event, value) {
    console.log(event);
    console.log(value);
    let array = value.split("|");
    let action = array[0]
    let params = {
        "action": action,
        "debug": event.ctrlKey
    };
    if (action === "visual_aid") {
        let url = array[1];
        if (url && !url.startsWith("http")) {
            url = "/static/img/visual_aids/" + url;
        }
        params["url"] = url;
    } else {
        params["target"] = array[1];
        if (array.length === 3) {
            let url = array[2];
            if (url && !url.startsWith("http")) {
                url = "/static/audio/" + url;
            }
            params["url"] = url;
        }
    }
    if (event.ctrlKey) {
        set_visual_aid_response(params["url"]);
    } else {
        ajax_call("/dragon_heist/set_visual_aid", null, params)
    }
}

function set_visual_aid_response(url) {
    console.log(url);
    if (url) {
        var new_window = window.open(url, "", "");
    }
}
