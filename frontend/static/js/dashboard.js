// HealthShield AI — Global JS utilities
const API = '/api';

function token() {
  return localStorage.getItem('access_token') || '';
}

function authHeaders() {
  return {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer ' + token()
  };
}

function logout() {
  const refresh = localStorage.getItem('refresh_token');
  fetch(`${API}/auth/logout/`, {
    method: 'POST',
    headers: authHeaders(),
    body: JSON.stringify({ refresh })
  }).finally(() => {
    localStorage.clear();
    window.location.href = '/login/';
  });
}

function toggleTheme() {
  const html = document.documentElement;
  const isDark = html.getAttribute('data-bs-theme') === 'dark';
  const newTheme = isDark ? 'light' : 'dark';
  html.setAttribute('data-bs-theme', newTheme);
  document.getElementById('themeIcon').className = isDark ? 'bi bi-moon-fill' : 'bi bi-sun-fill';
  localStorage.setItem('theme', newTheme);
}

// Restore theme on load
(function () {
  const saved = localStorage.getItem('theme') || 'light';
  document.documentElement.setAttribute('data-bs-theme', saved);
  const icon = document.getElementById('themeIcon');
  if (icon) icon.className = saved === 'dark' ? 'bi bi-sun-fill' : 'bi bi-moon-fill';
})();

// Check if token is present, redirect to login if not
function requireAuth() {
  if (!token()) {
    window.location.href = '/login/';
    return false;
  }
  return true;
}

// Load user info into navbar
window.addEventListener('DOMContentLoaded', async () => {
  if (!token() && !window.location.pathname.includes('/login/')) {
    window.location.href = '/login/';
    return;
  }
  const user = JSON.parse(localStorage.getItem('user') || '{}');
  const el = document.getElementById('userName');
  if (el && user.nombre) el.textContent = user.nombre;

  // Check alerts
  try {
    const r = await fetch(`${API}/etl/alertas/`, { headers: authHeaders() });
    const d = await r.json();
    const count = d.count || (d.results && d.results.length) || 0;
    if (count > 0) {
      const el = document.getElementById('alertaCount');
      const banner = document.getElementById('alertaBanner');
      if (el) el.textContent = count;
      if (banner) banner.classList.remove('d-none');
    }
  } catch (e) { /* no alert info */ }
});
