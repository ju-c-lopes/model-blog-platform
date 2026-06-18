(function () {
    var sections = document.querySelectorAll(".html-sitemap__section");
    if (!sections.length) {
        return;
    }

    document.querySelectorAll(".html-sitemap__toggle-all").forEach(function (button) {
        button.addEventListener("click", function () {
            var expand = button.getAttribute("data-action") === "expand";
            sections.forEach(function (section) {
                section.open = expand;
            });
        });
    });
})();
