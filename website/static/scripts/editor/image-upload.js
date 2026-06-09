function getUploadConfig() {
    const container = document.querySelector(".post-form-container");
    if (!container) return null;

    return {
        uploadUrl: container.dataset.uploadUrl,
        uploadSessionId: container.dataset.uploadSessionId || "",
        postSlug: container.dataset.postSlug || "",
    };
}

function getCsrfToken() {
    const input = document.querySelector("[name=csrfmiddlewaretoken]");
    return input ? input.value : "";
}

async function uploadContentImage(file) {
    const config = getUploadConfig();
    if (!config || !config.uploadUrl) {
        throw new Error("Upload de imagem não configurado.");
    }

    const formData = new FormData();
    formData.append("image", file);

    if (config.postSlug) {
        formData.append("url_slug", config.postSlug);
    } else if (config.uploadSessionId) {
        formData.append("upload_session_id", config.uploadSessionId);
    }

    const response = await fetch(config.uploadUrl, {
        method: "POST",
        credentials: "same-origin",
        headers: {
            "X-CSRFToken": getCsrfToken(),
        },
        body: formData,
    });

    const data = await response.json();
    if (!response.ok || !data.success) {
        throw new Error(data.error || "Falha ao enviar imagem.");
    }

    return data.url;
}

async function handleImageUpload(event) {
    const file = event.target.files[0];
    if (!file || !window.quillEditor) return;

    try {
        const imageUrl = await uploadContentImage(file);
        const range = window.quillEditor.getSelection(true);
        const index = range ? range.index : 0;

        window.quillEditor.insertEmbed(index, "image", imageUrl);
        window.quillEditor.setSelection(index + 1);
        showMediaPreview("Imagem", file.name);
    } catch (error) {
        alert(error.message || "Não foi possível enviar a imagem.");
    } finally {
        event.target.value = "";
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
