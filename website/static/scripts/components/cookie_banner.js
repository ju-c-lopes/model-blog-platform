(function () {
    var STORAGE_KEY = "cookie_notice_dismissed";
    var banner = document.getElementById("cookie-notice-banner");
    var acceptButton = document.getElementById("cookie-notice-accept");

    if (!banner || !acceptButton) {
        return;
    }

    try {
        if (localStorage.getItem(STORAGE_KEY) === "1") {
            return;
        }
    } catch (error) {
        banner.hidden = false;
        acceptButton.addEventListener("click", dismiss);
        return;
    }

    banner.hidden = false;

    function dismiss() {
        try {
            localStorage.setItem(STORAGE_KEY, "1");
        } catch (error) {
            /* ignore */
        }
        banner.hidden = true;
    }

    acceptButton.addEventListener("click", dismiss);
})();
