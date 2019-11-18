import { ajax_call, spell_table } from "./utils.js";

let key_press_timer;

export function filter() {
    clearTimeout(key_press_timer);
    let json = {};
    json["classes"] = filter_list(
        "class",
        ["bard", "cleric", "druid", "paladin", "ranger", "sorcerer", "warlock", "wizard"]
    );
    json["levels"] = filter_list(
        "level",
        ["cantrip", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
    );
    json["schools"] = filter_list(
        "school",
        ["abjuration", "conjuration", "divination", "evocation", "enchantment", "illusion", "necromancy",
         "transmutation"]
    );
    let toggles = ["concentration", "ritual", "verbal", "somatic", "material", "expensive", "consumed"];
    toggles.forEach(toggle =>
        {
            json[toggle] = get_radio_group_value(toggle);
        }
    );
    ajax_call("/filter_results/" + JSON.stringify(json), handle_filter_results);
}

export function on_click(e) {
    clearTimeout(key_press_timer);
    key_press_timer = setTimeout(search, 1000);
}

function handle_filter_results(xhttp) {
    document.getElementById("filter_results").innerHTML = xhttp.responseText;
}

function filter_list(name, list) {
    return list.filter(n => document.getElementById("checkbox-" + name + "-" + n).checked);
}

function get_radio_group_value(name) {
    let nodes = document.getElementsByName("radio-" + name);
    for (let i=0; i < nodes.length; i++) {
        if (nodes[i].checked) {
            return nodes[i].value;
        }
    }
}
