export function init_npc_sheets() {
    let npc_sheets = document.getElementsByClassName("npc-sheet");
    for (let npc_sheet of npc_sheets)
        npc_sheet.onclick = click_npc_sheet;
}

function click_npc_sheet(event) {
    let target = event.target;
    let monster_sheet;
    if (target.className === "npc-sheet-hover")
        monster_sheet = target.nextElementSibling;
    else
        monster_sheet = target.closest(".monster-sheet");
    if (monster_sheet.style.visibility)
        monster_sheet.style.visibility = null;
    else
        monster_sheet.style.visibility = "visible";
}
