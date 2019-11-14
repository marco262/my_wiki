export function ajax_call(url, func, spell_table_header, spell_table_row) {
    let xhttp;
    xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            func(this);
        }
    };
    xhttp.open("GET", url, true);
    xhttp.send();
}

export function title_case(s) {
    return s.charAt(0).toUpperCase() + s.slice(1).toLowerCase();
}

export function spell_table_header() {
    return `<tr>
        <th>Spell Name</th>
        <th>School</th>
        <th>Bard</th>
        <th>Cleric</th>
        <th>Druid</th>
        <th>Paladin</th>
        <th>Ranger</th>
        <th>Sorcerer</th>
        <th>Warlock</th>
        <th>Wizard</th>
        <th>Source</th>
    </tr>\n`
}

export function spell_table_row(url, dict) {
    let ar = ["bard", "cleric", "druid", "paladin", "ranger", "sorcerer", "warlock", "wizard"];
    ar = ar.map(classname => `<td>${dict["classes"].includes(classname) ? "X" : ""}</td>`);
    return `<tr>
        <td><a href="spell/${url}">${dict["title"]}</a></td>
        <td>${title_case(dict["school"])}</td>
        ${ar.join("\n")}
        <td>${dict["source"]}</td>
    </tr>\n`;
}