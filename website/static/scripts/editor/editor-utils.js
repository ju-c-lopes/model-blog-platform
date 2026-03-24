function getEditorRange() {
    let range = window.quillEditor.getSelection();

    if (!range) {
        window.quillEditor.focus();
        range = window.quillEditor.getSelection();
    }

    if (!range) {
        range = {
            index: window.quillEditor.getLength(),
            length: 0
        };
    }

    return range;
}

function insertIntoEditor(html) {
    const range = getEditorRange();

    window.quillEditor.clipboard.dangerouslyPasteHTML(
        range.index,
        html + "<br><br>"
    );

    window.quillEditor.setSelection(range.index + 1);
}

window.getEditorRange = getEditorRange;
window.insertIntoEditor = insertIntoEditor;
