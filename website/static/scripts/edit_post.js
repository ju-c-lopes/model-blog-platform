/**
 * Edit Post Page JavaScript
 * Handles rich text editor, character modules: {
                toolbar: [
                    [{ header: [1, 2, 3, 4, 5, 6, false] }],
                    ["bold", "italic", "underline", "strike"],
                    [{ color: [] }, { background: [] }],
                    [{ font: [] }],
                    [{ align: [] }],
                    ["blockquote", "code-block"],
                    [{ list: "ordered" }, { list: "bullet" }],
                    [{ indent: "-1" }, { indent: "+1" }],
                    ["link", "image"], // removed "video" here
                    ["clean"],
                ],
                // Removed video handler - using custom YouTube button instead
            },ploads, and form validation
 * Works for both creating new posts and editing existing posts
 */
console.log("Edit Post JS loaded");

// Character counters
function updateCharCounter(inputId, counterId, maxLength) {
    const input = document.getElementById(inputId);
    const counter = document.getElementById(counterId);

    if (!input || !counter) return;

    function updateCounter() {
        const currentLength = input.value.length;
        counter.textContent = `${currentLength}/${maxLength}`;

        // Update counter color based on usage
        counter.classList.remove("warning", "danger");
        if (currentLength > maxLength * 0.8) {
            counter.classList.add("warning");
        }
        if (currentLength > maxLength * 0.95) {
            counter.classList.add("danger");
        }
    }

    input.addEventListener("input", updateCounter);
    updateCounter(); // Initial count
}

// Initialize character counters and Quill editor when DOM is ready
document.addEventListener("DOMContentLoaded", function () {
    // Character counters
    updateCharCounter("id_title", "title-counter", 200);
    updateCharCounter("id_meta_description", "meta-counter", 160);

    // Auto-generate URL slug from title (only if creating new post)
    const urlSlugField = document.getElementById("id_url_slug");
    const titleField = document.getElementById("id_title");

    // Check if this is a new post by seeing if URL slug is empty
    const isCreating = !urlSlugField || !urlSlugField.value.trim();

    if (isCreating && titleField) {
        titleField.addEventListener("input", function () {
            const title = this.value;
            const slug = title
                .toLowerCase()
                .replace(/[^a-z0-9\s-]/g, "") // Remove special characters
                .replace(/\s+/g, "-") // Replace spaces with hyphens
                .replace(/-+/g, "-") // Replace multiple hyphens with single
                .replace(/^-|-$/g, ""); // Remove leading/trailing hyphens

            urlSlugField.value = slug;
        });
    }

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
                    [{ header: [1, 2, 3, 4, 5, 6, false] }],
                    ["bold", "italic", "underline", "strike"],
                    [{ color: [] }, { background: [] }],
                    [{ font: [] }],
                    [{ align: [] }],
                    ["blockquote", "code-block"],
                    [{ list: "ordered" }, { list: "bullet" }],
                    [{ indent: "-1" }, { indent: "+1" }],
                    ["link", "image"], // video removed
                    ["clean"],
                ],
                // no custom video handler here
            },
            placeholder: "Start writing your amazing content here...",
        });

        // Set initial content if editing
        const initialContent = document.getElementById("id_text").value;
        console.log("Initial content:", initialContent);
        if (initialContent) {
            quill.root.innerHTML = initialContent;
        }

        // Update hidden textarea when content changes
        quill.on("text-change", function () {
            document.getElementById("id_text").value = initialContent;
        });

        // Make quill globally accessible for media functions
        window.quillEditor = quill;
    } else {
        console.error("ERROR: Rich editor container not found!");
    }
});

// Media upload functions
function handleImageUpload(event) {
    const file = event.target.files[0];
    if (file && window.quillEditor) {
        const reader = new FileReader();
        reader.onload = function (e) {
            const range = window.quillEditor.getSelection();
            window.quillEditor.insertEmbed(
                range ? range.index : 0,
                "image",
                e.target.result
            );
            showMediaPreview("Image", file.name);
        };
        reader.readAsDataURL(file);
    }
}

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
            const range = window.quillEditor.getSelection();
            // Create a more robust video element
            const videoHtml = `<video controls style="max-width: 100%; height: auto;">
                <source src="${e.target.result}" type="${file.type}">
                Your browser does not support the video tag.
            </video>`;

            window.quillEditor.clipboard.dangerouslyPasteHTML(
                range ? range.index : 0,
                videoHtml
            );
            showMediaPreview("Video", file.name);
        };
        reader.readAsDataURL(file);
    }
}

// Remove legacy Quill video handler usage (kept commented/removed)
// legacy code that used prompt/dangerously insert video has been removed to avoid Quill video issues

const mediaBtn = document.querySelector(".media-video-btn");
const videoButtons = document.querySelector(".video-buttons");
mediaBtn.onclick = () => {
    videoButtons.style.display = "flex";
};

const closeButton = document.querySelector(".close-btn");
if (closeButton && videoButtons) {
    closeButton.onclick = () => {
        videoButtons.style.display = "none";
    };
}

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
    const popup = document.querySelector(".popup");

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

    // Insert only the link wrapper into the editor. iframe will be injected on submit.
    const linkHtml = `
        <div class="youtube-link-wrapper" data-video-id="${videoId}" contenteditable="false" style="margin:1rem 0; text-align:center;">
            <p style="margin:0.25rem 0; font-size:0.95em; color:#666;">
                📺 <a href="https://www.youtube.com/watch?v=${videoId}" target="_blank" rel="noopener noreferrer">View on YouTube</a>
            </p>
        </div>
    `;
    const ta = document.getElementById("id_text");
    if (ta) ta.value += linkHtml;

    showMediaPreview("YouTube Link", `Video ID: ${videoId}`);

    // Clear and hide the form
    const input = document.getElementById("youtube-url");
    if (input) input.value = "";
    const youtubeForm = document.querySelector(".youtube-form");
    if (youtubeForm) youtubeForm.style.display = "none";
    const popup = document.querySelector(".popup");
    if (popup) {
        popup.style.display = "none";
        videoButtons.style.display = "none";
    }

    console.log(
        `✅ YouTube link inserted (video id ${videoId}). Iframe will be added on save.`
    );
    if (ta) {
        ta.value = injectYouTubeIframes(ta.value, videoId);
        console.log("Text area", ta)
    }
}

// -- New helper: inject iframe tags into HTML payload before submit --
function injectYouTubeIframes(html, vid) {
    // Use DOMParser to safely manipulate HTML string
    try {
        html += `
            <div class="youtube-video-container ql-editor" contenteditable="true" style="position: relative; margin: 1.5rem 0; padding-bottom: 56.25%; height: 0; overflow: hidden; background-color: #000; border-radius: 8px;"><iframe width="560" height="315" src="https://www.youtube.com/embed/${vid}" title="YouTube video player" style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe></div>
        `;
        console.log("Processed HTML:", html);
        return html;
    } catch (err) {
        console.error("injectYouTubeIframes error:", err);
        return html; // fallback: return original html
    }
}

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

// Helper function to show media previews
function showMediaPreview(type, filename) {
    const preview = document.getElementById("media-preview");
    preview.style.display = "flex";

    const item = document.createElement("div");
    item.className = "preview-item";
    item.innerHTML = `
        <span><strong>${type}:</strong> ${filename}</span>
        <button type="button" class="remove-btn" onclick="this.parentElement.remove()">Remove</button>
    `;

    preview.appendChild(item);
}
