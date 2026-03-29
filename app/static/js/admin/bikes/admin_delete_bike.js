document.addEventListener("DOMContentLoaded", () => {
  const deleteButtons = document.querySelectorAll("[data-bike-id]");

  deleteButtons.forEach((button) => {
    button.addEventListener("click", async (event) => {
            event.preventDefault();

            const bikeId = button.dataset.bikeId;
            const shouldDelete = confirm("Na pewno usunąć ten rower?");
            if (!shouldDelete) {
                return;
            }

            const token = window.getCookieValue?.("access_token");
            if (!token) {
                window.location.href = "/auth/login";
                return;
            }

            try {
                const response = await fetch(`/admin/bikes/${bikeId}`, {
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

                alert("Nie udało się usunąć roweru.");
            } catch (error) {
                alert("Wystąpił błąd podczas usuwania roweru.");
            }
        });
    });
});
