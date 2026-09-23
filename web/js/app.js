// Shared helper: call the backend and get JSON back.
const API_BASE = '../backend/api';

async function api(path, { method = 'GET', body } = {}) {
  const res = await fetch(`${API_BASE}/${path}`, {
    method,
    headers: body ? { 'Content-Type': 'application/json' } : {},
    body: body ? JSON.stringify(body) : undefined,
    credentials: 'same-origin',
  });
  const data = await res.json().catch(() => ({}));
  if (!res.ok) throw new Error(data.error || `Request failed (${res.status})`);
  return data;
}
