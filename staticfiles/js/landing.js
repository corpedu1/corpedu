document.addEventListener("DOMContentLoaded", () => {
    document.body.dataset.page = "landing";
    const anchors = document.querySelectorAll('a[href^="#"]');
    anchors.forEach((anchor) => {
        anchor.addEventListener("click", (event) => {
            const targetId = anchor.getAttribute("href");
            if (!targetId || targetId === "#") {
                return;
            }
            const target = document.querySelector(targetId);
            if (target) {
                event.preventDefault();
                target.scrollIntoView({ behavior: "smooth", block: "start" });
            }
        });
    });
});
