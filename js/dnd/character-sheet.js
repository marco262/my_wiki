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

export function load_json(character_json) {
    console.log(character_json);
    document.getElementById("race").innerText = character_json["race"];
    document.getElementById("class").innerText = character_json["class"];
    level = Math.trunc(character_json["level"]);
    document.getElementById("level").innerText = level.toString();
    for (const ability_score in character_json["attributes"]) {
        const score = character_json["attributes"][ability_score];
        document.getElementById(ability_score.toLowerCase() + "-score").innerText = score;
        const mod = (Math.trunc(score) - 10) / 2;
        ability_score_mods[ability_score.toLowerCase()] = mod;
        document.getElementById(ability_score.toLowerCase() + "-mod").innerText = to_mod(mod);
    }
    character_json["saves"].forEach(s => document.getElementById(s.toLowerCase() + "-prof").checked = true);
    character_json["skills"].forEach(s => {
        document.getElementById(s.toLowerCase() + "-prof").checked = true
    });

    calculate_stats();
}

function to_mod(num) {
    let mod = Math.trunc(num).toString();
    if (!mod.startsWith("-")) {
        mod = "+" + mod
    }
    return mod
}


function calculate_stats() {
    // Proficiency bonus
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
        let mod = ability_score_mods[skills[i][1].toLowerCase()];
        const skill_name = skills[i][0].toLowerCase().replace(/ /g, "-");
        if (document.getElementById(skill_name + "-prof").checked) {
            mod += prof_bonus;
        }
        if (document.getElementById(skill_name + "-ex").checked) {
            mod += prof_bonus;
        }
        document.getElementById(skill_name + "-mod").innerText = to_mod(mod);
    }
}
