const API_URL =
  import.meta.env.VITE_API_URL || "http://127.0.0.1:8000";

export async function planTrip(payload) {
  const res = await fetch(`${API_URL}/api/plan`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  });

  if (!res.ok) {
    let detail = `Request failed (${res.status})`;

    try {
      const body = await res.json();
      if (body.detail) detail = body.detail;
    } catch {}

    throw new Error(detail);
  }

  return res.json();
}