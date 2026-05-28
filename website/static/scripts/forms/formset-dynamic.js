/**
 * Utilitário para formsets inline Django (empty_form + __prefix__).
 * Expõe initFormsetDynamic no escopo global para templates sem bundler.
 */
(function (global) {
    function normalizeFormsetBlock(el) {
        if (!el) return;

        el.querySelectorAll("select").forEach((s) =>
            s.classList.add("custom-select")
        );
        el.querySelectorAll(
            'input[type="text"], input[type="number"], input[type="url"]'
        ).forEach((i) => i.classList.add("form-control"));
        el.querySelectorAll('input[type="checkbox"]').forEach((cb) =>
            cb.classList.add("form-check-input")
        );
        el.querySelectorAll("textarea").forEach((ta) =>
            ta.classList.add("form-control")
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

    function initFormsetDynamic(options) {
        const {
            addButtonId,
            listSelector,
            templateId,
            totalFormsSelector,
            itemSelector,
        } = options;

        const addBtn = document.getElementById(addButtonId);
        const container = document.querySelector(listSelector);
        const template = document.getElementById(templateId);
        const totalFormsInput = document.querySelector(totalFormsSelector);

        document.querySelectorAll(itemSelector).forEach(normalizeFormsetBlock);

        if (!addBtn || !container || !template || !totalFormsInput) {
            return;
        }

        addBtn.addEventListener("click", function () {
            const index = parseInt(totalFormsInput.value, 10);
            const newHtml = template.innerHTML.replace(/__prefix__/g, index);
            container.insertAdjacentHTML("beforeend", newHtml);
            totalFormsInput.value = index + 1;

            const blocks = container.querySelectorAll(itemSelector);
            const el = blocks[blocks.length - 1];
            normalizeFormsetBlock(el);

            const firstInput = el.querySelector("input, select, textarea");
            if (firstInput) firstInput.focus();
        });
    }

    global.initFormsetDynamic = initFormsetDynamic;
})(window);
