const socialPlus = document.querySelector(".social-button-plus");
var newSocialFields = document.querySelectorAll(".plus-field");

checkMaxNodes()
socialPlus.addEventListener('click', () => {
    for (let i = 0; i < 1; i++) {
        newSocialFields[i].style.display = 'flex';
        newSocialFields[i].classList.remove('plus-field');
        newSocialFields[i + 1].style.display = 'flex';
        newSocialFields[i + 1].classList.remove('plus-field');
        newSocialFields = document.querySelectorAll(".plus-field");
    }
    checkMaxNodes();
});

function checkMaxNodes() {
    if (newSocialFields.length == 0) {
        socialPlus.style.display = 'none';
        document.querySelector(".plus-button-field").style.margin = "0";
        document.querySelector(".save-button").style.marginTop = "1vh";
    }
}

const optionSelected = document.querySelectorAll(".op-selected");
const optionToDisable = document.querySelectorAll(".plus-options");

for (let disable of optionToDisable) {
    for (let mediaSelected of optionSelected)  {
        if (mediaSelected.text == disable.text) {
            disable.setAttribute("disabled", "");
        }
    }
};
