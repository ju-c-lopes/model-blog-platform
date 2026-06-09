function initCoverPreview() {
    const input = document.getElementById("id_cover_image");
    const previewWrap = document.getElementById("cover-preview");
    const previewImg = document.getElementById("cover-preview-img");

    if (!input || !previewWrap || !previewImg) return;

    input.addEventListener("change", () => {
        const file = input.files && input.files[0];
        if (!file) {
            previewWrap.hidden = true;
            previewImg.removeAttribute("src");
            return;
        }

        previewImg.src = URL.createObjectURL(file);
        previewWrap.hidden = false;
    });
}

window.initCoverPreview = initCoverPreview;
