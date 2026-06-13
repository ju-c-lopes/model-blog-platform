console.log("Edit Post JS loaded");

document.addEventListener("DOMContentLoaded", () => {
    initCounters();
    initSlug();
    initSlugTooltip();
    initQuillEditor();
    initFirstLineIndentButton();
    initPopup();
    initImageUpload();
    initVideoUpload();
    initYoutube();
    initTable();
    initCoverPreview();
    initTagPicker();
    initHtmlSourceEditor();
});

// -- Sync Quill content into textarea before submit --
const form = document.querySelector("form");
if (form) {
    form.addEventListener("submit", function (e) {
        const htmlPaneActive = document.querySelector('.editor-pane[data-pane="html"]')?.classList.contains("is-active");
        const sourceEl = document.getElementById("html-source");
        const ta = document.getElementById("id_text");

        if (htmlPaneActive && sourceEl && ta) {
            ta.value = sourceEl.value;
        } else if (window.quillEditor && ta) {
            ta.value = window.quillEditor.root.innerHTML;
        }

        const titleEl = document.getElementById("id_title");
        const title = titleEl ? titleEl.value.trim() : "";
        const contentHtml = ta ? ta.value : "";
        const contentText = contentHtml.replace(/<[^>]*>/g, " ").replace(/\s+/g, " ").trim();

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
