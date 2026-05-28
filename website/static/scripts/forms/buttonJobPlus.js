/** @deprecated Carregue author-edit-formsets.js na página de edição do autor. */
document.addEventListener("DOMContentLoaded", function () {
    if (typeof window.initFormsetDynamic !== "function") {
        return;
    }
    window.initFormsetDynamic({
        addButtonId: "add-job",
        listSelector: ".job-list",
        templateId: "job-empty-template",
        totalFormsSelector: 'input[name^="job"][name$="-TOTAL_FORMS"]',
        itemSelector: ".job-item",
    });
});
