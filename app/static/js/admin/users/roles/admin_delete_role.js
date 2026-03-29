document.addEventListener("DOMContentLoaded", () => {
    const deleteButtons = document.querySelectorAll("[data-role-id]");

    deleteButtons.forEach((button) => {
        button.addEventListener("click", async (event) => {
            event.preventDefault();

            const roleId = button.dataset.roleId;
            const shouldDelete = confirm("Na pewno usunąć tę rolę?");
            if (!shouldDelete) {
                return;
            }

            const token = window.getCookieValue?.("access_token");
            if (!token) {
                window.location.href = "/auth/login";
                return;
            }

            try {
                const response = await fetch(`/admin/user/role/${roleId}`, {
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

                alert("Nie udało się usunąć roli.");
            } catch (error) {
                alert("Wystąpił błąd podczas usuwania roli.");
            }
        });
    });
});
