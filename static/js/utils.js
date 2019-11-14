export const class_list = ["bard", "cleric", "druid", "paladin", "ranger", "sorcerer", "warlock", "wizard"];

export function ajax_call(url, func, spell_table_header, spell_table_row) {
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

export function spell_table(spells) {
    // spells is list of 2-tuples of (url, dict)
    return `
    <table border='1'>
        ${spell_table_header()}
        ${spells.map(spell => spell_table_row(spell[0], spell[1])).join("\n")}
    </table>`;
}

export function spell_table_header() {
    return `
    <tr>
        <th>Spell Name</th>
        <th>School</th>
        ${class_list.map(classname => `<th>${title_case(classname)}</th>`).join("\n")}
        <th>Source</th>
    </tr>`;
}

export function spell_table_row(url, dict) {
    return `
    <tr>
        <td><a href="spell/${url}">${dict["title"]}</a></td>
        <td>${title_case(dict["school"])}</td>
        ${class_list.map(classname => `<td>${dict["classes"].includes(classname) ? "X" : ""}</td>`).join("\n")}
        <td>${dict["source"]}</td>
    </tr>`;
}
