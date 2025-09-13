(function () {
    document.addEventListener("DOMContentLoaded", function () {
        const container = document.querySelector(".reaction-section");
        if (!container) return;

        const likeBtn = document.getElementById("like-btn");
        const loveBtn = document.getElementById("love-btn");
        const likeIcon = document.getElementById("like-icon");
        const loveIcon = document.getElementById("love-icon");
        const likesCountEl = document.getElementById("likes-count");
        const lovesCountEl = document.getElementById("loves-count");

        const likeUrl = container.dataset.likeUrl;
        const loveUrl = container.dataset.loveUrl;
        const imgActivateLike = container.dataset.imgActivateLike;
        const imgDeactivateLike = container.dataset.imgDeactivateLike;
        const imgActivateLove = container.dataset.imgActivateLove;
        const imgDeactivateLove = container.dataset.imgDeactivateLove;

        // CSRF token from hidden form rendered in the page
        const csrftokenEl = document.querySelector(
            "[name=csrfmiddlewaretoken]"
        );
        const csrftoken = csrftokenEl ? csrftokenEl.value : null;

        function postToggle(path, onDone) {
            fetch(path, {
                method: "POST",
                headers: {
                    "X-CSRFToken": csrftoken,
                    Accept: "application/json",
                },
            })
                .then((r) => {
                    if (!r.ok) throw r;
                    return r.json();
                })
                .then(onDone)
                .catch((err) => {
                    console.log("Error occurred while toggling reaction");
                    if (err.status === 403) {
                        const modal = document.getElementById("signup-modal");
                        if (modal) modal.style.display = "flex";
                    } else {
                        console.error(err);
                    }
                });
        }

        if (likeBtn) {
            likeBtn.addEventListener("click", function () {
                postToggle(likeUrl, function (data) {
                    likesCountEl.textContent = data.likes_count;
                    lovesCountEl.textContent = data.loves_count;
                    if (data.liked) {
                        likeIcon.classList.add("active");
                        likeIcon.innerHTML =
                            "<img width='40' src='" +
                            imgActivateLike +
                            "' alt='' class='like-btn'>";
                    } else {
                        likeIcon.classList.remove("active");
                        likeIcon.innerHTML =
                            "<img width='40' src='" +
                            imgDeactivateLike +
                            "' alt='' class='like-btn'>";
                    }
                    if (data.loved) {
                        loveIcon.classList.add("active");
                        loveIcon.innerHTML =
                            "<img width='40' src='" +
                            imgActivateLove +
                            "' alt='' class='love-btn'>";
                    } else {
                        loveIcon.classList.remove("active");
                        loveIcon.innerHTML =
                            "<img width='40' src='" +
                            imgDeactivateLove +
                            "' alt='' class='love-btn'>";
                    }
                });
            });
        }

        if (loveBtn) {
            loveBtn.addEventListener("click", function () {
                postToggle(loveUrl, function (data) {
                    lovesCountEl.textContent = data.loves_count;
                    likesCountEl.textContent = data.likes_count;
                    if (data.loved) {
                        loveIcon.classList.add("active");
                        loveIcon.innerHTML =
                            "<img width='40' src='" +
                            imgActivateLove +
                            "' alt='' class='love-btn'>";
                    } else {
                        loveIcon.classList.remove("active");
                        loveIcon.innerHTML =
                            "<img width='40' src='" +
                            imgDeactivateLove +
                            "' alt='' class='love-btn'>";
                    }
                    if (data.liked) {
                        likeIcon.classList.add("active");
                        likeIcon.innerHTML =
                            "<img width='40' src='" +
                            imgActivateLike +
                            "' alt='' class='like-btn'>";
                    } else {
                        likeIcon.classList.remove("active");
                        likeIcon.innerHTML =
                            "<img width='40' src='" +
                            imgDeactivateLike +
                            "' alt='' class='like-btn'>";
                    }
                });
            });
        }

        // signup modal close handler
        document
            .getElementById("close-signup-modal")
            ?.addEventListener("click", function () {
                const modal = document.getElementById("signup-modal");
                if (modal) modal.style.display = "none";
            });
    });
})();
