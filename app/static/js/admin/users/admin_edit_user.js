document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("user-edit-form");
    const messageBox = document.getElementById("form-message");

    if (!form || !messageBox) {
        return;
    }

    const showMessage = (text, type = "info") => {
        messageBox.textContent = text;
        messageBox.className = `form-message form-message-${type}`;
        messageBox.style.display = text ? "block" : "none";
    };

    const toBoolean = (value) => value === "true";

    const userIdMatch = window.location.pathname.match(/\/admin\/user\/(\d+)\/edit$/);
    const userId = userIdMatch ? userIdMatch[1] : null;

    if (!userId) {
        showMessage("Nie udało się odczytać ID użytkownika.", "error");
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
            username: document.getElementById("username").value.trim(),
            email: document.getElementById("email").value.trim(),
            name: document.getElementById("name").value.trim(),
            surname: document.getElementById("surname").value.trim(),
            role_id: Number(document.getElementById("role_id").value),
            is_active: toBoolean(document.getElementById("is_active").value),
            email_verified: toBoolean(document.getElementById("email_verified").value),
        };

        if (!payload.username || !payload.email || !payload.name || !payload.surname) {
            showMessage("Uzupełnij wszystkie wymagane pola.", "error");
            return;
        }

        if (!Number.isInteger(payload.role_id) || payload.role_id <= 0) {
            showMessage("Wybierz poprawną rolę użytkownika.", "error");
            return;
        }

        try {
            showMessage("Zapisywanie zmian...", "info");

            const response = await fetch(`/admin/user/${userId}`, {
                method: "PUT",
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

            window.location.href = `/admin/user/${userId}/details`;
        } catch (error) {
            showMessage("Wystąpił błąd sieci podczas zapisu zmian.", "error");
        }
    });
});
