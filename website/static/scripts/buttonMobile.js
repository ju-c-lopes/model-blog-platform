const btn = document.querySelector(".button-menu-mobile");
const menuNavigation = document.querySelector("#menu-nav");

btn.addEventListener("click", function() {
    //e.preventDefault();
    btn.classList.toggle('active');
    
    menuNavigation.classList.toggle('menu-visible');
});