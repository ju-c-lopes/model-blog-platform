(function () {
    var root = document.getElementById("viewport-debug");
    if (!root) {
        return;
    }

    var panel = root.querySelector(".viewport-debug__panel");
    var toggle = root.querySelector(".viewport-debug__toggle");
    var closeButton = root.querySelector(".viewport-debug__close");
    var content = root.querySelector(".viewport-debug__content");

    if (!panel || !toggle || !content) {
        return;
    }

    function renderMetrics() {
        content.innerHTML =
            "<p><strong>Largura:</strong> " +
            window.innerWidth +
            "px</p>" +
            "<p><strong>Altura:</strong> " +
            window.innerHeight +
            "px</p>" +
            "<p><strong>Device Pixel Ratio:</strong> " +
            window.devicePixelRatio +
            "</p>" +
            '<p class="viewport-debug__ua"><strong>User Agent:</strong> ' +
            navigator.userAgent +
            "</p>";
    }

    function setOpen(isOpen) {
        root.classList.toggle("is-open", isOpen);
        panel.hidden = !isOpen;
        toggle.setAttribute("aria-expanded", isOpen ? "true" : "false");
        if (isOpen) {
            renderMetrics();
        }
    }

    toggle.addEventListener("click", function () {
        setOpen(!root.classList.contains("is-open"));
    });

    if (closeButton) {
        closeButton.addEventListener("click", function () {
            setOpen(false);
        });
    }

    window.addEventListener("resize", function () {
        if (root.classList.contains("is-open")) {
            renderMetrics();
        }
    });

    document.addEventListener("keydown", function (event) {
        if (event.key === "Escape" && root.classList.contains("is-open")) {
            setOpen(false);
        }
    });
})();
