document.addEventListener("DOMContentLoaded", () => {
    const deleteButtons = document.querySelectorAll(".action-delete[data-manufacturer-id]");

    deleteButtons.forEach((button) => {
        button.addEventListener("click", async (event) => {
            event.preventDefault();

            const manufacturerId = button.dataset.manufacturerId;
            const shouldDelete = confirm("Na pewno usunąć tego producenta?");
            if (!shouldDelete) {
                return;
            }

            const token = window.getCookieValue?.("access_token");
            if (!token) {
                window.location.href = "/auth/login";
                return;
            }

            try {
                const response = await fetch(`/admin/manufacturer/${manufacturerId}`, {
                    method: "DELETE",
                    headers: {
                        "Authorization": `Bearer ${token}`
                    }
                });

                if (response.ok) {
                    window.location.reload();
                    return;
                }

                if (response.status === 401 || response.status === 403) {
                    window.location.href = "/auth/login";
                    return;
                }

                alert("Nie udało się usunąć producenta.");
            } catch (error) {
                alert("Wystąpił błąd podczas usuwania producenta.");
            }
        });
    });
});