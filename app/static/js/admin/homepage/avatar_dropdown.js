document.addEventListener("DOMContentLoaded", () => {
    const toggle = document.getElementById("avatarToggle");
    const dropdown = document.getElementById("avatarDropdown");

    if (!toggle || !dropdown) return;

    const closeDropdown = () => {
        dropdown.classList.remove("is-open");
        toggle.setAttribute("aria-expanded", "false");
        dropdown.setAttribute("aria-hidden", "true");
    };

    const openDropdown = () => {
        dropdown.classList.add("is-open");
        toggle.setAttribute("aria-expanded", "true");
        dropdown.setAttribute("aria-hidden", "false");
    };

    toggle.addEventListener("click", (event) => {
        event.stopPropagation();
        if (dropdown.classList.contains("is-open")) {
            closeDropdown();
        } else {
            openDropdown();
        }
    });

    document.addEventListener("click", (event) => {
        if (!event.target.closest(".avatar-menu")) {
            closeDropdown();
        }
    });

    document.addEventListener("keydown", (event) => {
        if (event.key === "Escape") {
            closeDropdown();
        }
    });
});
