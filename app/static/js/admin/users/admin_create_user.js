document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("user-create-form");
  const messageBox = document.getElementById("form-message");

  if (!form) return;

  const showMessage = (text, type = "error") => {
    if (!messageBox) return;
    messageBox.textContent = text;
    messageBox.className = `form-message ${type}`;
  };

  const clearMessage = () => {
    if (!messageBox) return;
    messageBox.textContent = "";
    messageBox.className = "form-message";
  };

  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    clearMessage();

    const token = window.getCookieValue?.("access_token");
    if (!token) {
      window.location.href = "/auth/login";
      return;
    }

    const formData = new FormData(form);

    const payload = {
      username: formData.get("username")?.toString().trim(),
      email: formData.get("email")?.toString().trim(),
      name: formData.get("name")?.toString().trim(),
      surname: formData.get("surname")?.toString().trim(),
      role_id: Number(formData.get("role_id")),
      password: formData.get("password")?.toString() || "",
      is_active: formData.get("is_active") === "on",
      email_verified: formData.get("email_verified") === "on",
    };

    try {
      const response = await fetch("/admin/user", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Bearer ${token}`,
        },
        body: JSON.stringify(payload),
      });

      if (response.ok) {
        window.location.href = "/admin/user/list";
        return;
      }

      const data = await response.json().catch(() => null);
      showMessage(data?.detail || "Nie udało się dodać użytkownika.");
    } catch (error) {
      showMessage("Wystąpił błąd podczas dodawania użytkownika.");
    }
  });
});
