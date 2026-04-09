document.addEventListener("DOMContentLoaded", () => {
    const searchInput = document.querySelector("[data-user-search]");
    const rows = Array.from(document.querySelectorAll("[data-user-row]"));
    if (!searchInput || !rows.length) {
        return;
    }

    const applyFilter = () => {
        const query = searchInput.value.trim().toLowerCase();
        rows.forEach((row) => {
            const login = row.dataset.login || "";
            const isMatch = query === "" || login.includes(query);
            row.hidden = !isMatch;
        });
    };

    searchInput.addEventListener("input", applyFilter);
});
