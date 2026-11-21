const form = document.getElementById("restaurant-form");
const message = document.getElementById("message");

function show(text, ok) {
  if (!message) return;
  message.textContent = text;
  message.className = ok ? "ok" : "error";
}

async function errorText(response) {
  try {
    const body = await response.json();
    if (typeof body.detail === "string") return body.detail;
    if (Array.isArray(body.detail)) {
      return body.detail.map((e) => `${e.loc.slice(-1)[0]}: ${e.msg}`).join(" | ");
    }
  } catch (_) {}
  return "Error al guardar";
}

if (form) {
  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    const formData = Object.fromEntries(new FormData(form));
    formData.price = Number(formData.price);
    if (!formData.photoUrl.trim()) formData.photoUrl = null;

    const id = form.dataset.id;
    const response = await fetch(id ? `/api/v1/restaurants/${id}` : "/api/v1/restaurants", {
      method: id ? "PATCH" : "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(formData),
    });

    if (!response.ok) {
      show(await errorText(response), false);
      return;
    }
    if (id) {
      show("Restaurante actualizado correctamente", true);
      setTimeout(() => (window.location.href = `/restaurants/${id}`), 800);
    } else {
      show("Restaurante creado correctamente", true);
      form.reset();
    }
  });
}

const deleteBtn = document.getElementById("delete-btn");
if (deleteBtn) {
  deleteBtn.addEventListener("click", async () => {
    if (!confirm(`¿Eliminar "${deleteBtn.dataset.name}"? Esta acción no se puede deshacer.`)) return;
    const response = await fetch(`/api/v1/restaurants/${deleteBtn.dataset.id}`, { method: "DELETE" });
    if (response.status === 204) {
      window.location.href = "/";
    } else {
      show(await errorText(response), false);
    }
  });
}
