import { ajax_call, getCookie, setCookie } from "../common/utils.js";

export function init_events() {
    let filter_state = getCookie("magic_item_filter_state");
    if (filter_state !== "") {
        set_ui_state(JSON.parse(filter_state));
    }
    document.getElementById("filter_button").onclick = filter;
    document.getElementById("reset_button").onclick = reset_ui;
    document.getElementsByName("checkbox-all").forEach(n => n.onclick = check_all);
    filter();
}

function filter() {
    let json = JSON.stringify(get_ui_state());
    setCookie("magic_item_filter_state", json);
    ajax_call("/dnd/equipment/magic_item_filter_results", handle_filter_results, {"filter_keys": json});
}

function handle_filter_results(xhttp) {
    document.getElementById("filter_results").innerHTML = xhttp.responseText;
}

function get_ui_state() {
    let d = {};
    d["types"] = get_checkboxes("type");
    d["rarities"] = get_checkboxes("rarity");
    d["classes"] = get_checkboxes("class");
    d["sources"] = get_checkboxes("source");
    let toggles = ["attunement"];
    toggles.forEach(toggle => d[toggle] = get_radio_group_value(toggle));
    return d;
}

function set_ui_state(d) {
    set_checkboxes("type", d["types"]);
    set_checkboxes("rarity", d["rarities"]);
    set_checkboxes("class", d["classes"]);
    set_checkboxes("source", d["sources"]);
    let toggles = ["attunement"];
    toggles.forEach(toggle => set_radio_group_value(toggle, d[toggle]));
    return d;
}

function reset_ui() {
    set_checkboxes("type", "all");
    set_checkboxes("rarity", "all");
    set_checkboxes("class", "all");
    set_checkboxes("source", "all");
    let toggles = ["attunement"];
    toggles.forEach(toggle => set_radio_group_value(toggle, "both"));
    let json = JSON.stringify(get_ui_state());
    setCookie("magic_item_filter_state", json);
}

function check_all(e) {
    document.getElementsByName("checkbox-" + e.target.value).forEach(n => n.checked = e.target.checked);
}

function get_checkboxes(name) {
    let list = document.getElementsByName("checkbox-" + name);
    let filtered_list = [];
    list.forEach(n => {
        if (n.checked)
            filtered_list.push(n.value);
    });
    return filtered_list;
}

function set_checkboxes(name, to_set) {
    let list = document.getElementsByName("checkbox-" + name);
    if (to_set)
        list.forEach(n => n.checked = (to_set.includes(n.value) || to_set === "all"));
}

function get_radio_group_value(name) {
    let nodes = document.getElementsByName("radio-" + name);
    for (let i=0; i < nodes.length; i++) {
        if (nodes[i].checked)
            return nodes[i].value;
    }
}

function set_radio_group_value(name, value) {
    let nodes = document.getElementsByName("radio-" + name);
    for (let i=0; i < nodes.length; i++) {
        if (nodes[i].value === value) {
            nodes[i].checked = true;
            return;
        }
    }
}
