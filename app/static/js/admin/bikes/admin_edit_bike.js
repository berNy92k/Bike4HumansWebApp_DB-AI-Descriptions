document.addEventListener("DOMContentLoaded", () => {
    const aiButton = document.getElementById("ai-generate-description-btn");
    const description = document.getElementById("description");
    const isAiGeneratedInput = document.getElementById("is_description_ai_generated");
    const descriptionStatusBadge = document.getElementById("description-status-badge");

    if (!aiButton || !description) return;

    const setDescriptionAiGenerated = (isAiGenerated) => {
        if (isAiGeneratedInput) isAiGeneratedInput.value = isAiGenerated ? "true" : "false";
        if (descriptionStatusBadge) {
            descriptionStatusBadge.textContent = isAiGenerated ? "AI" : "Ręcznie";
            descriptionStatusBadge.className = `badge ${isAiGenerated ? "badge-success" : "badge-danger"}`;
        }
    };

    description.addEventListener("input", () => setDescriptionAiGenerated(false));

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
            setDescriptionAiGenerated(true);
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

    const toNullableInt = (value) => {
        const trimmed = value?.trim();
        if (!trimmed) return null;
        const parsed = Number(trimmed);
        return Number.isFinite(parsed) ? parsed : null;
    };

    const toNullableDecimal = (value) => {
        const trimmed = value?.trim();
        if (!trimmed) return null;
        const parsed = Number(trimmed.replace(",", "."));
        return Number.isFinite(parsed) ? parsed : null;
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
            brand_id: Number(document.getElementById("brand_id").value),
            is_description_ai_generated: document.getElementById("is_description_ai_generated")?.value === "true",
            bike_type: toNullableString(document.getElementById("bike_type").value),
            frame_material: toNullableString(document.getElementById("frame_material").value),
            frame_size: toNullableInt(document.getElementById("frame_size").value),
            frame_size_label: toNullableString(document.getElementById("frame_size_label").value),
            wheel_size: toNullableInt(document.getElementById("wheel_size").value),
            tire_width: toNullableDecimal(document.getElementById("tire_width").value),
            gear_count: toNullableInt(document.getElementById("gear_count").value),
            brake_type: toNullableString(document.getElementById("brake_type").value),
            suspension_type: toNullableString(document.getElementById("suspension_type").value),
            color: toNullableString(document.getElementById("color").value),
            weight_kg: toNullableDecimal(document.getElementById("weight_kg").value),
            recommended_height_min: toNullableInt(document.getElementById("recommended_height_min").value),
            recommended_height_max: toNullableInt(document.getElementById("recommended_height_max").value),
            usage: toNullableString(document.getElementById("usage").value),
            target_user: toNullableString(document.getElementById("target_user").value),
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
document.addEventListener("DOMContentLoaded", () => {
    const autoTagButton = document.getElementById("ai-auto-tag-btn");

    if (!autoTagButton) return;

    const setSelectValue = (id, value) => {
        if (!value) return;
        const select = document.getElementById(id);
        if (select) select.value = value;
    };

    autoTagButton.addEventListener("click", async () => {
        autoTagButton.disabled = true;
        const originalText = autoTagButton.textContent;
        autoTagButton.textContent = "Analizuję...";

        try {
            const token = window.getCookieValue?.("access_token");
            if (!token) {
                alert("Brak tokenu logowania.");
                return;
            }

            const name = document.getElementById("name")?.value?.trim() || "";
            const description = document.getElementById("description")?.value?.trim() || "";

            if (!name) {
                alert("Uzupełnij najpierw nazwę roweru.");
                return;
            }

            if (!description) {
                alert("Uzupełnij najpierw opis roweru.");
                return;
            }

            const response = await fetch("/admin/bikes/ai-auto-tag", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": `Bearer ${token}`,
                },
                body: JSON.stringify({ name, description }),
            });

            if (!response.ok) {
                throw new Error("Nie udało się zaproponować tagów.");
            }

            const data = await response.json();
            setSelectValue("bike_type", data.bike_type);
            setSelectValue("frame_material", data.frame_material);
            setSelectValue("frame_size_label", data.frame_size_label);
            setSelectValue("brake_type", data.brake_type);
            setSelectValue("suspension_type", data.suspension_type);
            setSelectValue("color", data.color);
            setSelectValue("usage", data.usage);
            setSelectValue("target_user", data.target_user);
        } catch (error) {
            alert(error.message || "Wystąpił błąd podczas analizy opisu.");
        } finally {
            autoTagButton.disabled = false;
            autoTagButton.textContent = originalText;
        }
    });
});