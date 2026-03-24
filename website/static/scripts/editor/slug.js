function initSlug() {
    const urlSlugField = document.getElementById("id_url_slug");
    const titleField = document.getElementById("id_title");

    if (!urlSlugField || !titleField) return;

    let slugWasEditedManually = false;

    urlSlugField.addEventListener("input", () => {
        slugWasEditedManually = true;
    });

    titleField.addEventListener("input", function () {
        if (slugWasEditedManually) return;

        const title = this.value;
        const slug = title
            .normalize("NFD")
            .replace(/[\u0300-\u036f]/g, "")
            .toLowerCase()
            .replace(/[^a-z0-9\s-]/g, "")
            .replace(/\s+/g, "-")
            .replace(/-+/g, "-")
            .replace(/^-|-$/g, "");

        urlSlugField.value = slug;
    });
}

function initSlugTooltip() {
    const icon = document.getElementById("slug-info");
    const tooltip = document.getElementById("slug-tooltip");

    if (icon && tooltip) {
        icon.addEventListener("click", (event) => {
            event.stopPropagation();
            tooltip.classList.toggle("show");
        });

        tooltip.addEventListener("click", (event) => {
            event.stopPropagation();
        });

        document.addEventListener("click", () => {
            tooltip.classList.remove("show");
        })
    }
}

window.initSlug = initSlug;
window.initSlugTooltip = initSlugTooltip;