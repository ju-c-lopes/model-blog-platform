var buttonShowHide = document.querySelectorAll(".show-hide-btn");
var inputTypePass = document.querySelectorAll(".input-type-pass");

for (let i = 0; i < buttonShowHide.length; i++) {
    buttonShowHide[i].addEventListener('click' || 'touchstart', () => {
        if (inputTypePass[i].getAttribute("type") == "password") {
            inputTypePass[i].setAttribute("type", "text");
            buttonShowHide[i].innerHTML = "<img src='/website/static/img/view.png' />";
        } else {
            inputTypePass[i].setAttribute("type", "password");
            buttonShowHide[i].innerHTML = "<img src='/website/static/img/hide.png' />";
        }
    })
}