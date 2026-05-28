/* TECH-COMMITMENT:
    Local video upload flow is validated up to HTML generation,
    but Quill currently discards the inserted video block/data-url content.

    Current limitation:
    - local video HTML is built and sent to the editor
    - Quill does not render/preserve the block inside the editable area

    Future improvement:
    - evaluate custom Quill blot/module for video
    - or persist local video separately and render outside Quill flow
    - or replace with storage-backed media URL workflow

    Reason:
    Avoid overengineering during current editor stabilization phase.
*/

function handleVideoUpload(event) {
    const file = event.target.files[0];
    console.log("Selected video file:", file);
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
            // // Create a more robust video element
            // const videoHtml = `
            //     <div class="local-video-wrapper" contenteditable="false" style="margin: 1rem 0;">
            //         <video
            //             controls
            //             preload="metadata"
            //             style="
            //                 max-width: 100%;
            //                 height: auto;"
            //             src="${e.target.result}"
            //         >
            //         </video>
            //     </div>`;
            const placeholderHtml = `
                <div class="local-video-placeholder" contenteditable="false">
                    🎥 Vídeo local inserido: ${file.name}
                </div>
            `;

            insertIntoEditor(placeholderHtml);
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
