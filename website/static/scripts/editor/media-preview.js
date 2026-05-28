// Helper function to show media previews
function showMediaPreview(type, filename) {
    const preview = document.getElementById("media-preview");
    if (!preview) return;
    preview.style.display = "flex";

    const item = document.createElement("div");
    item.className = "preview-item";
    const text = document.createElement("span");
    text.innerHTML = `<strong>${type}:</strong> ${filename}`;

    const button = document.createElement("button");
    button.type = "button";
    button.className = "remove-btn";
    button.textContent = "Remove";

    button.addEventListener("click", () => item.remove());

    item.appendChild(text);
    item.appendChild(button);

    preview.appendChild(item);
}

window.showMediaPreview = showMediaPreview;
