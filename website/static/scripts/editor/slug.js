function initSlug() {
    const urlSlugField = document.getElementById("id_url_slug");
    const titleField = document.getElementById("id_title");

    // Check if this is a new post by seeing if URL slug is empty
    const isCreating = !urlSlugField || !urlSlugField.value.trim();

    if (isCreating && titleField) {
        titleField.addEventListener("input", function () {
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
}

window.initSlug = initSlug;