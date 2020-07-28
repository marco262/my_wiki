export function search() {
    let search_key = document.getElementById("search_key").value;
    if (search_key === "") return;
    document.location = "/dnd/search/" + search_key;
}
