const API_BASE = "/";

export async function startAnalysis(githubUrl) {
  const res = await fetch(`${API_BASE}analyze`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ github_url: githubUrl }),
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || "Failed to start analysis");
  }
  return res.json();
}

export async function getStatus(jobId) {
  const res = await fetch(`${API_BASE}status/${jobId}`);
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || "Failed to fetch status");
  }
  return res.json();
}

export async function getResult(jobId) {
  const res = await fetch(`${API_BASE}result/${jobId}`);
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || "Failed to fetch result");
  }
  return res.json();
}

export async function sendChatMessage(jobId, message, history = []) {
  const res = await fetch(`${API_BASE}chat/${jobId}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message, history }),
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || "Failed to send message");
  }
  return res.json();
}
