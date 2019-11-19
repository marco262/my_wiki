import { ajax_call } from "./utils.js";

let key_press_timer;

export function init_events() {
    document.getElementById("filter_button").onclick = filter;
    document.getElementById("checkbox-class-all").onclick = on_click_class_all;
    document.getElementById("checkbox-level-all").onclick = on_click_level_all;
    document.getElementById("checkbox-school-all").onclick = on_click_school_all;
    document.getElementById("show-advanced-block").onclick = on_click_show_advanced_block;
    document.getElementById("hide-advanced-block").onclick = on_click_hide_advanced_block;
}

function filter() {
    clearTimeout(key_press_timer);
    let json = {};
    json["classes"] = filter_list("class");
    json["levels"] = filter_list("level");
    json["schools"] = filter_list("school");
    let toggles = ["concentration", "ritual", "verbal", "somatic", "material", "expensive", "consumed"];
    toggles.forEach(toggle => {
        json[toggle] = get_radio_group_value(toggle);
    });
    ajax_call("/filter_results/" + JSON.stringify(json), handle_filter_results);
}

function on_click(e) {
    clearTimeout(key_press_timer);
    key_press_timer = setTimeout(search, 1000);
}

function handle_filter_results(xhttp) {
    document.getElementById("filter_results").innerHTML = xhttp.responseText;
}

function on_click_class_all(e) {
    check_all("class", e.target.checked);
}

function on_click_level_all(e) {
    check_all("level", e.target.checked);
}

function on_click_school_all(e) {
    check_all("school", e.target.checked);
}

function check_all(name, state) {
    document.getElementsByName("checkbox-" + name).forEach(n => { n.checked = state; });
}

function on_click_show_advanced_block(e) {
    document.getElementById("show-advanced-block").style.display = "none";
    document.getElementById("advanced-block").style.display = "block";
}

function on_click_hide_advanced_block(e) {
    document.getElementById("show-advanced-block").style.display = "block";
    document.getElementById("advanced-block").style.display = "none";
}

function filter_list(name) {
    let list = document.getElementsByName("checkbox-" + name);
    let filtered_list = [];
    list.forEach(n => {
        if (n.checked) {
            filtered_list.push(n.value);
        }
    });
    return filtered_list;
}

function get_radio_group_value(name) {
    let nodes = document.getElementsByName("radio-" + name);
    for (let i=0; i < nodes.length; i++) {
        if (nodes[i].checked) {
            return nodes[i].value;
        }
    }
}
