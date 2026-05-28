// Helper function to extract YouTube video ID
function extractYouTubeId(url) {
    const regExp =
        /^.*(youtu.be\/|v\/|u\/\w\/|embed\/|watch\?v=|&v=)([^#&?]*).*/;
    const match = url.match(regExp);
    return match && match[2].length === 11 ? match[2] : null;
}

// Secure YouTube video insertion function (keeps building iframe dynamically)
function insertYouTubeVideo() {
    const youtubeForm = document.querySelector(".youtube-form");
    const popup = document.querySelector(".video-buttons .popup");

    if (!youtubeForm) return;

    // Show form and focus input
    youtubeForm.style.display = "flex";
    if (popup) {
        popup.style.height = "auto";
        popup.style.padding = "2rem";
    }
    const input = document.getElementById("youtube-url");
    if (input) {
        input.value = ""; // clear previous
        input.focus();
    }
}

// Called by the small button next to the input in your template
function insertUrl() {
    const input = document.getElementById("youtube-url");
    if (!input) return;
    const url = input.value.trim();
    sendYoutubeUrl(url);
}

// -- Replace sendYoutubeUrl to insert only the link wrapper --
function sendYoutubeUrl(url) {
    if (!url || url.trim() === "") {
        alert("Por favor cole a URL do YouTube no campo.");
        return;
    }

    const videoId = extractYouTubeId(url.trim());
    if (!videoId || !/^[a-zA-Z0-9_-]{11}$/.test(videoId)) {
        alert(
            "❌ URL inválida! Use https://youtu.be/VIDEO_ID ou https://www.youtube.com/watch?v=VIDEO_ID"
        );
        return;
    }

    const youtubeHtml = buildYouTubeContentHtml(videoId);

    console.log("Inserted YouTube link wrapper into editor.");

    insertIntoEditor(youtubeHtml);
    showMediaPreview("YouTube Link", `Video ID: ${videoId}`);

    // Clear and hide the form
    const input = document.getElementById("youtube-url");
    if (input) input.value = "";
    const youtubeForm = document.querySelector(".youtube-form");
    if (youtubeForm) youtubeForm.style.display = "none";

    closePopup(".video-buttons");

    console.log(
        `✅ YouTube link inserted (video id ${videoId}). Iframe will be added on save.`
    );
}

function buildYouTubeLinkHtml(videoId) {
    return `
        <div class="youtube-link-wrapper"
            data-video-id="${videoId}"
            contenteditable="false"
            style="margin:1rem 0; text-align:left;">

            📺 <a href="https://www.youtube.com/watch?v=${videoId}"
                target="_blank"
                rel="noopener noreferrer">
                View on YouTube
            </a>

        </div>
        `;
}

// -- New helper: inject iframe tags into HTML payload before submit --
function buildYouTubeEmbedHtml(videoId) {
    return `
            <div class="youtube-video-container"
                style="
                    position: relative;
                    margin: 1.5rem 0;
                    padding-bottom: 56.25%;
                    overflow: hidden;
                    border-radius: 8px;"
            >
                <iframe
                    src="https://www.youtube.com/embed/${videoId}"
                    title="YouTube video player"
                    style="
                        position: absolute;
                        top: 0;
                        left: 0;
                        width: 100%;
                        height: 100%;"
                    frameborder="0"
                    allow="
                        accelerometer;
                        autoplay;
                        clipboard-write;
                        encrypted-media;
                        gyroscope;
                        picture-in-picture;
                        web-share"
                    referrerpolicy="strict-origin-when-cross-origin"
                    allowfullscreen
                ></iframe>
            </div>
        `;
}

function buildYouTubeContentHtml(videoId) {
    const linkHtml = buildYouTubeLinkHtml(videoId);
    const embedHtml = buildYouTubeEmbedHtml(videoId);

    return linkHtml + embedHtml;
}

function initYoutube() {
    const youtubeBtn = document.querySelector(".youtube-btn");
    const insertUrlBtn = document.querySelector(".insert-url-btn");

    if (youtubeBtn) {
        youtubeBtn.addEventListener("click", insertYouTubeVideo);
    }

    if (insertUrlBtn) {
        insertUrlBtn.addEventListener("click", insertUrl);
    }
}

window.initYoutube = initYoutube;
