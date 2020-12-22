
export function init() {
    let flip_card_inner_elements = document.getElementsByClassName("flip-card-inner");
    Array.prototype.forEach.call(flip_card_inner_elements, function (element) {
        element.onclick = function (event) {
            element.classList.toggle("flipped");
        };
    });
}