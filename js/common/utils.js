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

export function init_accordions() {
    let acc = document.getElementsByClassName("accordion-button");
    for (let i = 0; i < acc.length; i++) {
        acc[i].addEventListener("click", function() {
            this.classList.toggle("accordion-active");
            let panel = this.nextElementSibling;
            if (panel.style.maxHeight) {
                panel.style.maxHeight = null;
            } else {
                panel.style.maxHeight = panel.scrollHeight + "px";
            }
        });
    }
}

export function init_tabs() {
    let tabs = document.getElementsByClassName("tab-button");
    for (let i = 0; i < tabs.length; i++) {
        tabs[i].addEventListener("click", click_tab)
    }
}

export function click_tab(event) {
    // Set all tabs to in-active, then set the target tab to active
    let tabs = document.getElementsByClassName("tab-button");
    // console.log(tabs);
    for (let i = 0; i < tabs.length; i++) {
        tabs[i].classList.remove("tab-active");
    }
    event.target.className += " tab-active";
    let id = event.target.id;
    let active_page_id = id.substring(0, id.length - 4) + "-page";
    let pages = document.getElementsByClassName("tab-page");
    for (let i = 0; i < pages.length; i++) {
        pages[i].style.display = (pages[i].id === active_page_id) ? "inline-block" : "none";
    }
}