import { ajax_call, getCookie, setCookie } from "../common/utils.js";

let key_press_timer;

export function init_events() {
    let filter_state = getCookie("filter_state");
    if (filter_state !== "") {
        set_ui_state(JSON.parse(filter_state));
    }
    document.getElementById("filter_button").onclick = filter;
    document.getElementById("reset_button").onclick = reset_ui;
    document.getElementsByName("checkbox-all").forEach(n => n.onclick = check_all);
    document.getElementById("show-advanced-block").onclick = on_click_show_advanced;
    document.getElementById("hide-advanced-block").onclick = on_click_hide_advanced;
    filter();
}

function filter() {
    clearTimeout(key_press_timer);
    let json = JSON.stringify(get_ui_state());
    setCookie("filter_state", json);
    ajax_call("/dnd/spell_filter_results", handle_filter_results, {"filter_keys": json});
}

function handle_filter_results(xhttp) {
    document.getElementById("filter_results").innerHTML = xhttp.responseText;
}

function get_ui_state() {
    let d = {};
    d["classes"] = get_checkboxes("class");
    d["levels"] = get_checkboxes("level");
    d["schools"] = get_checkboxes("school");
    d["casting_times"] = get_checkboxes("casting-time");
    d["ranges"] = get_checkboxes("range");
    d["durations"] = get_checkboxes("duration");
    d["sources"] = get_checkboxes("source");
    d["all"] = get_checkboxes("all");
    let toggles = ["concentration", "ritual", "verbal", "somatic", "material", "expensive", "consumed"];
    toggles.forEach(toggle => d[toggle] = get_radio_group_value(toggle));
    d["ua_spells"] = document.getElementById("checkbox-ua-spells").checked;
    return d;
}

function set_ui_state(d) {
    set_checkboxes("class", d["classes"]);
    set_checkboxes("level", d["levels"]);
    set_checkboxes("school", d["schools"]);
    set_checkboxes("casting-time", d["casting_times"]);
    set_checkboxes("range", d["ranges"]);
    set_checkboxes("duration", d["durations"]);
    set_checkboxes("source", d["sources"]);
    set_checkboxes("all", d["all"]);
    let toggles = ["concentration", "ritual", "verbal", "somatic", "material", "expensive", "consumed"];
    toggles.forEach(toggle => set_radio_group_value(toggle, d[toggle]));
    document.getElementById("checkbox-ua-spells").checked = d["ua_spells"];
    return d;
}

function reset_ui() {
    let checkboxes = ["class", "level", "school", "casting-time", "range", "duration", "source", "all"];
    checkboxes.forEach(checkbox => set_checkboxes(checkbox, "all"));
    let toggles = ["concentration", "ritual", "verbal", "somatic", "material", "expensive", "consumed"];
    toggles.forEach(toggle => set_radio_group_value(toggle, "both"));
    document.getElementById("checkbox-ua-spells").checked = true;
    let json = JSON.stringify(get_ui_state());
    setCookie("filter_state", json);
}

export function check_all(e) {
    document.getElementsByName("checkbox-" + e.target.value).
        forEach(n => n.checked = e.target.checked);
}

export function get_checkboxes(name) {
    let list = document.getElementsByName("checkbox-" + name);
    let filtered_list = [];
    list.forEach(n => {
        if (n.checked)
            filtered_list.push(n.value);
    });
    return filtered_list;
}

export function set_checkboxes(name, to_set) {
    let list = document.getElementsByName("checkbox-" + name);
    if (to_set)
        list.forEach(n => n.checked = (to_set.includes(n.value) || to_set === "all"));
}

export function get_radio_group_value(name) {
    let nodes = document.getElementsByName("radio-" + name);
    for (let i=0; i < nodes.length; i++) {
        if (nodes[i].checked)
            return nodes[i].value;
    }
}

export function set_radio_group_value(name, value) {
    let nodes = document.getElementsByName("radio-" + name);
    for (let i=0; i < nodes.length; i++) {
        if (nodes[i].value === value) {
            nodes[i].checked = true;
            return;
        }
    }
}

export function on_click_show_advanced(e) {
    document.getElementById("show-advanced-block").style.display = "none";
    document.getElementById("advanced-block").style.display = "block";
}

export function on_click_hide_advanced(e) {
    document.getElementById("show-advanced-block").style.display = "block";
    document.getElementById("advanced-block").style.display = "none";
}
