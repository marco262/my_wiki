export function search() {
    let search_key = document.getElementById("search_key").value;
    if (search_key === "") return;
    document.location = "/dnd/search/" + search_key;
}

export function on_key_press(e) {
    if (e.key === "Enter")
        search(this);
}
