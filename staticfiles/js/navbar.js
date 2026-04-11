document.addEventListener("DOMContentLoaded", () => {
    const toggle = document.querySelector("[data-user-menu-toggle]");
    const menu = document.querySelector("[data-user-menu]");
    if (!toggle || !menu) {
        return;
    }

    toggle.addEventListener("click", (event) => {
        event.stopPropagation();
        const isOpen = menu.classList.contains("is-open");
        menu.classList.toggle("is-open", !isOpen);
        toggle.classList.toggle("is-open", !isOpen);
    });

    document.addEventListener("click", (event) => {
        if (!menu.contains(event.target) && !toggle.contains(event.target)) {
            menu.classList.remove("is-open");
            toggle.classList.remove("is-open");
        }
    });

    menu.addEventListener("click", () => {
        menu.classList.remove("is-open");
        toggle.classList.remove("is-open");
    });
});
