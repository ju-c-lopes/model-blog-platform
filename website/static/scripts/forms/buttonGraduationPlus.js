/** @deprecated Carregue author-edit-formsets.js na página de edição do autor. */
document.addEventListener("DOMContentLoaded", function () {
    if (typeof window.initFormsetDynamic !== "function") {
        return;
    }
    window.initFormsetDynamic({
        addButtonId: "add-graduation",
        listSelector: ".graduation-list",
        templateId: "graduation-empty-template",
        totalFormsSelector: 'input[name^="graduation"][name$="-TOTAL_FORMS"]',
        itemSelector: ".graduation-item",
    });
});
