function normalizeTagSearch(value) {
    return (value || "").trim().toLocaleLowerCase("pt-BR");
}

function initTagPicker() {
    const picker = document.getElementById("tag-picker");
    if (!picker) return;

    const toggleBtn = document.getElementById("tag-picker-toggle");
    const dropdown = document.getElementById("tag-picker-dropdown");
    const searchInput = document.getElementById("tag-picker-search");
    const optionsList = document.getElementById("tag-picker-options");
    const createBtn = document.getElementById("tag-picker-create");
    const createNameEl = document.getElementById("tag-picker-create-name");
    const selectedList = document.getElementById("tag-selected-list");
    const hiddenInputs = document.getElementById("tag-hidden-inputs");

    if (!toggleBtn || !dropdown || !searchInput || !optionsList || !selectedList || !hiddenInputs) {
        return;
    }

    const options = Array.from(optionsList.querySelectorAll(".tag-picker-option"));

    function isTagSelected(tagId) {
        return Boolean(hiddenInputs.querySelector(`input[name="tags"][data-tag-id="${tagId}"]`));
    }

    function isNewTagSelected(name) {
        const normalized = normalizeTagSearch(name);
        return Array.from(hiddenInputs.querySelectorAll('input[name="new_tag_names"]')).some(
            (input) => normalizeTagSearch(input.value) === normalized
        );
    }

    function syncOptionState(option) {
        const tagId = option.dataset.tagId;
        const selected = isTagSelected(tagId);
        option.classList.toggle("is-selected", selected);
        option.hidden = selected;
        option.setAttribute("aria-disabled", selected ? "true" : "false");
    }

    function buildChip({ tagId, name, iconUrl, isNew }) {
        const chip = document.createElement("span");
        chip.className = `tag-chip${isNew ? " tag-chip--new" : ""}`;
        if (tagId) chip.dataset.tagId = tagId;
        if (isNew) chip.dataset.newName = name;

        const label = document.createElement("span");
        label.className = "tag-chip-label";

        if (iconUrl) {
            const img = document.createElement("img");
            img.src = iconUrl;
            img.alt = "";
            img.width = 18;
            img.height = 18;
            img.className = "tag-icon";
            label.appendChild(img);
        }

        const nameSpan = document.createElement("span");
        nameSpan.className = "tag-chip-name";
        nameSpan.textContent = name;
        label.appendChild(nameSpan);

        const removeBtn = document.createElement("button");
        removeBtn.type = "button";
        removeBtn.className = "tag-chip-remove";
        removeBtn.setAttribute("aria-label", "Remover tag");
        removeBtn.innerHTML = "&times;";

        chip.appendChild(label);
        chip.appendChild(removeBtn);
        return chip;
    }

    function addExistingTag(option) {
        const tagId = option.dataset.tagId;
        const name = option.dataset.tagName;
        const iconUrl = option.dataset.iconUrl || "";

        if (!tagId || isTagSelected(tagId)) return;

        selectedList.appendChild(
            buildChip({
                tagId,
                name,
                iconUrl,
                isNew: false,
            })
        );

        const input = document.createElement("input");
        input.type = "hidden";
        input.name = "tags";
        input.value = tagId;
        input.dataset.tagId = tagId;
        hiddenInputs.appendChild(input);

        syncOptionState(option);
    }

    function addNewTag(name) {
        const trimmed = name.trim();
        if (!trimmed || isNewTagSelected(trimmed)) return;

        selectedList.appendChild(
            buildChip({
                name: trimmed,
                isNew: true,
            })
        );

        const input = document.createElement("input");
        input.type = "hidden";
        input.name = "new_tag_names";
        input.value = trimmed;
        input.dataset.newName = trimmed;
        hiddenInputs.appendChild(input);
    }

    function removeTagChip(chip) {
        const tagId = chip.dataset.tagId;
        const newName = chip.dataset.newName;

        if (tagId) {
            hiddenInputs.querySelector(`input[name="tags"][data-tag-id="${tagId}"]`)?.remove();
            const option = options.find((item) => item.dataset.tagId === tagId);
            if (option) syncOptionState(option);
        } else if (newName) {
            Array.from(hiddenInputs.querySelectorAll('input[name="new_tag_names"]')).forEach((input) => {
                if (input.value === newName) {
                    input.remove();
                }
            });
        }

        chip.remove();
    }

    function filterOptions() {
        const query = normalizeTagSearch(searchInput.value);
        let visibleCount = 0;
        let exactMatch = false;

        options.forEach((option) => {
            if (option.classList.contains("is-selected")) {
                option.hidden = true;
                return;
            }

            const name = normalizeTagSearch(option.dataset.tagName);
            const matches = !query || name.includes(query);
            option.hidden = !matches;
            if (matches) visibleCount += 1;
            if (query && name === query) exactMatch = true;
        });

        const canCreate = query.length > 0 && !exactMatch && !isNewTagSelected(searchInput.value.trim());
        if (createBtn && createNameEl) {
            createBtn.hidden = !canCreate;
            createNameEl.textContent = searchInput.value.trim();
        }

        return visibleCount;
    }

    function openDropdown() {
        dropdown.hidden = false;
        toggleBtn.setAttribute("aria-expanded", "true");
        searchInput.value = "";
        filterOptions();
        searchInput.focus();
    }

    function closeDropdown() {
        dropdown.hidden = true;
        toggleBtn.setAttribute("aria-expanded", "false");
        searchInput.value = "";
        if (createBtn) createBtn.hidden = true;
        options.forEach((option) => {
            if (!option.classList.contains("is-selected")) {
                option.hidden = false;
            }
        });
    }

    toggleBtn.addEventListener("click", () => {
        if (dropdown.hidden) {
            openDropdown();
        } else {
            closeDropdown();
        }
    });

    searchInput.addEventListener("input", filterOptions);

    searchInput.addEventListener("keydown", (event) => {
        if (event.key === "Escape") {
            closeDropdown();
            toggleBtn.focus();
            return;
        }

        if (event.key === "Enter") {
            event.preventDefault();
            const query = searchInput.value.trim();
            const visibleOptions = options.filter((option) => !option.hidden && !option.classList.contains("is-selected"));

            if (visibleOptions.length === 1) {
                addExistingTag(visibleOptions[0]);
                closeDropdown();
                return;
            }

            if (createBtn && !createBtn.hidden && query) {
                addNewTag(query);
                closeDropdown();
            }
        }
    });

    optionsList.addEventListener("click", (event) => {
        const option = event.target.closest(".tag-picker-option");
        if (!option || option.classList.contains("is-selected") || option.hidden) return;
        addExistingTag(option);
        closeDropdown();
    });

    createBtn?.addEventListener("click", () => {
        addNewTag(searchInput.value);
        closeDropdown();
    });

    selectedList.addEventListener("click", (event) => {
        const removeBtn = event.target.closest(".tag-chip-remove");
        if (!removeBtn) return;
        const chip = removeBtn.closest(".tag-chip");
        if (chip) removeTagChip(chip);
    });

    document.addEventListener("click", (event) => {
        if (!picker.contains(event.target)) {
            closeDropdown();
        }
    });

    options.forEach(syncOptionState);
}

window.initTagPicker = initTagPicker;
