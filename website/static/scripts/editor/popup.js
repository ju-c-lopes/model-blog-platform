// const mediaBtn = document.querySelector(".media-video-btn");
// const videoButtons = document.querySelector(".video-buttons");
// mediaBtn.onclick = () => {
//     videoButtons.style.display = "flex";
// };

// const closeButton = document.querySelector(".close-btn");
// if (closeButton && videoButtons) {
//     closeButton.onclick = () => {
//         videoButtons.style.display = "none";
//     };
// }

function openPopup(popupSelector) {
    const popup = document.querySelector(popupSelector);
    if (!popup) return;

    popup.style.display = "flex";
}

function closePopup(popupSelector) {
    const popup = document.querySelector(popupSelector);
    if (!popup) return;

    popup.style.display = "none";
}

function bindPopup(triggerSelector, popupSelector, closeSelector) {
    const trigger = document.querySelector(triggerSelector);
    const closeBtn = document.querySelector(closeSelector);

    if (trigger) {
        trigger.addEventListener("click", () => {
            openPopup(popupSelector);
        });
    }

    if (closeBtn) {
        closeBtn.addEventListener("click", () => {
            closePopup(popupSelector);
        });
    }
}

function initPopup() {
    bindPopup(".media-video-btn", ".video-buttons", ".video-buttons .close-btn");
    bindPopup(".table-btn", ".table-buttons", ".table-buttons .close-btn");
}

/* TECH-COMMITMENT:
    Close popup logic is currently exposed globally (window.closePopup)
    to simplify modular refactor phase, due its use for content successful
    insertion flow that must close the popup immediately.

    Future improvement:
    - Replace with ES module import/export
    Encapsulate popup lifecycle inside component
    - Add overlay click + ESC support

    Reason:
    Avoid overengineering during refactoring and initial JS modularization.

    Created: 2026-03
*/

window.initPopup = initPopup;
window.closePopup = closePopup;