/**
 * Shared Expenses — Global Script
 * Handles: Sidebar, Toasts, Modals, Helpers
 */

/* ─── Sidebar Toggle ──────────────────────────────────────── */
document.addEventListener('DOMContentLoaded', () => {
  const sidebar  = document.getElementById('sidebar');
  const overlay  = document.getElementById('sidebarOverlay');
  const menuBtn  = document.getElementById('menuToggle');

  function openSidebar() {
    sidebar?.classList.add('open');
    overlay?.classList.add('open');
    document.body.style.overflow = 'hidden';
  }

  function closeSidebar() {
    sidebar?.classList.remove('open');
    overlay?.classList.remove('open');
    document.body.style.overflow = '';
  }

  menuBtn?.addEventListener('click', openSidebar);
  overlay?.addEventListener('click', closeSidebar);

  /* Close sidebar on nav click (mobile) */
  document.querySelectorAll('.nav-item').forEach(link => {
    link.addEventListener('click', () => {
      if (window.innerWidth < 769) closeSidebar();
    });
  });

  /* Mark active nav item */
  const currentPage = window.location.pathname.split('/').pop() || 'dashboard.html';
  document.querySelectorAll('.nav-item').forEach(link => {
    const href = link.getAttribute('href') || '';
    if (href === currentPage || href.includes(currentPage)) {
      link.classList.add('active');
    }
  });
});

/* ─── Toast Notifications ─────────────────────────────────── */
const ToastSystem = (() => {
  let container;

  function getContainer() {
    if (!container) {
      container = document.createElement('div');
      container.className = 'toast-container';
      document.body.appendChild(container);
    }
    return container;
  }

  function show({ title, message, type = 'info', duration = 4000 }) {
    const icons = {
      success: `<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M20 6 9 17l-5-5"/></svg>`,
      error:   `<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><circle cx="12" cy="12" r="10"/><path d="m15 9-6 6M9 9l6 6"/></svg>`,
      warning: `<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3Z"/><path d="M12 9v4M12 17h.01"/></svg>`,
      info:    `<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><circle cx="12" cy="12" r="10"/><path d="M12 16v-4M12 8h.01"/></svg>`,
    };

    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    toast.innerHTML = `
      <span class="toast-icon">${icons[type]}</span>
      <div class="toast-content">
        ${title ? `<div class="toast-title">${title}</div>` : ''}
        ${message ? `<div class="toast-message">${message}</div>` : ''}
      </div>
      <button class="toast-close" aria-label="Close">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M18 6 6 18M6 6l12 12"/></svg>
      </button>
    `;

    const c = getContainer();
    c.appendChild(toast);

    toast.querySelector('.toast-close').addEventListener('click', () => remove(toast));

    const timer = setTimeout(() => remove(toast), duration);
    toast._timer = timer;
    return toast;
  }

  function remove(toast) {
    clearTimeout(toast._timer);
    toast.classList.add('removing');
    setTimeout(() => toast.remove(), 300);
  }

  return { show, success: m => show({...m, type:'success'}),
                  error:   m => show({...m, type:'error'}),
                  warning: m => show({...m, type:'warning'}),
                  info:    m => show({...m, type:'info'}) };
})();

/* ─── Modal System ────────────────────────────────────────── */
const ModalSystem = (() => {
  function open(id) {
    const modal = document.getElementById(id);
    if (modal) {
      modal.classList.add('open');
      document.body.style.overflow = 'hidden';
    }
  }

  function close(id) {
    const modal = document.getElementById(id);
    if (modal) {
      modal.classList.remove('open');
      document.body.style.overflow = '';
    }
  }

  /* Wire up data-modal-open / data-modal-close attributes */
  document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('[data-modal-open]').forEach(btn => {
      btn.addEventListener('click', () => open(btn.dataset.modalOpen));
    });

    document.querySelectorAll('[data-modal-close]').forEach(btn => {
      btn.addEventListener('click', () => close(btn.dataset.modalClose));
    });

    document.querySelectorAll('.modal-overlay').forEach(overlay => {
      overlay.addEventListener('click', e => {
        if (e.target === overlay) {
          overlay.classList.remove('open');
          document.body.style.overflow = '';
        }
      });
    });

    /* Escape key */
    document.addEventListener('keydown', e => {
      if (e.key === 'Escape') {
        document.querySelectorAll('.modal-overlay.open').forEach(m => {
          m.classList.remove('open');
          document.body.style.overflow = '';
        });
      }
    });
  });

  return { open, close };
})();

/* ─── Utility Functions ───────────────────────────────────── */

/** Format currency */
function formatCurrency(amount, currency = 'USD') {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency,
    minimumFractionDigits: 2,
  }).format(amount);
}

/** Format date */
function formatDate(dateStr) {
  const d = new Date(dateStr);
  return d.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
}

/** Relative time */
function relativeTime(dateStr) {
  const diff = Date.now() - new Date(dateStr).getTime();
  const mins  = Math.floor(diff / 60000);
  const hours = Math.floor(diff / 3600000);
  const days  = Math.floor(diff / 86400000);

  if (mins < 1)   return 'just now';
  if (mins < 60)  return `${mins}m ago`;
  if (hours < 24) return `${hours}h ago`;
  if (days < 30)  return `${days}d ago`;
  return formatDate(dateStr);
}

/** Debounce */
function debounce(fn, delay = 300) {
  let timer;
  return (...args) => {
    clearTimeout(timer);
    timer = setTimeout(() => fn(...args), delay);
  };
}

/** Generate initials */
function getInitials(name = '') {
  return name.split(' ').map(w => w[0]).join('').toUpperCase().slice(0, 2);
}

/** Avatar color from name */
function avatarColor(name = '') {
  const colors = [
    'linear-gradient(135deg,#7C3AED,#5B21B6)',
    'linear-gradient(135deg,#10B981,#059669)',
    'linear-gradient(135deg,#F59E0B,#D97706)',
    'linear-gradient(135deg,#EF4444,#DC2626)',
    'linear-gradient(135deg,#3B82F6,#2563EB)',
    'linear-gradient(135deg,#EC4899,#DB2777)',
  ];
  const idx = name.charCodeAt(0) % colors.length;
  return colors[idx];
}

/* ─── Form Validation Helper ──────────────────────────────── */
const Validator = {
  required: (val) => val.trim() !== '' || 'This field is required',
  email:    (val) => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(val) || 'Enter a valid email address',
  minLength:(n) => (val) => val.length >= n || `Minimum ${n} characters required`,
  maxLength:(n) => (val) => val.length <= n || `Maximum ${n} characters allowed`,
  number:   (val) => !isNaN(parseFloat(val)) && isFinite(val) || 'Enter a valid number',
  positive: (val) => parseFloat(val) > 0 || 'Value must be greater than 0',

  run(value, rules) {
    for (const rule of rules) {
      const result = rule(value);
      if (result !== true) return result;
    }
    return null;
  },

  showError(inputEl, message) {
    const group = inputEl.closest('.form-group');
    const err   = group?.querySelector('.form-error');
    inputEl.classList.add('error');
    inputEl.classList.remove('success');
    if (err) { err.textContent = message; err.classList.add('visible'); }
  },

  showSuccess(inputEl) {
    const group = inputEl.closest('.form-group');
    const err   = group?.querySelector('.form-error');
    inputEl.classList.remove('error');
    inputEl.classList.add('success');
    if (err) { err.textContent = ''; err.classList.remove('visible'); }
  },

  clearError(inputEl) {
    const group = inputEl.closest('.form-group');
    const err   = group?.querySelector('.form-error');
    inputEl.classList.remove('error', 'success');
    if (err) { err.textContent = ''; err.classList.remove('visible'); }
  },
};

/* ─── Expose globals ──────────────────────────────────────── */
window.ToastSystem  = ToastSystem;
window.ModalSystem  = ModalSystem;
window.Validator    = Validator;
window.formatCurrency = formatCurrency;
window.formatDate     = formatDate;
window.relativeTime   = relativeTime;
window.debounce       = debounce;
window.getInitials    = getInitials;
window.avatarColor    = avatarColor;
