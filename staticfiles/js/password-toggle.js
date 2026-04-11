(function () {
    function syncButtonState(button, input) {
        const revealed = input.type === "text";
        button.classList.toggle("is-revealed", revealed);
        button.setAttribute("aria-pressed", revealed ? "true" : "false");
        button.setAttribute("aria-label", revealed ? "Скрыть пароль" : "Показать пароль");
    }

    function init() {
        document.querySelectorAll(".password-field__toggle").forEach((button) => {
            const id = button.getAttribute("aria-controls");
            const input = id ? document.getElementById(id) : null;
            if (!input || !input.classList.contains("password-field__input")) {
                return;
            }
            button.addEventListener("click", () => {
                input.type = input.type === "password" ? "text" : "password";
                syncButtonState(button, input);
            });
            syncButtonState(button, input);
        });
    }

    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", init);
    } else {
        init();
    }
})();
