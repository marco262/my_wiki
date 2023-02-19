export function init_calculator() {
    let elements = document.querySelectorAll(".spellcasting-calculator-input");
    elements.forEach(e => e.onchange = calculate_cost);
    calculate_cost();
}

function calculate_cost() {
    let spell_level = document.querySelector("#spell-level").value;
    let consumed_material = document.querySelector("#consumed-material").value;
    let non_consumed_material = document.querySelector("#non-consumed-material").value;
    let ritual_spell = document.querySelector("#ritual-spell").checked;
    let cost = Math.max((parseInt(spell_level) ** 2) * 10, 5);
    if (ritual_spell)
        cost *= 0.1;
    if (consumed_material) {
        try {
            cost += parseFloat(consumed_material);
        } catch {}
    }
    if (non_consumed_material) {
        try {
            cost += parseFloat(non_consumed_material) * 0.1;
        } catch {}
    }
    document.querySelector("#spellcasting-service-cost span").innerText = cost;
}