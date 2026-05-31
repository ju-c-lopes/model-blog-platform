const saveButton = document.querySelector(".save-button");
const unfilledSocialFields = document.querySelectorAll(".plus-field");
const excludeButton = document.querySelectorAll(".btn-exclude-social");
const socialPlusButton = document.querySelector(".social-button-plus");

let plusClicked;

function removeEmptySocialFields() {
    for (let i = 0; i < unfilledSocialFields.length; i += 2) {
        const emptyInput =
            unfilledSocialFields[i + 1].lastElementChild.querySelector("input")
                .value.length === 0;
        if (!plusClicked || (plusClicked && emptyInput)) {
            unfilledSocialFields[i].lastElementChild.querySelector("td>select").remove();
            unfilledSocialFields[i + 1].lastElementChild
                .querySelector("input")
                .remove();
        }
    }
}

if (saveButton && unfilledSocialFields.length) {
    saveButton.addEventListener("click", removeEmptySocialFields);
}

for (const exclude of excludeButton) {
    exclude.addEventListener("click", removeEmptySocialFields);
}

if (socialPlusButton) {
    socialPlusButton.addEventListener("click", () => {
        plusClicked = true;
    });
}
