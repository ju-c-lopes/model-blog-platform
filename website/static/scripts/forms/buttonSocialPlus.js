/** @deprecated Carregue author-edit-formsets.js na página de edição do autor. */
document.addEventListener("DOMContentLoaded", function () {
    if (typeof window.initFormsetDynamic !== "function") {
        return;
    }
    window.initFormsetDynamic({
        addButtonId: "add-social",
        listSelector: ".social-list",
        templateId: "social-empty-template",
        totalFormsSelector: 'input[name^="social"][name$="-TOTAL_FORMS"]',
        itemSelector: ".social-item",
    });
});
