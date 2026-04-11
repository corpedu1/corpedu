document.addEventListener("DOMContentLoaded", () => {
    const items = document.querySelectorAll(".faq-item");

    items.forEach((item) => {
        const button = item.querySelector(".faq-question");
        if (!button) {
            return;
        }

        button.addEventListener("click", () => {
            const isOpen = item.classList.contains("is-open");
            item.classList.toggle("is-open", !isOpen);
            button.setAttribute("aria-expanded", String(!isOpen));
        });
    });
});
