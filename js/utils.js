export const class_list = ["bard", "cleric", "druid", "paladin", "ranger", "sorcerer", "warlock", "wizard"];
export const spell_list = ["cantrip", "1", "2", "3", "4", "5", "6", "7", "8", "9"];

export function ajax_call(url, func, params=null) {
    const xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState === 4 && this.status === 200) {
            func(this);
        }
    };
    xhttp.open(params === null ? "GET" : "POST", url, true);
    xhttp.setRequestHeader("X-Requested-With", "XMLHttpRequest");
    if (params === null) {
        xhttp.send();
    } else {
        let post_params;
        if (typeof params === "string") {
            post_params = params;
        } else {
            post_params = Object.keys(params).map(
                k => encodeURIComponent(k) + "=" + encodeURIComponent(params[k])
            ).join("&");
        }
        xhttp.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
        xhttp.send(post_params);
    }
}

export function title_case(s) {
    return s.charAt(0).toUpperCase() + s.slice(1).toLowerCase();
}

function num_to_level(num) {
    if (isNaN(num))
        return "Cantrip";
    let level;
    if (num === "1")
        level = "1st";
    else if (num === "2")
        level = "2nd";
    else if (num === "3")
        level = "3rd";
    else
        level = num.toString() + "th";
    return level + " level"
}

export function spell_table(spells, split=true, show_classes=true) {
    // Creates multiple tables of spells, sorted by spell level, if split is true. Otherwise, a single table
    // If split is False, spells must be a list of 2-tuples of (url, dict)
    // If split is True, spells must be a dictionary of spells by spell level, with each dict value
    //  taking the format above.
    if (split === false)
        return spell_table_level(spells, show_classes);
    let html = "";
    spell_list.forEach(function(spell_level) {
        if (spells.hasOwnProperty(spell_level)) {
            html += `
            <h2>${num_to_level(spell_level)}</h2>
            ${spell_table_level(spells[spell_level], show_classes)}`;
        }
    });
    return html;
}

export function spell_table_level(spells, show_classes=true) {
    // Creates a single table of spells
    // spells is list of 2-tuples of (url, dict)
    return `
    <table>
        ${spell_table_header(show_classes)}
        ${spells.map(spell => spell_table_row(spell[0], spell[1], show_classes)).join("\n")}
    </table>`;
}

function spell_table_header(show_classes=true) {
    let html = `
    <tr>
        <th>Spell Name</th>
        <th>School</th>
        `;
    if (show_classes)
        html += class_list.map(classname => `<th>${title_case(classname)}</th>`).join("\n");
    html += `
        <th>Source</th>
    </tr>`;
    return html;
}

function spell_table_row(url, dict, show_classes=true) {
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

export function setCookie(cname, cvalue) {
  document.cookie = cname + "=" + cvalue + ";";
}

export function getCookie(cname) {
  const name = cname + "=";
  const ca = document.cookie.split(';');
  for(let i = 0; i < ca.length; i++) {
    let c = ca[i];
    while (c.charAt(0) === ' ') {
      c = c.substring(1);
    }
    if (c.indexOf(name) === 0) {
      return c.substring(name.length, c.length);
    }
  }
  return "";
}
