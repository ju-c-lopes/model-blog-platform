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
});

// -- Update form submit handler to inject iframes before saving payload --
const form = document.querySelector("form");
if (form) {
    form.addEventListener("submit", function (e) {
        // Update hidden textarea with final content (after injecting iframes)
        if (window.quillEditor) {
            const currentHtml = window.quillEditor.root.innerHTML;
            const processedHtml = injectYouTubeIframes(currentHtml);
            document.getElementById("id_text").value = processedHtml;
        } else {
            // Fallback for non-Quill case: try to inject in textarea value
            const ta = document.getElementById("id_text");
            if (ta) {
                ta.value += injectYouTubeIframes(ta.value);
            }
        }

        // Basic validation (unchanged)
        const titleEl = document.getElementById("id_title");
        const title = titleEl ? titleEl.value.trim() : "";
        const contentText = window.quillEditor
            ? window.quillEditor.getText().trim()
            : "";

        if (!title) {
            alert("Please enter a title for your post.");
            e.preventDefault();
            return;
        }

        if (!contentText || contentText.length < 10) {
            alert(
                "Please write some content for your post (at least 10 characters)."
            );
            e.preventDefault();
            return;
        }
    });
}
