export const class_list = ["bard", "cleric", "druid", "paladin", "ranger", "sorcerer", "warlock", "wizard"];

export function ajax_call(url, func) {
    const xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState === 4 && this.status === 200) {
            func(this);
        }
    };
    xhttp.open("GET", url, true);
    xhttp.send();
}

export function title_case(s) {
    return s.charAt(0).toUpperCase() + s.slice(1).toLowerCase();
}

export function spell_table(spells, split=true, show_classes=true) {
    // If split is False, spells is list of 2-tuples of (url, dict)
    // If split is True, spells is a dictionary of spells by spell level, with each dict value taking the format above.
    return `
    <table border='1'>
        ${spell_table_header(show_classes)}
        ${spells.map(spell => spell_table_row(spell[0], spell[1], show_classes)).join("\n")}
    </table>`;
}

export function spell_table_header(show_classes=true) {
    let html = `
    <tr>
        <th>Spell Name</th>
        <th>School</th>
        `;
    if (show_classes)
        html += class_list.map(classname => `<th>${title_case(classname)}</th>`).join("\n");
    html += `
        <th>Source</th>;
    </tr>`;
    return html;
}

export function spell_table_row(url, dict, show_classes=true) {
    let html =  `
    <tr>
        <td><a href="spell/${url}">${dict["title"]}</a></td>
        <td>${title_case(dict["school"])}</td>
        `;
    if (show_classes)
        html += class_list.map(classname => `<td>${dict["classes"].includes(classname) ? "X" : ""}</td>`).join("\n");
    html += `
        <td>${dict["source"]}</td>
    </tr>`;
    return html;
}
