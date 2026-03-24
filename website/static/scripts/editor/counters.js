// Character counters
function updateCharCounter(inputId, counterId, maxLength) {
    const input = document.getElementById(inputId);
    const counter = document.getElementById(counterId);

    if (!input || !counter) return;

    function updateCounter() {
        const currentLength = input.value.length;
        counter.textContent = `${currentLength}/${maxLength}`;

        // Update counter color based on usage
        counter.classList.remove("warning", "danger");
        if (currentLength > maxLength * 0.8) {
            counter.classList.add("warning");
        }
        if (currentLength > maxLength * 0.95) {
            counter.classList.add("danger");
        }
    }

    input.addEventListener("input", updateCounter);
    updateCounter(); // Initial count
}

function initCounters() {
    updateCharCounter("id_title", "title-counter", 60);
    updateCharCounter("id_meta_description", "meta-counter", 160);
}

window.initCounters = initCounters;
