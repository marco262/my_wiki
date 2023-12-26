export function ajax_call(url, func, params=null, error_func=null) {
    const xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState === 4) {
            if (this.status === 200) {
                if (func) {
                    func(this);
                }
            } else {
                console.error(xhttp);
                if (error_func) {
                    error_func(this);
                }
            }
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
  document.cookie = cname + "=" + cvalue + "; SameSite=Strict";
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

export function init_toc() {
    let collapse= document.getElementById("toc-collapse");
    if (collapse) {
        collapse.addEventListener("click", function () {
            this.classList.toggle("toc-hidden");
            const hidden = this.classList.contains("toc-hidden");
            collapse.innerText = hidden ? "[+]" : "[-]";
            let content = document.getElementById("toc-content");
            if (hidden) {
                content.style.maxHeight = "0";
            } else {
                content.style.maxHeight = content.scrollHeight + "px";
            }
        });
    }
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

// Durstenfeld Shuffle from https://stackoverflow.com/questions/2450954/how-to-randomize-shuffle-a-javascript-array
export function shuffle_array(array) {
    for (let i = array.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [array[i], array[j]] = [array[j], array[i]];
    }
}

export function get_w_default(dict, key, def) {
    if (!dict.hasOwnProperty(key))
        return def;
    return dict[key]
}

export function init_glossary() {
    const tooltips = document.getElementsByClassName("dfn-tooltip");
    for (let i = 0; i < tooltips.length; i++) {
        tooltips[i].addEventListener("click", function(event){
            console.log(event);
            let target;
            if (event.target.classList.contains("dfn-tooltip")) {
                target = event.target;
            } else {
                // In case we clicked an element inside the tooltip
                target = event.target.closest(".dfn-tooltip");
            }
            console.log(target);
            console.log(target.attributes);
            const anchor = target.attributes["anchor"].value;
            console.log(anchor);
            window.open(`/onednd/general/Rules Glossary#${anchor}`, '_blank');
        });
    }
}
