function handleVideoUpload(event) {
    const file = event.target.files[0];
    if (file && window.quillEditor) {
        // Check file size (limit to 10MB for better performance)
        if (file.size > 10 * 1024 * 1024) {
            alert(
                "Video file is too large. Please choose a file smaller than 10MB or use a video hosting service like YouTube."
            );
            return;
        }

        // Check if it's a video file
        if (!file.type.startsWith("video/")) {
            alert("Please select a video file.");
            return;
        }

        const reader = new FileReader();
        reader.onload = function (e) {
            const range = window.quillEditor.getSelection(true);
            // Create a more robust video element
            const videoHtml = `<video controls style="max-width: 100%; height: auto;" src="${e.target.result}">
                Your browser does not support the video tag.
            </video>`;

            window.quillEditor.clipboard.dangerouslyPasteHTML(
                range ? range.index : 0,
                videoHtml
            );
            showMediaPreview("Video", file.name);
            closePopup(".video-buttons");
            event.target.value = "";
        };
        reader.readAsDataURL(file);
    }
}

function initVideoUpload() {
    const videoUploadBtn = document.querySelector(".local-btn");
    const videoInput = document.getElementById("video-upload");

    if (videoUploadBtn && videoInput) {
        console.log("Clicking Video Upload button")
        videoUploadBtn.addEventListener("click", () => {
            videoInput.click();
        })
        videoInput.addEventListener("change", handleVideoUpload);
    }
}

window.initVideoUpload = initVideoUpload;
