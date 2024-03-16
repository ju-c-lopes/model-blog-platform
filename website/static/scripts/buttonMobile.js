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

btn.onclick = () => {
    btn.classList.toggle("active");
    menuNavigation.classList.toggle("menu-visible");
    menuNavigation.classList.contains("menu-visible") ? openMenu() : closeMenu();
};