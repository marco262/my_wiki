const skills = [
    ["Acrobatics", "Dexterity"],
    ["Animal Handling", "Wisdom"],
    ["Arcana", "Intelligence"],
    ["Athletics", "Strength"],
    ["Deception", "Charisma"],
    ["History", "Intelligence"],
    ["Insight", "Wisdom"],
    ["Intimidation", "Charisma"],
    ["Investigation", "Intelligence"],
    ["Medicine", "Wisdom"],
    ["Nature", "Intelligence"],
    ["Perception", "Wisdom"],
    ["Performance", "Charisma"],
    ["Persuasion", "Charisma"],
    ["Religion", "Intelligence"],
    ["Sleight of Hand", "Dexterity"],
    ["Stealth", "Dexterity"],
    ["Survival", "Wisdom"]
];

const spell_levels = ["Cantrips", "1st level", "2nd level", "3rd level", "4th level", "5th level", "6th level", 
    "7th level", "8th level", "9th level"];

let ability_score_mods = {};
let level = 1;
let class_features = [];
let character_json;

export function load_json(cj) {
    character_json = cj;
    load_ability_scores();
    calculate_stats();
    init_checkboxes();
    // set_tab_page_size();
    add_class_features();
}

function load_ability_scores() {
    document.getElementById("race").innerText = character_json["race"];
    document.getElementById("class").innerText = character_json["class"];
    level = Math.trunc(character_json["level"]);
    document.getElementById("level").innerText = level.toString();
    document.getElementById("background").innerText = character_json["background"];
    for (const ability_score in character_json["attributes"]) {
        const score = character_json["attributes"][ability_score];
        document.getElementById(to_id(ability_score) + "-score").innerText = score;
        const mod = (Math.trunc(score) - 10) / 2;
        ability_score_mods[to_id(ability_score)] = mod;
        document.getElementById(to_id(ability_score) + "-mod").innerText = to_mod(mod);
    }
    character_json["saves"].forEach(s => document.getElementById(to_id(s) + "-prof").checked = true);
    character_json["skills"].forEach(s => document.getElementById(to_id(s) + "-prof").checked = true);
    character_json["expertises"].forEach(s => document.getElementById(to_id(s) + "-ex").checked = true);
    class_features = character_json["class_features"];
}

function to_mod(num) {
    let mod = Math.trunc(num).toString();
    if (!mod.startsWith("-")) {
        mod = "+" + mod
    }
    return mod
}

function to_id(name) {
    return name.toLowerCase().replace(/ /g, "-");
}


function calculate_stats() {
    const prof_bonus = Math.trunc((level - 1) / 4) + 2;
    // Saves
    for (const name in ability_score_mods) {
        let mod = ability_score_mods[name];
        if (document.getElementById(name + "-prof").checked) {
            mod += prof_bonus;
        }
        document.getElementById(name + "-save-mod").innerText = to_mod(mod);
    }
    // Skills
    for (let i=0; i < skills.length; i++) {
        let mod = ability_score_mods[to_id(skills[i][1])];
        const skill_name = to_id(skills[i][0]);
        if (document.getElementById(skill_name + "-prof").checked) {
            mod += prof_bonus;
            if (document.getElementById(skill_name + "-ex").checked) {
                mod += prof_bonus;
            }
        } else if (class_features.hasOwnProperty("Jack of All Trades")) {
            mod += Math.trunc(prof_bonus / 2);
        }
        document.getElementById(skill_name + "-mod").innerText = to_mod(mod);
    }
    // Combat
    document.getElementById("hp").innerText = character_json["hp"];
    document.getElementById("proficiency-bonus").innerText = to_mod(prof_bonus);
    let initiative = ability_score_mods["dexterity"];
    if (class_features.hasOwnProperty("Jack of All Trades")) {
        initiative += Math.trunc(prof_bonus / 2);
    }
    document.getElementById("initiative").innerText = to_mod(initiative);
    document.getElementById("melee-attack-bonus").innerText = 
        to_mod(ability_score_mods["strength"] + prof_bonus);
    document.getElementById("melee-attack-bonus").innerText = 
        to_mod(ability_score_mods["strength"] + prof_bonus);
    document.getElementById("ranged-attack-bonus").innerText =
        to_mod(ability_score_mods["strength"] + prof_bonus);
    // Spellcasting
    if (class_features.hasOwnProperty("Spellcasting")) {
        const spellcasting_dict = class_features["Spellcasting"];
        const spellcasting_bonus = ability_score_mods[spellcasting_dict["stat"].toLowerCase()];
        document.getElementById("spellcasting-bonus").innerText = to_mod(spellcasting_bonus);
        document.getElementById("spell-attack-bonus").innerText = to_mod(spellcasting_bonus + prof_bonus);
        document.getElementById("spell-dc").innerText = 8 + spellcasting_bonus + prof_bonus;
        const spell_list_grid = document.getElementById("spell-list-grid");
        spell_list_grid.innerHTML = "";
        spell_levels.forEach(function (spell_level) {
            console.log(spell_level);
            if (spellcasting_dict["spells"].hasOwnProperty(spell_level)) {
                let spell_slots_div = document.createElement("div");
                console.log(spellcasting_dict["spell_slots"]);
                for (let i=0; i < spellcasting_dict["spell_slots"][spell_level]; i++) {
                    let checkbox = document.createElement("input");
                    checkbox.type = "checkbox";
                    spell_slots_div.appendChild(checkbox);
                }
                spell_list_grid.appendChild(spell_slots_div);
                let spell_name_div = document.createElement("div");
                spell_name_div.className = "spell-name";
                spell_name_div.innerText = spell_level;
                spell_list_grid.appendChild(spell_name_div);
                const spells_div = document.createElement("div");
                let spells = [];
                spellcasting_dict["spells"][spell_level].forEach(function (spell) {
                    spells.push(`<a href="/dnd/spell/${spell}"><i>${spell}</i></a>`);
                });
                spells_div.innerHTML = spells.join(", ");
                spell_list_grid.appendChild(spells_div);
            }
        });
    }
}

function init_checkboxes() {
    const classes = ["save-checkbox", "skill-prof-checkbox", "skill-ex-checkbox"];
    classes.forEach(c => {
        const checkboxes = document.getElementsByClassName(c);
        for (let i=0; i < checkboxes.length; i++) {
            checkboxes[i].addEventListener("change", on_checked);
        }
    });
}

function on_checked(event) {
    const id = event.currentTarget.id;
    if (id.endsWith("-prof") && !event.currentTarget.checked) {
        let secondary_checkbox_id = id.substring(0, id.length - 5) + "-ex";
        let secondary_checkbox = document.getElementById(secondary_checkbox_id);
        if (secondary_checkbox) {
            secondary_checkbox.checked = false;
        }
    } else if (id.endsWith("-ex") && event.currentTarget.checked) {
        let secondary_checkbox_id = id.substring(0, id.length - 3) + "-prof";
        document.getElementById(secondary_checkbox_id).checked = true;
    }
    calculate_stats();
}

function set_tab_page_size() {
    let tab_pages = document.getElementsByClassName("tab-page");
    // Find max size
    let max_height = 0;
    let max_width = 0;
    for (let i=0; i < tab_pages.length; i++) {
        let tab_page = tab_pages[i];
        max_height = Math.max(max_height, tab_page.offsetHeight);
        max_width = Math.max(max_width, tab_page.offsetWidth);
    }
    // Set size for all pages
    for (let i=0; i < tab_pages.length; i++) {
        let tab_page = tab_pages[i];
        tab_page.style.height = max_height.toString() + "px";
        tab_page.style.width = max_width.toString() + "px";
    }
    for (let i=0; i < tab_pages.length; i++) {
        let tab_page = tab_pages[i];
        if (i > 0) {
            tab_page.style.display = "none";
        }
    }
}

function add_class_features() {
    let class_features_json = character_json["class_features"];
    let class_features_div = document.getElementById("class-features-grid");
    for (const name in class_features_json) {
        if (class_features_json.hasOwnProperty(name)) {
            let class_feature_dict = class_features_json[name];
            // Add uses checkboxes
            let checkboxes = document.createElement("div");
            if (class_feature_dict.hasOwnProperty("max_uses")) {
                for (let i=0; i < class_feature_dict["max_uses"]; i++) {
                    let checkbox = document.createElement("input");
                    checkbox.type = "checkbox";
                    checkbox.className = "class-feature-use";
                    if (class_feature_dict.hasOwnProperty("used") && class_feature_dict["used"] > i) {
                        checkbox.checked = true;
                    }
                    checkboxes.appendChild(checkbox)
                }
            }
            class_features_div.appendChild(checkboxes);
            // Add class feature name
            let class_feature_name = document.createElement("div");
            class_feature_name.className = "class-feature-name";
            class_feature_name.innerText = name;
            class_features_div.appendChild(class_feature_name);
        }
    }
}
