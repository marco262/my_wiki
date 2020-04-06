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

let ability_score_mods = {};
let level = 1;
let class_features = [];

export function load_json(character_json) {
    load_ability_scores(character_json);
    calculate_stats();
    init_checkboxes();
}

function load_ability_scores(character_json) {
    document.getElementById("race").innerText = character_json["race"];
    document.getElementById("class").innerText = character_json["class"];
    level = Math.trunc(character_json["level"]);
    document.getElementById("level").innerText = level.toString();
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
    // Misc
    const prof_bonus = Math.trunc((level - 1) / 4) + 2;
    document.getElementById("proficiency-bonus").innerText = to_mod(prof_bonus);
    let initiative = ability_score_mods["dexterity"];
    if (class_features.includes("Jack of All Trades")) {
        initiative += Math.trunc(prof_bonus / 2);
    }
    document.getElementById("initiative").innerText = to_mod(initiative);
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
        } else if (class_features.includes("Jack of All Trades")) {
            mod += Math.trunc(prof_bonus / 2);
        }
        document.getElementById(skill_name + "-mod").innerText = to_mod(mod);
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
