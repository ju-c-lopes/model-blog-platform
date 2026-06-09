console.log("Edit Post JS loaded");

document.addEventListener("DOMContentLoaded", () => {
    initCounters();
    initSlug();
    initSlugTooltip();
    initQuillEditor();
    initPopup();
    initImageUpload();
    initVideoUpload();
    initYoutube();
    initTable();
    initCoverPreview();
    initHtmlSourceEditor();
});

// -- Update form submit handler to inject iframes before saving payload --
const form = document.querySelector("form");
if (form) {
    form.addEventListener("submit", function (e) {
        const htmlPaneActive = document.querySelector('.editor-pane[data-pane="html"]')?.classList.contains("is-active");
        const sourceEl = document.getElementById("html-source");
        const ta = document.getElementById("id_text");

        if (htmlPaneActive && sourceEl && ta) {
            ta.value = sourceEl.value;
        } else if (window.quillEditor && ta) {
            const currentHtml = window.quillEditor.root.innerHTML;
            const processedHtml =
                typeof injectYouTubeIframes === "function"
                    ? injectYouTubeIframes(currentHtml)
                    : currentHtml;
            ta.value = processedHtml;
        } else if (ta && typeof injectYouTubeIframes === "function") {
            ta.value = injectYouTubeIframes(ta.value);
        }

        // Basic validation (unchanged)
        const titleEl = document.getElementById("id_title");
        const title = titleEl ? titleEl.value.trim() : "";
        const contentText = window.quillEditor
            ? window.quillEditor.getText().trim()
            : "";

        if (!title) {
            alert("Informe um título para o post.");
            e.preventDefault();
            return;
        }

        if (!contentText || contentText.length < 10) {
            alert("Escreva o conteúdo do post (mínimo 10 caracteres).");
            e.preventDefault();
            return;
        }
    });
}
