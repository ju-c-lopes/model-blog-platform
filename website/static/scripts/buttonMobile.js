const btn = document.querySelector(".button-menu-mobile");
const menuNavigation = document.querySelector(".menu-navigation");

// Initialize menu in closed position on page load
const initializeMenu = () => {
    menuNavigation.style.top = "0";
    menuNavigation.style.transform = "translateY(calc(-800px - 4em - 15px))";
    menuNavigation.style.transition = "0.3s ease-out";
    // Ensure body scroll is enabled on initialization
    document.body.style.overflowY = "scroll";
};

const closeMenu = () => {
    menuNavigation.style.top = "0";
    menuNavigation.style.transform = "translateY(calc(-800px - 4em - 15px))";
    menuNavigation.style.transition = "0.3s ease-out";
    // Re-enable body scroll when menu is closed
    document.body.style.overflowY = "scroll";
    // Reset menu scroll position
    menuNavigation.scrollTop = 0;
};

const openMenu = () => {
    menuNavigation.style.top = "-360px";
    menuNavigation.style.transform = "";
    menuNavigation.style.transition = "";
    // Disable body scroll when menu is open
    document.body.style.overflowY = "hidden";
    // Ensure menu can scroll
    menuNavigation.style.overflowY = "auto";
};

function clickButton() {
    // Check current state BEFORE toggling
    const isCurrentlyVisible =
        menuNavigation.classList.contains("menu-visible");

    // Toggle classes
    btn.classList.toggle("active");
    menuNavigation.classList.toggle("menu-visible");

    // Apply correct behavior based on NEW state (opposite of current)
    if (isCurrentlyVisible) {
        // Menu was visible, now closing
        closeMenu();
    } else {
        // Menu was hidden, now opening
        openMenu();
    }
}

// Initialize menu position on page load
initializeMenu();

btn.onclick = clickButton;

menuNavigation.addEventListener("touchstart", (e) => {
    e.stopPropagation();
});

menuNavigation.addEventListener("click", (e) => {
    e.stopPropagation();
});

window.addEventListener("touchstart", (e) => {
    if (
        e.target !== menuNavigation &&
        menuNavigation.classList.contains("menu-visible")
    ) {
        if (e.target === btn) {
            return;
        } else {
            const childElements = menuNavigation.children;
            let isChildElement = false;

            // Check if clicked element is a child of menu
            for (let child of childElements) {
                if (child.contains(e.target)) {
                    isChildElement = true;
                    break;
                }
            }

            if (!isChildElement) {
                btn.classList.remove("active");
                menuNavigation.classList.remove("menu-visible");
                closeMenu();
            }
        }
    }
});

window.addEventListener("click", (e) => {
    if (
        e.target !== menuNavigation &&
        menuNavigation.classList.contains("menu-visible")
    ) {
        if (e.target === btn) {
            return;
        } else {
            const childElements = menuNavigation.children;
            let isChildElement = false;

            // Check if clicked element is a child of menu
            for (let child of childElements) {
                if (child.contains(e.target)) {
                    isChildElement = true;
                    break;
                }
            }

            if (!isChildElement) {
                btn.classList.remove("active");
                menuNavigation.classList.remove("menu-visible");
                closeMenu();
            }
        }
    }
});
