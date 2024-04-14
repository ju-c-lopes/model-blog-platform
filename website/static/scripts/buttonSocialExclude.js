const socialMedia = [
    [1, 'Facebook'],
    [2, 'Instagram'],
    [3, 'LinkedIn'],
    [4, 'X'],
]

var buttonFieldExclude = document.querySelectorAll(".form-table-social>tbody>tr>td");

for (let i = 1; i < buttonFieldExclude.length - 2; i += 4) {
    buttonFieldExclude[i].classList.add("td-for-button");
}

var buttonExclude = document.querySelectorAll(".btn-exclude-social");

for (let bt of buttonExclude) {
    for (let social of socialMedia) {
        bt.addEventListener('click', () => {
            if (social[0] == bt.id) {
                let inputField = bt.parentNode.querySelector("input");
                inputField.value = social[0];
            }
        });
    }
}
