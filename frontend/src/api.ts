const API_BASE_URL = "";

export async function register(email: string, password: string) {
  const response = await fetch(`${API_BASE_URL}/auth/register`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password }),
  });
  if (!response.ok) {
    throw new Error(`Ошибка регистрации: ${response.statusText}`);
  }
  return await response.json();
}

export async function login(email: string, password: string) {
  const response = await fetch(`${API_BASE_URL}/auth/login`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password }),
  });
  if (!response.ok) {
    throw new Error(`Ошибка входа: ${response.statusText}`);
  }
  return await response.json();
}

export async function createResume(token: string, title: string, content: string) {
  const response = await fetch(`${API_BASE_URL}/resumes`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify({ title, content }),
  });
  if (!response.ok) {
    throw new Error(`Ошибка создания резюме: ${response.statusText}`);
  }
  return await response.json();
}

export async function listResumes(token: string) {
  const response = await fetch(`${API_BASE_URL}/resumes`, {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });
  if (!response.ok) {
    throw new Error(`Ошибка получения списка резюме: ${response.statusText}`);
  }
  return await response.json();
}

export async function getResume(token: string, resumeId: number) {
  const response = await fetch(`${API_BASE_URL}/resumes/${resumeId}`, {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });
  if (!response.ok) {
    throw new Error(`Ошибка получения резюме: ${response.statusText}`);
  }
  return await response.json();
}

export async function updateResume(token: string, resumeId: number, title: string, content: string) {
  const response = await fetch(`${API_BASE_URL}/resumes/${resumeId}`, {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify({ title, content }),
  });
  if (!response.ok) {
    throw new Error(`Ошибка обновления резюме: ${response.statusText}`);
  }
  return await response.json();
}

export async function deleteResume(token: string, resumeId: number) {
  const response = await fetch(`${API_BASE_URL}/resumes/${resumeId}`, {
    method: "DELETE",
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });
  if (!response.ok) {
    throw new Error(`Ошибка удаления резюме: ${response.statusText}`);
  }
}

export async function improveResume(token: string, resumeId: number) {
  const response = await fetch(`${API_BASE_URL}/resumes/${resumeId}/improvements/improve`, {
    method: "POST",
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });
  if (!response.ok) {
    throw new Error(`Ошибка улучшения резюме: ${response.statusText}`);
  }
  return await response.json();
}

export async function listImprovements(token: string, resumeId: number) {
  const response = await fetch(`${API_BASE_URL}/resumes/${resumeId}/improvements`, {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });
  if (!response.ok) {
    throw new Error(`Ошибка получения улучшений: ${response.statusText}`);
  }
  return await response.json();
}
