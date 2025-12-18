import { ajax_call, getCookie, setCookie } from "../common/utils.js";
import {
    check_all,
    get_checkboxes,
    get_radio_group_value,
    set_checkboxes,
    set_radio_group_value,
    on_click_show_advanced,
    on_click_hide_advanced,
} from "./spell_filter.js";

let cookie_name = "";

export function init() {
    init_events("magic_item_filter_state");
    document.getElementById("filter_button").onclick = filter;
    filter();
}

export function init_events(v_cookie_name) {
    cookie_name = v_cookie_name;
    let filter_state = getCookie(cookie_name);
    if (filter_state !== "") {
        set_ui_state(JSON.parse(filter_state));
    }
    document.getElementById("reset_button").onclick = reset_ui;
    document.getElementsByName("checkbox-all").forEach(n => n.onclick = check_all);
    document.getElementById("show-advanced-block").onclick = on_click_show_advanced;
    document.getElementById("hide-advanced-block").onclick = on_click_hide_advanced;
}

function filter() {
    let json = JSON.stringify(get_ui_state());
    setCookie("magic_item_filter_state", json);
    ajax_call("/dnd/equipment/magic_item_filter_results", handle_filter_results, {"filter_keys": json});
}

function handle_filter_results(xhttp) {
    document.getElementById("filter_results").innerHTML = xhttp.responseText;
}

export function get_ui_state() {
    let d = {};
    let checkboxes = ["type", "rarity", "minor-major", "subtype", "classes", "source", "all"];
    checkboxes.forEach(checkbox_name => d[checkbox_name] = get_checkboxes(checkbox_name));
    let toggles = ["attunement"];
    toggles.forEach(toggle => d[toggle] = get_radio_group_value(toggle));
    return d;
}

function set_ui_state(d) {
    let checkboxes = ["type", "rarity", "minor-major", "subtype", "classes", "source", "all"];
    checkboxes.forEach(checkbox_name => set_checkboxes(checkbox_name, d[checkbox_name]));
    let toggles = ["attunement"];
    toggles.forEach(toggle => set_radio_group_value(toggle, d[toggle]));
    return d;
}

function reset_ui() {
    let checkboxes = ["type", "rarity", "minor-major", "subtype", "classes", "source", "all"];
    checkboxes.forEach(checkbox => set_checkboxes(checkbox, "all"));
    // Disable some checkboxes by default
    let prosthetic_checkbox = document.querySelector('[name="checkbox-subtype"][value="prosthetic"]');
    if (prosthetic_checkbox)
        prosthetic_checkbox.checked = false;
    let toggles = ["attunement"];
    toggles.forEach(toggle => set_radio_group_value(toggle, "both"));
    let json = JSON.stringify(get_ui_state());
    setCookie(cookie_name, json);
}
