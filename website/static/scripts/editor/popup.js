function openPopup(popupSelector) {
    const popup = document.querySelector(popupSelector);
    if (!popup) return;

    popup.style.display = "flex";
    document.body.classList.add("popup-open");
}

function closePopup(popupSelector) {
    const popup = document.querySelector(popupSelector);
    if (!popup) return;

    popup.style.display = "none";
    document.body.classList.remove("popup-open");
}

function bindPopup(triggerSelector, popupSelector, closeSelector) {
    const trigger = document.querySelector(triggerSelector);
    const popupWrapper = document.querySelector(popupSelector);
    const popupBox = popupWrapper ? popupWrapper.querySelector(".popup") : null;
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

    if (popupWrapper && popupBox) {
        popupWrapper.addEventListener("click", (event) => {
            if (!popupBox.contains(event.target)) {
                closePopup(popupSelector);
            }
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