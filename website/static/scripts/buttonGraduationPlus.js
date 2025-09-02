const graduationPlus = document.querySelector(".graduation-button-plus");
var newGraduationFields = document.querySelectorAll(".plus-field");

checkMaxNodes();
// graduationPlus.addEventListener("click", () => {
//     const newGraduation = document.createElement("div");
//     newGraduation.classList.add("plus-field");
//     newGraduation.innerHTML = `
//         <label for="graduation">Nova Graduação</label>
//         <input type="text" name="graduation" id="graduation" />
//     `;
//     document.querySelector(".graduation-fields").appendChild(newGraduation);
//     // for (let i = 0; i < 1; i++) {
//     //     newGraduationFields[i].style.visibility = 'visible';
//     //     newGraduationFields[i].style.height = 'auto';
//     //     newGraduationFields[i].classList.remove('plus-field');
//     //     newGraduationFields[i + 1].style.visibility = 'visible';
//     //     newGraduationFields[i + 1].style.height = 'auto';
//     //     newGraduationFields[i + 1].classList.remove('plus-field');
//     //     newGraduationFields = document.querySelectorAll(".plus-field");
//     // }
//     // checkMaxNodes();
// });

// function checkMaxNodes() {
//     if (newGraduationFields.length == 0) {
//         graduationPlus.style.display = "none";
//         document.querySelector(".plus-button-field").style.margin = "0";
//         document.querySelector(".save-button").style.marginTop = "1vh";
//     }
// }

document.addEventListener("DOMContentLoaded", function () {
    const addBtn = document.getElementById("add-graduation");
    const container = document.querySelector(".graduation-list");
    const template = document.getElementById("graduation-empty-template");
    const totalFormsInput = document.querySelector(
        'input[name$="-TOTAL_FORMS"]'
    );

    // função utilitária para padronizar um bloco (server-rendered ou novo)
    function normalizeBlock(el) {
        if (!el) return;
        // adiciona classes nos inputs/selects
        el.querySelectorAll("select").forEach((s) =>
            s.classList.add("custom-select")
        );
        el.querySelectorAll('input[type="text"], input[type="number"]').forEach(
            (i) => i.classList.add("form-control")
        );
        el.querySelectorAll('input[type="checkbox"]').forEach((cb) =>
            cb.classList.add("form-check-input")
        );

        // envolve selects com .select-wrapper se ainda não estiverem
        el.querySelectorAll("select").forEach((s) => {
            if (!s.closest(".select-wrapper")) {
                const wrap = document.createElement("div");
                wrap.className = "select-wrapper";
                s.parentNode.insertBefore(wrap, s);
                wrap.appendChild(s);
            }
        });
    }

    // normaliza blocos já renderizados
    document.querySelectorAll(".graduation-item").forEach(normalizeBlock);

    if (!addBtn || !container || !template || !totalFormsInput) return;

    addBtn.addEventListener("click", function () {
        const index = parseInt(totalFormsInput.value, 10);
        let newHtml = template.innerHTML.replace(/__prefix__/g, index);
        container.insertAdjacentHTML("beforeend", newHtml);
        totalFormsInput.value = index + 1;

        // pega o bloco recém-adicionado e normaliza
        const blocks = container.querySelectorAll(".graduation-item");
        const el = blocks[blocks.length - 1];
        normalizeBlock(el);

        // foco no primeiro campo do novo bloco
        const firstInput = el.querySelector("input, select, textarea");
        if (firstInput) firstInput.focus();
    });
});
