document.addEventListener("DOMContentLoaded", () => {
    const form = document.querySelector(".auth-form");
    if (!form) return;

    form.addEventListener("submit", async (event) => {
        event.preventDefault();

        const formData = new FormData(form);
        const payload = {
            username: formData.get("username"),
            email: formData.get("email"),
            name: formData.get("name"),
            surname: formData.get("surname"),
            password: formData.get("password"),
            confirm_password: formData.get("confirm_password")
        };

        if (payload.password !== payload.confirm_password) {
            alert("Hasła nie są takie same");
            return;
        }

        try {
            const response = await fetch("/auth/user", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(payload)
            });

            if (response.ok) {
                window.location.href = "/auth/login";
                return;
            }

            const errorData = await response.json();
            console.error("Błąd rejestracji:", errorData);
            alert("Nie udało się zarejestrować użytkownika");
        } catch (error) {
            console.error("Błąd sieci:", error);
            alert("Błąd połączenia z serwerem");
        }
    });
});
