/**
 * Edit Post Page JavaScript
 * Handles rich text editor, character counters, media uploads, and form validation
 * Works for both creating new posts and editing existing posts
 */

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
                    ["link", "image", "video"],
                    ["clean"],
                ],
                handlers: {
                    video: function () {
                        insertVideoHandler();
                    },
                },
            },
            placeholder: "Start writing your amazing content here...",
        });

        // Set initial content if editing
        const initialContent = document.getElementById("id_text").value;
        if (initialContent) {
            quill.root.innerHTML = initialContent;
        }

        // Update hidden textarea when content changes
        quill.on("text-change", function () {
            document.getElementById("id_text").value = quill.root.innerHTML;
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

// Custom video handler for YouTube and other video URLs
function insertVideoHandler() {
    if (!window.quillEditor) return;

    const url = prompt(
        "Enter video URL (YouTube, Vimeo, or direct video URL):"
    );
    if (!url) return;

    let embedUrl = url;
    let videoHtml = "";

    // Handle YouTube URLs
    if (url.includes("youtube.com/watch?v=") || url.includes("youtu.be/")) {
        const videoId = extractYouTubeId(url);
        if (videoId) {
            embedUrl = `https://www.youtube.com/embed/${videoId}`;
            videoHtml = `<div class="video-responsive">
                <iframe src="${embedUrl}" frameborder="0" allowfullscreen 
                    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"></iframe>
            </div>`;
        }
    }
    // Handle Vimeo URLs
    else if (url.includes("vimeo.com/")) {
        const videoId = url.split("/").pop();
        embedUrl = `https://player.vimeo.com/video/${videoId}`;
        videoHtml = `<div class="video-responsive">
            <iframe src="${embedUrl}" frameborder="0" allowfullscreen 
                allow="autoplay; fullscreen; picture-in-picture"></iframe>
        </div>`;
    }
    // Handle direct video URLs or already embedded URLs
    else if (
        url.includes("youtube.com/embed/") ||
        url.includes("player.vimeo.com/video/")
    ) {
        videoHtml = `<div class="video-responsive">
            <iframe src="${url}" frameborder="0" allowfullscreen></iframe>
        </div>`;
    }
    // Handle direct video file URLs
    else if (url.match(/\.(mp4|webm|ogg)$/i)) {
        videoHtml = `<video controls style="max-width: 100%; height: auto;">
            <source src="${url}" type="video/${url
            .split(".")
            .pop()
            .toLowerCase()}">
            Your browser does not support the video tag.
        </video>`;
    } else {
        alert(
            "Please enter a valid video URL (YouTube, Vimeo, or direct video file URL)."
        );
        return;
    }

    const range = window.quillEditor.getSelection();
    window.quillEditor.clipboard.dangerouslyPasteHTML(
        range ? range.index : 0,
        videoHtml
    );
}

// Helper function to extract YouTube video ID
function extractYouTubeId(url) {
    const regExp =
        /^.*(youtu.be\/|v\/|u\/\w\/|embed\/|watch\?v=|&v=)([^#&?]*).*/;
    const match = url.match(regExp);
    return match && match[2].length === 11 ? match[2] : null;
}

function insertTable() {
    if (!window.quillEditor) return;

    const rows = prompt("Number of rows:", "3");
    const cols = prompt("Number of columns:", "3");

    if (rows && cols) {
        let tableHTML =
            '<table border="1" style="border-collapse: collapse; width: 100%; margin: 1rem 0;">';

        // Header row
        tableHTML += "<thead><tr>";
        for (let j = 0; j < cols; j++) {
            tableHTML +=
                '<th style="padding: 8px; background-color: #f8f9fa; border: 1px solid #dee2e6;">Header ' +
                (j + 1) +
                "</th>";
        }
        tableHTML += "</tr></thead>";

        // Body rows
        tableHTML += "<tbody>";
        for (let i = 0; i < rows - 1; i++) {
            tableHTML += "<tr>";
            for (let j = 0; j < cols; j++) {
                tableHTML +=
                    '<td style="padding: 8px; border: 1px solid #dee2e6;">Cell ' +
                    (i + 1) +
                    "," +
                    (j + 1) +
                    "</td>";
            }
            tableHTML += "</tr>";
        }
        tableHTML += "</tbody></table>";

        const range = window.quillEditor.getSelection();
        window.quillEditor.clipboard.dangerouslyPasteHTML(
            range ? range.index : 0,
            tableHTML
        );
    }
}

function insertHeading() {
    if (!window.quillEditor) return;

    const level = prompt("Heading level (1-6):", "2");
    const text = prompt("Heading text:", "Your Heading Here");

    if (level && text && level >= 1 && level <= 6) {
        const range = window.quillEditor.getSelection();
        window.quillEditor.insertText(range ? range.index : 0, text);
        window.quillEditor.formatText(
            range ? range.index : 0,
            text.length,
            "header",
            parseInt(level)
        );
    }
}

function showMediaPreview(type, filename) {
    const preview = document.getElementById("media-preview");
    preview.style.display = "block";

    const item = document.createElement("div");
    item.className = "preview-item";
    item.innerHTML = `
        <span><strong>${type}:</strong> ${filename}</span>
        <button type="button" class="remove-btn" onclick="this.parentElement.remove()">Remove</button>
    `;

    preview.appendChild(item);
}

// Form submission handler
document.querySelector("form").addEventListener("submit", function (e) {
    // Update hidden textarea with final content
    if (window.quillEditor) {
        document.getElementById("id_text").value =
            window.quillEditor.root.innerHTML;
    }

    // Basic validation
    const title = document.getElementById("id_title").value.trim();
    const content = window.quillEditor
        ? window.quillEditor.getText().trim()
        : "";

    if (!title) {
        alert("Please enter a title for your post.");
        e.preventDefault();
        return;
    }

    if (!content || content.length < 10) {
        alert(
            "Please write some content for your post (at least 10 characters)."
        );
        e.preventDefault();
        return;
    }
});
