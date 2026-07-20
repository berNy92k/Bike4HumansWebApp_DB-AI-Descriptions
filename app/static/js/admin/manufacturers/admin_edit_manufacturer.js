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

            const payload = {
                name: document.getElementById("name")?.value?.trim() || "",
                description: document.getElementById("description")?.value || "",
            };

            const response = await fetch("/admin/manufacturer/ai-generate-description", {
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
    const form = document.getElementById("manufacturer-edit-form");
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

    const manufacturerIdMatch = window.location.pathname.match(/\/admin\/manufacturer\/(\d+)\/edit$/);
    const manufacturerId = manufacturerIdMatch ? manufacturerIdMatch[1] : null;

    if (!manufacturerId) {
        showMessage("Nie udało się ustalić ID producenta.", "error");
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
            is_description_ai_generated: document.getElementById("is_description_ai_generated")?.value === "true"
        };

        if (!payload.name) {
            showMessage("Uzupełnij nazwę producenta.", "error");
            return;
        }

        try {
            showMessage("Zapisywanie zmian...", "info");

            const response = await fetch(`/admin/manufacturer/${manufacturerId}`, {
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

            window.location.href = `/admin/manufacturer/${manufacturerId}/details`;
        } catch (error) {
            showMessage("Wystąpił błąd sieci podczas zapisu zmian.", "error");
        }
    });
});