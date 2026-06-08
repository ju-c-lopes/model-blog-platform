(function () {
    function findPasswordInput(field) {
        if (!field) {
            return null;
        }
        return field.querySelector(
            'input[type="password"], input.input-type-pass, input[name="password"]'
        );
    }

    function setToggleIcon(button, visible) {
        const img = button.querySelector("img");
        if (!img) {
            return;
        }
        const showSrc = button.dataset.viewIcon;
        const hideSrc = button.dataset.hideIcon;
        if (showSrc && hideSrc) {
            img.src = visible ? showSrc : hideSrc;
            img.alt = visible ? "Ocultar senha" : "Mostrar senha";
        }
    }

    document.querySelectorAll(".show-hide-btn").forEach((button) => {
        const field = button.closest(".form-field");
        const input = findPasswordInput(field);
        if (!input) {
            return;
        }

        if (!button.dataset.hideIcon) {
            const img = button.querySelector("img");
            if (img) {
                button.dataset.hideIcon = img.getAttribute("src") || "";
                button.dataset.viewIcon = img.getAttribute("src") || "";
            }
        }

        const toggle = () => {
            const isPassword = input.getAttribute("type") === "password";
            input.setAttribute("type", isPassword ? "text" : "password");
            setToggleIcon(button, isPassword);
        };

        button.addEventListener("click", toggle);
    });
})();
