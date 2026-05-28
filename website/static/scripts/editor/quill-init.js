function initQuillEditor() {
    // Check if Quill is loaded
    if (typeof Quill === "undefined") {
        console.error("ERROR: Quill.js is not loaded! Check your CDN link.");
        return;
    }

    // Initialize Quill Rich Text Editor
    const editorContainer = document.querySelector("#rich-editor-container");

    if (editorContainer) {
        const quill = new Quill("#rich-editor-container", {
            theme: "snow",
            modules: {
                toolbar: [
                    [{ header: [2, 3, 4, false] }],
                    ["bold", "italic", "underline", "strike"],
                    [{ color: [] }, { background: [] }],
                    [{ font: [] }],
                    [{ align: [] }],
                    ["blockquote", "code-block"],
                    [{ list: "ordered" }, { list: "bullet" }],
                    [{ indent: "-1" }, { indent: "+1" }],
                    ["link"], // image & video removed
                    ["clean"],
                ],
                // no custom video handler here
            },
            placeholder: "Start writing your content here...",
        });

        // Set initial content if editing
        const textarea = document.getElementById("id_text");
        const initialContent = textarea ? textarea.value : "";

        console.log(initialContent.length > 0);
        if (initialContent.length > 0) {
            document.querySelector(".ql-editor").innerHTML = initialContent;
            console.log("entrou")
        }
        console.log("quill root after init:", document.querySelector(".ql-editor"));

        // Update hidden textarea when content changes
        quill.on("text-change", function () {
            textarea.value = quill.root.innerHTML;
        });

        // Make quill globally accessible for media functions
        window.quillEditor = quill;
    } else {
        console.error("ERROR: Rich editor container not found!");
    }
}

window.initQuillEditor = initQuillEditor;
