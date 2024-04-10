const btn = document.querySelector(".button-menu-mobile");
const menuNavigation = document.querySelector(".menu-navigation");

const closeMenu = () => {
    menuNavigation.style.top = "0";
    menuNavigation.style.transform = "translateY(calc(-250px - 4em - 15px))";
    menuNavigation.style.transition = "0.3s ease-out";
};

const openMenu = () => {
    menuNavigation.style.top = "-250px";
    menuNavigation.style.transform = "";
    menuNavigation.style.transition = "";
}

function clickButton() {
    console.log("aqui")
    btn.classList.toggle("active");
    menuNavigation.classList.toggle("menu-visible");
    menuNavigation.classList.contains("menu-visible") ? openMenu() : closeMenu();
};

btn.onclick = clickButton;

menuNavigation.addEventListener('touchstart' || 'click' || 'scroll', (e) => {
    e.stopPropagation();
})

window.addEventListener('touchstart' || 'click' || 'scroll', (e) => {
    if ((e.target !== menuNavigation) && menuNavigation.classList.contains("menu-visible")) {
        if (e.target === btn) {
            return;
        } else {
            childElements = menuNavigation.children;
            for (let child of childElements) {
                () => {
                    if (e.target !== child) {
                        child.style.display = 'none';
                    }
                }
            }
            btn.classList.remove("active");
            menuNavigation.classList.remove("menu-visible");
            closeMenu();
        }
    }
})