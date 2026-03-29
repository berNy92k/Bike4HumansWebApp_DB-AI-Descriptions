document.addEventListener("DOMContentLoaded", () => {
    const pageSizeSelect = document.getElementById("page-size");

    if (!pageSizeSelect) {
        return;
    }

    pageSizeSelect.addEventListener("change", () => {
        const url = new URL(window.location.href);
        url.searchParams.set("page", "1");
        url.searchParams.set("size", pageSizeSelect.value);
        window.location.href = url.toString();
    });
});