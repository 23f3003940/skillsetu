
const BASE_URL = "https://skillsetu-scd2.onrender.com";

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
