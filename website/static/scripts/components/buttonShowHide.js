const buttonShowHide = document.querySelectorAll(".show-hide-btn");
const inputTypePass = document.querySelectorAll(".input-type-pass");
const inputLoginPass1 = document.querySelector("#id_password1");
const inputLoginPass2 = document.querySelector("#id_password2");
const buttonShowLoginPass = document.querySelector(".show-hide-btn");

for (let i = 0; i < buttonShowHide.length; i++) {
    buttonShowHide[i].addEventListener('click' || 'touchstart', () => {
        if (inputTypePass[i].getAttribute("type") == "password") {
            inputTypePass[i].setAttribute("type", "text");
            buttonShowHide[i].innerHTML = "<img src='/website/static/img/icons/view.png' />";
        } else {
            inputTypePass[i].setAttribute("type", "password");
            buttonShowHide[i].innerHTML = "<img src='/website/static/img/icons/hide.png' />";
        }
    })
}

buttonShowLoginPass1.addEventListener("click" || "touchstart", () => {
    if (inputLoginPass1.getAttribute("type") == "password") {
        inputLoginPass1.setAttribute("type", "text");
        buttonShowLoginPass1.innerHTML = "<img src='/website/static/img/icons/view.png' />";
    } else {
        inputLoginPass1.setAttribute("type", "password");
        buttonShowLoginPass1.innerHTML = "<img src='/website/static/img/icons/hide.png' />";
    }
});

buttonShowLoginPass2.addEventListener("click" || "touchstart", () => {
    if (inputLoginPass2.getAttribute("type") == "password") {
        inputLoginPass2.setAttribute("type", "text");
        buttonShowLoginPass2.innerHTML = "<img src='/website/static/img/icons/view.png' />";
    } else {
        inputLoginPass2.setAttribute("type", "password");
        buttonShowLoginPass2.innerHTML = "<img src='/website/static/img/icons/hide.png' />";
    }
})
