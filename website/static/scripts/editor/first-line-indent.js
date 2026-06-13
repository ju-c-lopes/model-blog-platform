const FIRST_LINE_INDENT = "\u00A0".repeat(4);

function insertFirstLineIndent(quill) {
    const range = quill.getSelection(true);
    if (range == null) {
        return;
    }

    const lineResult = quill.getLine(range.index);
    if (!lineResult) {
        return;
    }

    const line = lineResult[0];
    const lineStart = quill.getIndex(line);
    quill.insertText(lineStart, FIRST_LINE_INDENT, "user");

    const cursor = range.index >= lineStart ? range.index + FIRST_LINE_INDENT.length : range.index;
    quill.setSelection(cursor, 0, "user");

    const textarea = document.getElementById("id_text");
    if (textarea) {
        textarea.value = quill.root.innerHTML;
    }
}

function initFirstLineIndentButton() {
    const button = document.getElementById("btn-first-line-indent");
    if (!button) {
        return;
    }

    button.addEventListener("click", () => {
        if (!window.quillEditor) {
            return;
        }
        insertFirstLineIndent(window.quillEditor);
        window.quillEditor.focus();
    });
}

window.initFirstLineIndentButton = initFirstLineIndentButton;
