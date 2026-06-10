function extractYouTubeId(url) {
    const regExp =
        /^.*(youtu.be\/|v\/|u\/\w\/|embed\/|watch\?v=|&v=)([^#&?]*).*/;
    const match = url.match(regExp);
    return match && match[2].length === 11 ? match[2] : null;
}

function buildYouTubeEmbedUrl(videoId) {
    return `https://www.youtube.com/embed/${videoId}`;
}

function syncEditorTextarea() {
    const textarea = document.getElementById("id_text");
    if (textarea && window.quillEditor) {
        textarea.value = window.quillEditor.root.innerHTML;
    }
}

function insertYouTubeVideo() {
    const youtubeForm = document.querySelector(".youtube-form");
    const popup = document.querySelector(".video-buttons .popup");

    if (!youtubeForm) return;

    youtubeForm.style.display = "flex";
    if (popup) {
        popup.style.height = "auto";
        popup.style.padding = "2rem";
    }
    const input = document.getElementById("youtube-url");
    if (input) {
        input.value = "";
        input.focus();
    }
}

function insertUrl() {
    const input = document.getElementById("youtube-url");
    if (!input) return;
    sendYoutubeUrl(input.value.trim());
}

function sendYoutubeUrl(url) {
    if (!url) {
        alert("Por favor cole a URL do YouTube no campo.");
        return;
    }

    const videoId = extractYouTubeId(url);
    if (!videoId || !/^[a-zA-Z0-9_-]{11}$/.test(videoId)) {
        alert(
            "URL inválida. Use https://youtu.be/VIDEO_ID ou https://www.youtube.com/watch?v=VIDEO_ID"
        );
        return;
    }

    if (!window.quillEditor) {
        alert("Editor não disponível.");
        return;
    }

    const embedUrl = buildYouTubeEmbedUrl(videoId);
    const range = getEditorRange();

    window.quillEditor.insertEmbed(range.index, "video", embedUrl);
    window.quillEditor.insertText(range.index + 1, "\n\n");
    window.quillEditor.setSelection(range.index + 3, 0);

    syncEditorTextarea();
    showMediaPreview("YouTube", `Vídeo ${videoId}`);

    const input = document.getElementById("youtube-url");
    if (input) input.value = "";
    const youtubeForm = document.querySelector(".youtube-form");
    if (youtubeForm) youtubeForm.style.display = "none";

    closePopup(".video-buttons");
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
window.extractYouTubeId = extractYouTubeId;
window.buildYouTubeEmbedUrl = buildYouTubeEmbedUrl;
