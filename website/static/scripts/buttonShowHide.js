var buttonShowHide = document.querySelectorAll(".show-hide-btn");
var inputTypePass = document.querySelectorAll(".input-type-pass");
var inputLoginPass = document.querySelector("#id_password");
var buttonShowLoginPass = document.querySelector(".show-hide-btn");

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

buttonShowLoginPass.addEventListener("click" || "touchstart", () => {
    if (inputLoginPass.getAttribute("type") == "password") {
        inputLoginPass.setAttribute("type", "text");
        buttonShowLoginPass.innerHTML = "<img src='/website/static/img/view.png' />";
    } else {
        inputLoginPass.setAttribute("type", "password");
        buttonShowLoginPass.innerHTML = "<img src='/website/static/img/hide.png' />";
    }
})