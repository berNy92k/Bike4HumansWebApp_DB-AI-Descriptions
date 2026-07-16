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

            const parseDecimal = (value) => {
                const trimmed = value?.trim();
                if (!trimmed) return null;
                const parsed = Number(trimmed.replace(",", "."));
                return Number.isFinite(parsed) ? parsed : null;
            };

            const payload = {
                name: document.getElementById("name")?.value?.trim() || "",
                description: document.getElementById("description")?.value || "",
                bike_type: document.getElementById("bike_type")?.value?.trim() || "",
                frame_material: document.getElementById("frame_material")?.value?.trim() || "",
                frame_size: document.getElementById("frame_size")?.value?.trim() || "",
                frame_size_label: document.getElementById("frame_size_label")?.value?.trim() || "",
                wheel_size: document.getElementById("wheel_size")?.value?.trim() || "",
                tire_width: parseDecimal(document.getElementById("tire_width")?.value),
                gear_count: document.getElementById("gear_count")?.value || "",
                brake_type: document.getElementById("brake_type")?.value?.trim() || "",
                suspension_type: document.getElementById("suspension_type")?.value?.trim() || "",
                color: document.getElementById("color")?.value?.trim() || "",
                weight_kg: document.getElementById("weight_kg")?.value || "",
                recommended_height_min: document.getElementById("recommended_height_min")?.value || "",
                recommended_height_max: document.getElementById("recommended_height_max")?.value || "",
                usage: document.getElementById("usage")?.value?.trim() || "",
                target_user: document.getElementById("target_user")?.value?.trim() || "",
                brand_id: document.getElementById("brand_id")?.value || "",

            };

            const response = await fetch("/admin/bikes/ai-generate-description", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": `Bearer ${token}`,
                },
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
    const form = document.getElementById("bike-edit-form");
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

    const bikeIdMatch = window.location.pathname.match(/\/admin\/bikes\/(\d+)\/edit$/);
    const bikeId = bikeIdMatch ? bikeIdMatch[1] : null;

    if (!bikeId) {
        showMessage("Nie udało się ustalić ID roweru.", "error");
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
            description: toNullableString(document.getElementById("description").value),
            price: Number(document.getElementById("price").value),
            stock_quantity: Number(document.getElementById("stock_quantity").value || 0),
            image_url: toNullableString(document.getElementById("image_url").value),
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
            showMessage("Zapisywanie zmian...", "info");

            const response = await fetch(`/admin/bikes/${bikeId}`, {
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

            window.location.href = `/admin/bikes/${bikeId}/details`;
        } catch (error) {
            showMessage("Wystąpił błąd sieci podczas zapisu zmian.", "error");
        }
    });
});