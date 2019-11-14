export function ajax_call(url, func) {
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
