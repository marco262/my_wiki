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
        params["url"] = array[1];
    } else {
        params["target"] = array[1];
        if (array.length === 3) {
            params["url"] = array[2];
        }
    }
    ajax_call("/dragon_heist/set_visual_aid", set_visual_aid_response, params)
}

function set_visual_aid_response(xhttp) {
    console.log(xhttp);
}
