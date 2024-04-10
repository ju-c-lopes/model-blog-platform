const saveButton = document.querySelector(".save-button");
const mainFormDiv = document.querySelector("#main-form-div");
const unfilledSocialFields = document.querySelectorAll(".plus-field");
const excludeButton = document.querySelectorAll(".btn-exclude-social");

let plusClicked;

saveButton.addEventListener('click', () => {
    for (let i = 0; i < unfilledSocialFields.length; i+=2) {
        let emptyInput = unfilledSocialFields[i + 1].lastElementChild.querySelector("input").value.length == 0;
        if (!plusClicked) {
            unfilledSocialFields[i].lastElementChild.querySelector("td>select").remove();
            unfilledSocialFields[i + 1].lastElementChild.querySelector("input").remove();
        }
        else if (plusClicked && emptyInput) {
            unfilledSocialFields[i].lastElementChild.querySelector("td>select").remove();
            unfilledSocialFields[i + 1].lastElementChild.querySelector("input").remove();
        }
    }
});

for (let exclude of excludeButton) {
    exclude.addEventListener('click', () => {
        for (let i = 0; i < unfilledSocialFields.length; i+=2) {
            let emptyInput = unfilledSocialFields[i + 1].lastElementChild.querySelector("input").value.length == 0;
            if (!plusClicked) {
                unfilledSocialFields[i].lastElementChild.querySelector("td>select").remove();
                unfilledSocialFields[i + 1].lastElementChild.querySelector("input").remove();
            }
            else if (plusClicked && emptyInput) {
                unfilledSocialFields[i].lastElementChild.querySelector("td>select").remove();
                unfilledSocialFields[i + 1].lastElementChild.querySelector("input").remove();
            }
        }
    });
}

document.querySelector('.social-button-plus').addEventListener('click', () => {
    plusClicked = true;
})