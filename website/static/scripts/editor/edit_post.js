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

    // const imageBtn = document.querySelector(".media-image-btn");
    // const imageInput = document.getElementById("image-upload");
    // const videoUploadBtn = document.querySelector(".local-btn");
    // const videoInput = document.getElementById("video-upload");
    // const youtubeBtn = document.querySelector(".youtube-btn");
    // const insertUrlBtn = document.querySelector(".insert-url-btn");

    console.log({
        imageBtn,
        imageInput,
        videoUploadBtn,
        videoInput
    });
    
    // if (imageBtn && imageInput) {
    //     imageBtn.addEventListener("click", () => {
    //         imageInput.click();
    //     });
    //     imageInput.addEventListener("change", handleImageUpload);
    // }
    // if (videoUploadBtn && videoInput) {
    //     console.log("Clicking Video Upload button")
    //     videoUploadBtn.addEventListener("click", () => {
    //         videoInput.click();
    //     })
    //     videoInput.addEventListener("change", handleVideoUpload);
    // }

    // if (youtubeBtn) {
    //     youtubeBtn.addEventListener("click", insertYouTubeVideo);
    // }

    // if (insertUrlBtn) {
    //     insertUrlBtn.addEventListener("click", insertUrl);
    // }
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
