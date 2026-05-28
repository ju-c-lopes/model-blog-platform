function handleImageUpload(event) {
    const file = event.target.files[0];
    if (file && window.quillEditor) {
        const reader = new FileReader();
        reader.onload = function (e) {
            const range = window.quillEditor.getSelection(true);
            window.quillEditor.insertEmbed(
                range ? range.index : 0,
                "image",
                e.target.result
            );
            window.quillEditor.setSelection(range.index + 1);
            showMediaPreview("Image", file.name);
        };
        reader.readAsDataURL(file);
    }
}

function initImageUpload() {
    const imageBtn = document.querySelector(".media-image-btn");
    const imageInput = document.getElementById("image-upload");

    if (imageBtn && imageInput) {
        imageBtn.addEventListener("click", () => {
            imageInput.click();
        });
        imageInput.addEventListener("change", handleImageUpload);
    }
}

window.initImageUpload = initImageUpload;
