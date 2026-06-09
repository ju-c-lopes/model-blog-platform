function initHtmlSourceEditor() {
    const sourceEl = document.getElementById("html-source");
    const toggleButtons = document.querySelectorAll(".editor-toggle-btn");
    const panes = document.querySelectorAll(".editor-pane");
    const hiddenTextarea = document.getElementById("id_text");

    if (!sourceEl || !toggleButtons.length) return;

    function syncQuillToSource() {
        if (!window.quillEditor) return;
        sourceEl.value = window.quillEditor.root.innerHTML;
    }

    function syncSourceToQuill() {
        if (!window.quillEditor) return;
        const html = sourceEl.value;
        window.quillEditor.root.innerHTML = html;
        if (hiddenTextarea) {
            hiddenTextarea.value = html;
        }
    }

    function syncSourceToHidden() {
        if (hiddenTextarea) {
            hiddenTextarea.value = sourceEl.value;
        }
    }

    toggleButtons.forEach((btn) => {
        btn.addEventListener("click", () => {
            const mode = btn.dataset.mode;
            const wasHtml = document.querySelector('.editor-pane[data-pane="html"]')?.classList.contains("is-active");

            if (mode === "html" && !wasHtml) {
                syncQuillToSource();
            } else if (mode === "editor" && wasHtml) {
                syncSourceToQuill();
            }

            toggleButtons.forEach((b) => b.classList.toggle("is-active", b === btn));
            panes.forEach((pane) => {
                const active = pane.dataset.pane === mode;
                pane.classList.toggle("is-active", active);
                pane.hidden = !active;
            });

            if (mode === "html") {
                sourceEl.focus();
            }
        });
    });

    sourceEl.addEventListener("input", syncSourceToHidden);

    const form = document.querySelector("form");
    if (form) {
        form.addEventListener("submit", () => {
            const htmlPaneActive = document.querySelector('.editor-pane[data-pane="html"]')?.classList.contains("is-active");
            if (htmlPaneActive) {
                syncSourceToHidden();
            } else if (window.quillEditor && hiddenTextarea) {
                hiddenTextarea.value = window.quillEditor.root.innerHTML;
            }
        });
    }
}

window.initHtmlSourceEditor = initHtmlSourceEditor;
