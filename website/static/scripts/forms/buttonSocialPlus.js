document.addEventListener("DOMContentLoaded", function () {
    const addBtn = document.getElementById("add-social");
    const container = document.querySelector(".social-list");
    const template = document.getElementById("social-empty-template");
    const totalFormsInput = document.querySelector(
        'input[name^="social"][name$="-TOTAL_FORMS"]'
    );

    function normalizeBlock(el) {
        if (!el) return;
        el.querySelectorAll("select").forEach((s) =>
            s.classList.add("custom-select")
        );
        el.querySelectorAll('input[type="text"], input[type="number"], input[type="url"]').forEach(
            (i) => i.classList.add("form-control")
        );
        el.querySelectorAll('input[type="checkbox"]').forEach((cb) =>
            cb.classList.add("form-check-input")
        );

        el.querySelectorAll("select").forEach((s) => {
            if (!s.closest(".select-wrapper")) {
                const wrap = document.createElement("div");
                wrap.className = "select-wrapper";
                s.parentNode.insertBefore(wrap, s);
                wrap.appendChild(s);
            }
        });
    }

    // normalize existing blocks
    document.querySelectorAll(".social-item").forEach(normalizeBlock);

    if (!addBtn || !container || !template || !totalFormsInput) return;

    addBtn.addEventListener("click", function () {
        const index = parseInt(totalFormsInput.value, 10);
        let newHtml = template.innerHTML.replace(/__prefix__/g, index);
        container.insertAdjacentHTML("beforeend", newHtml);
        totalFormsInput.value = index + 1;

        const blocks = container.querySelectorAll(".social-item");
        const el = blocks[blocks.length - 1];
        normalizeBlock(el);

        const firstInput = el.querySelector("input, select, textarea");
        if (firstInput) firstInput.focus();
    });
});
