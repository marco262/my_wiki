import {ajax_call} from "../common/utils.js";

let key_press_timer;
let last_url = "";

export function init() {
    timer_trigger();
}

function timer_trigger() {
    clearTimeout(key_press_timer);
    ajax_call("/dragon_heist/get_visual_aid", handle_visual_aid);
}

export function handle_visual_aid(xhttp) {
    let response = xhttp.response;
    let json = JSON.parse(response);
    let url = json["url"];
    // console.log(url);
    if (url !== last_url) {
        console.log("Setting img src: " + url);
        document.getElementById("picture").style.backgroundImage = "url('" + url + "')";
        // document.getElementById("picture").src = url;
        last_url = url;
    }
    key_press_timer = setTimeout(timer_trigger, 2000);
}