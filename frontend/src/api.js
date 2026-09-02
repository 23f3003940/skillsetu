// Backend runs separately on port 5000 (see backend/app.py)
const BASE_URL = "http://localhost:5000";

async function apiGet(url) {
  const res = await fetch(BASE_URL + url, { credentials: "include" });
  const out = await res.json();
  if (!res.ok) throw out;
  return out;
}

async function apiSend(url, method, body) {
  const res = await fetch(BASE_URL + url, {
    method,
    credentials: "include",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body || {})
  });
  const out = await res.json();
  if (!res.ok) throw out;
  return out;
}

async function apiUpload(url, formData) {
  const res = await fetch(BASE_URL + url, {
    method: "POST",
    credentials: "include",
    body: formData
  });
  const out = await res.json();
  if (!res.ok) throw out;
  return out;
}

function resumeUrl(filename) {
  return BASE_URL + "/view_resume/" + filename;
}

export { apiGet, apiSend, apiUpload, resumeUrl };
