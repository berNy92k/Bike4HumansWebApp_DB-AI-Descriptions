document.addEventListener("DOMContentLoaded", () => {
    const aiButton = document.getElementById("ai-generate-description-btn");
    const description = document.getElementById("description");

    if (!aiButton || !description) return;

    aiButton.addEventListener("click", async () => {
        aiButton.disabled = true;
        const originalText = aiButton.textContent;
        aiButton.textContent = "Generuję...";

        try {
            const token = window.getCookieValue?.("access_token");
            if (!token) {
                alert("Brak tokenu logowania.");
                return;
            }

            const payload = {
                name: document.getElementById("name")?.value?.trim() || "",
                brand_id: document.getElementById("brand_id")?.value || "",
                bike_type: document.getElementById("bike_type")?.value?.trim() || "",
                frame_material: document.getElementById("frame_material")?.value?.trim() || "",
                frame_size: document.getElementById("frame_size")?.value?.trim() || "",
                wheel_size: document.getElementById("wheel_size")?.value?.trim() || "",
                tire_width: document.getElementById("tire_width")?.value?.trim() || "",
                gear_count: document.getElementById("gear_count")?.value || "",
                brake_type: document.getElementById("brake_type")?.value?.trim() || "",
                suspension_type: document.getElementById("suspension_type")?.value?.trim() || "",
                color: document.getElementById("color")?.value?.trim() || "",
                usage: document.getElementById("usage")?.value?.trim() || "",
                target_user: document.getElementById("target_user")?.value?.trim() || "",
            };

            const response = await fetch("/admin/bikes/ai-generate-description", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": `Bearer ${token}`,
                },
                credentials: "include",
                body: JSON.stringify(payload),
            });

            if (!response.ok) {
                throw new Error("Nie udało się wygenerować opisu.");
            }

            const data = await response.json();
            description.value = data.description ?? "";
        } catch (error) {
            alert(error.message || "Wystąpił błąd podczas generowania opisu.");
        } finally {
            aiButton.disabled = false;
            aiButton.textContent = originalText;
        }
    });
});
document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("bike-create-form");
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

    form.addEventListener("submit", async (event) => {
        event.preventDefault();

        const token = window.getCookieValue?.("access_token");
        if (!token) {
            window.location.href = "/auth/login";
            return;
        }

        const payload = {
            name: document.getElementById("name").value.trim(),
            description: toNullableString(document.getElementById("description").value),
            price: Number(document.getElementById("price").value),
            stock_quantity: Number(document.getElementById("stock_quantity").value || 0),
            is_active: document.getElementById("is_active").checked,
            brand_id: Number(document.getElementById("brand_id").value)
        };

        if (!payload.name) {
            showMessage("Uzupełnij nazwę.", "error");
            return;
        }

        if (!Number.isFinite(payload.price) || payload.price <= 0) {
            showMessage("Cena musi być większa od 0.", "error");
            return;
        }

        if (!Number.isInteger(payload.stock_quantity) || payload.stock_quantity < 0) {
            showMessage("Stan magazynowy musi być liczbą całkowitą >= 0.", "error");
            return;
        }

        if (!payload.brand_id || !Number.isInteger(payload.brand_id) || payload.brand_id <= 0) {
            showMessage("Wybierz producenta.", "error");
            return;
        }

        try {
            showMessage("Zapisywanie roweru...", "info");

            const response = await fetch("/admin/bikes/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": `Bearer ${token}`
                },
                body: JSON.stringify(payload)
            });

            if (!response.ok) {
                const errorText = await response.text();
                showMessage(`Nie udało się zapisać roweru. ${errorText}`, "error");
                return;
            }

            window.location.href = "/admin/bikes/list";
        } catch (error) {
            showMessage("Wystąpił błąd sieci podczas zapisu roweru.", "error");
        }
    });
});
