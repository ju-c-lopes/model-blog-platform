var checkPass = {
    "Upper": /[A-Z]/g,
    "Number": /[0-9]/g,
    "Special": /[\W_]/g,
    "Len": function(password) {
        return (password.length >= 10 && password.length <= 16);
    }
};

var checked = {
    "Upper": false,
    "Number": false,
    "Special": false,
    "Len": false,
};

var inputPassOne = document.querySelector("input#id_password1");
var inputPassTwo = document.querySelector("input#id_password2");
var buttonFinishRegister = document.querySelector("#finish-register");

buttonFinishRegister.disabled = true;
buttonFinishRegister.classList.add("btn-disabled");

inputPassOne.addEventListener('focus', () => {
    document.querySelector(".popup-validate").style.height = "auto";
    document.querySelector(".popup-validate").style.display = "flex";
    document.querySelector(".popup-validate").style.visibility = "visible";
    document.querySelector(".popup-validate").style.padding = "0.3em 0.3em 0.3em 0.3em";
})

inputPassOne.addEventListener('input', (passValue) => {
    let passTyped = passValue.target.value;
    lineChecks = document.querySelectorAll(".popup-validate>ul>li");

    checked.Upper = (passTyped.match(checkPass.Upper)) === null ? false : passTyped.match(checkPass.Upper).length > 0;
    if (checked.Upper) {
        checked.Upper = true;
        lineChecks[0].style.color = "green";
        lineChecks[0].textContent = "✅ A senha contém letra maiúscula."
    } else {
        checked.Upper = false;
        lineChecks[0].style.color = "red";
        lineChecks[0].textContent = "❌ Pelo menos 1 letra maiúscula."
    }

    checked.Number = (passTyped.match(checkPass.Number)) === null ? false : passTyped.match(checkPass.Number).length > 0;
    if (checked.Number) {
        checked.Number = true;
        lineChecks[1].style.color = "green";
        lineChecks[1].textContent = "✅ A senha contém número."
    } else {
        checked.Number = false;
        lineChecks[1].style.color = "red";
        lineChecks[1].textContent = "❌ Pelo menos 1 número."
    }

    checked.Special = (passTyped.match(checkPass.Special)) === null ? false : passTyped.match(checkPass.Special).length > 0;
    if (checked.Special) {
        checked.Special = true;
        lineChecks[2].style.color = "green";
        lineChecks[2].textContent = "✅ A senha contém caractere especial."
    } else {
        checked.Special = false;
        lineChecks[2].style.color = "red";
        lineChecks[2].textContent = "❌ Pelo menos 1 caractere especial."
    }

    if (checkPass.Len(passTyped)) {
        checked.Len = true;
        lineChecks[3].style.color = "green";
        lineChecks[3].textContent = "✅ A senha tem tamanho adequado."
    } else {
        checked.Len = false;
        lineChecks[3].style.color = "red";
        lineChecks[3].textContent = "❌ Entre 10 a 16 caracteres."
    }

    if (checkPass.Upper && checkPass.Number && checkPass.Special && checkPass.Len) {
        inputPassTwo.addEventListener('input', () => {
            if (inputPassOne.value === inputPassTwo.value) {
                buttonFinishRegister.removeAttribute("disabled");
                buttonFinishRegister.classList.remove("btn-disabled");
            } else {
                buttonFinishRegister.setAttribute("disabled", "");
                buttonFinishRegister.classList.add("btn-disabled");
            }
        });
    }
});
