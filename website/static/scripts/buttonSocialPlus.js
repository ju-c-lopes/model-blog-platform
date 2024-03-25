const socialPlus = document.querySelector(".social-button-plus");
var newSocialFields = document.querySelectorAll(".plus-field");
console.log(newSocialFields)

checkMaxNodes()
socialPlus.addEventListener('click', function() {
    for (let i = 0; i < 1; i++) {
        newSocialFields[i].style.display = 'flex';
        newSocialFields[i].classList.remove('plus-field');
        newSocialFields[i + 1].style.display = 'flex';
        newSocialFields[i + 1].classList.remove('plus-field');
        newSocialFields = document.querySelectorAll(".plus-field");
    }
    checkMaxNodes();
    console.log(newSocialFields)
});

function checkMaxNodes() {
    if (newSocialFields.length == 0) {
        socialPlus.style.display = 'none';
        document.querySelector(".save-button").style.marginTop = "3vh";
    }
}