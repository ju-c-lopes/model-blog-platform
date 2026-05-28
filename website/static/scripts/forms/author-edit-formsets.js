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

    window.initFormsetDynamic({
        addButtonId: "add-graduation",
        listSelector: ".graduation-list",
        templateId: "graduation-empty-template",
        totalFormsSelector: 'input[name^="graduation"][name$="-TOTAL_FORMS"]',
        itemSelector: ".graduation-item",
    });

    window.initFormsetDynamic({
        addButtonId: "add-job",
        listSelector: ".job-list",
        templateId: "job-empty-template",
        totalFormsSelector: 'input[name^="job"][name$="-TOTAL_FORMS"]',
        itemSelector: ".job-item",
    });
});
