const btn = document.querySelector(".button-menu-mobile");
const menuNavigation = document.querySelector(".menu-navigation");

btn.onclick = function() {
    btn.classList.toggle('active');
    menuNavigation.classList.contains("menu-visible") ? menuNavigation.classList.remove("menu-visible") : menuNavigation.classList.add("menu-visible");
    if (!menuNavigation.classList.contains("menu-visible")) {
        menuNavigation.style.top = "0";
        menuNavigation.style.transform = "translateY(calc(-250px - 4em - 15px))";
        menuNavigation.style.transition = "0.3s ease-out";
    } else {
        menuNavigation.style.top = "-250px";
        menuNavigation.style.transform = "";
        menuNavigation.style.transition = "";
    }
};