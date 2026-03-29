document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("role-edit-form");
    const messageBox = document.getElementById("form-message");

    if (!form || !messageBox) {
        return;
    }

    const showMessage = (text, type = "info") => {
        messageBox.textContent = text;
        messageBox.className = `form-message form-message-${type}`;
        messageBox.style.display = text ? "block" : "none";
    };

    const toNullableString = (value) => {
        const trimmed = value.trim();
        return trimmed === "" ? null : trimmed;
    };

    const roleIdMatch = window.location.pathname.match(/\/admin\/user\/role\/(\d+)\/edit$/);
    const roleId = roleIdMatch ? roleIdMatch[1] : null;

    if (!roleId) {
        showMessage("Nie udało się ustalić ID roli.", "error");
        return;
    }

    form.addEventListener("submit", async (event) => {
        event.preventDefault();

        const token = window.getCookieValue?.("access_token");
        if (!token) {
            window.location.href = "/auth/login";
            return;
        }

        const payload = {
            name: document.getElementById("name").value.trim(),
            description: toNullableString(document.getElementById("description").value)
        };

        if (!payload.name) {
            showMessage("Uzupełnij nazwę roli.", "error");
            return;
        }

        try {
            showMessage("Zapisywanie zmian...", "info");

            const response = await fetch(`/admin/user/role/${roleId}`, {
                method: "PATCH",
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": `Bearer ${token}`
                },
                body: JSON.stringify(payload)
            });

            if (!response.ok) {
                const errorText = await response.text();
                showMessage(`Nie udało się zapisać zmian. ${errorText}`, "error");
                return;
            }

            window.location.href = `/admin/user/role/${roleId}`;
        } catch (error) {
            showMessage("Wystąpił błąd sieci podczas zapisu zmian.", "error");
        }
    });
});