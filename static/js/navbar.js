document.addEventListener("DOMContentLoaded", () => {
    const toggle = document.querySelector("[data-user-menu-toggle]");
    const menu = document.querySelector("[data-user-menu]");

    function closeAllNavDropdowns() {
        document.querySelectorAll("[data-nav-dropdown]").forEach((group) => {
            const ddMenu = group.querySelector("[data-nav-dropdown-menu]");
            const ddToggle = group.querySelector("[data-nav-dropdown-toggle]");
            ddMenu?.classList.remove("is-open");
            ddToggle?.classList.remove("is-open");
            ddToggle?.setAttribute("aria-expanded", "false");
        });
    }

    function isInsideNavDropdown(target) {
        return Boolean(
            target.closest("[data-nav-dropdown-toggle]") ||
                target.closest("[data-nav-dropdown-menu]")
        );
    }

    document.querySelectorAll("[data-nav-dropdown]").forEach((group) => {
        const ddToggle = group.querySelector("[data-nav-dropdown-toggle]");
        const ddMenu = group.querySelector("[data-nav-dropdown-menu]");
        if (!ddToggle || !ddMenu) {
            return;
        }

        ddToggle.addEventListener("click", (event) => {
            event.stopPropagation();
            if (toggle && menu) {
                menu.classList.remove("is-open");
                toggle.classList.remove("is-open");
            }
            const willOpen = !ddMenu.classList.contains("is-open");
            document.querySelectorAll("[data-nav-dropdown]").forEach((other) => {
                if (other === group) {
                    return;
                }
                const m = other.querySelector("[data-nav-dropdown-menu]");
                const t = other.querySelector("[data-nav-dropdown-toggle]");
                m?.classList.remove("is-open");
                t?.classList.remove("is-open");
                t?.setAttribute("aria-expanded", "false");
            });
            ddMenu.classList.toggle("is-open", willOpen);
            ddToggle.classList.toggle("is-open", willOpen);
            ddToggle.setAttribute("aria-expanded", willOpen ? "true" : "false");
        });

        ddMenu.addEventListener("click", () => {
            ddMenu.classList.remove("is-open");
            ddToggle.classList.remove("is-open");
            ddToggle.setAttribute("aria-expanded", "false");
        });
    });

    document.addEventListener("click", (event) => {
        if (!isInsideNavDropdown(event.target)) {
            closeAllNavDropdowns();
        }

        if (!toggle || !menu) {
            return;
        }
        if (!menu.contains(event.target) && !toggle.contains(event.target)) {
            menu.classList.remove("is-open");
            toggle.classList.remove("is-open");
        }
    });

    document.addEventListener("keydown", (event) => {
        if (event.key !== "Escape") {
            return;
        }
        closeAllNavDropdowns();
        if (toggle && menu) {
            menu.classList.remove("is-open");
            toggle.classList.remove("is-open");
        }
    });

    if (!toggle || !menu) {
        return;
    }

    toggle.addEventListener("click", (event) => {
        event.stopPropagation();
        closeAllNavDropdowns();
        const isOpen = menu.classList.contains("is-open");
        menu.classList.toggle("is-open", !isOpen);
        toggle.classList.toggle("is-open", !isOpen);
    });

    menu.addEventListener("click", () => {
        menu.classList.remove("is-open");
        toggle.classList.remove("is-open");
    });
});
