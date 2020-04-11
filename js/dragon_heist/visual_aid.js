import {ajax_call} from "../common/utils";

let key_press_timer;

export function init() {
    timer_trigger();
}

function timer_trigger() {
    clearTimeout(key_press_timer);
    ajax_call("/dragon_heist/get_visual_aid/", handle_visual_aid);
}

export function handle_visual_aid(xhttp) {
    console.log(xhttp.json());
    key_press_timer = setTimeout(timer_trigger, 1000);
}