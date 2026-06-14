/**
 * Shared Sidebar Component
 * Inject sidebar + topbar into any dashboard page.
 * Usage: <script src="_sidebar.js"></script> + renderShell({ title, subtitle })
 */

function renderShell({ title = '', subtitle = '', topbarActions = '' } = {}) {
  const sidebarHTML = `
  <!-- Mobile overlay -->
  <div class="sidebar-overlay" id="sidebarOverlay"></div>

  <!-- Sidebar -->
  <aside class="sidebar" id="sidebar" aria-label="Main navigation">
    <a class="sidebar-brand" href="dashboard.html">
      <div class="brand-logo" aria-hidden="true">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M2 20h20"/>
          <path d="M5 20V8l7-6 7 6v12"/>
          <path d="M9 20v-5h6v5"/>
          <circle cx="12" cy="10" r="1" fill="white"/>
        </svg>
      </div>
      <div class="brand-info">
        <div class="brand-name">SharedExpenses</div>
        <div class="brand-tagline">Roommate Finance</div>
      </div>
    </a>

    <!-- Main nav -->
    <nav class="sidebar-section" aria-label="Main">
      <div class="sidebar-section-title">Overview</div>
      <a class="nav-item" href="dashboard.html" aria-label="Dashboard">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <rect width="7" height="9" x="3" y="3" rx="1"/><rect width="7" height="5" x="14" y="3" rx="1"/>
          <rect width="7" height="9" x="14" y="12" rx="1"/><rect width="7" height="5" x="3" y="16" rx="1"/>
        </svg>
        Dashboard
      </a>
      <a class="nav-item" href="group.html" aria-label="Groups">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/>
          <circle cx="9" cy="7" r="4"/>
          <path d="M23 21v-2a4 4 0 0 0-3-3.87M16 3.13a4 4 0 0 1 0 7.75"/>
        </svg>
        Groups
      </a>
    </nav>

    <!-- Expenses nav -->
    <nav class="sidebar-section" aria-label="Expenses">
      <div class="sidebar-section-title">Expenses</div>
      <a class="nav-item" href="add-expense.html" aria-label="Add Expense">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <circle cx="12" cy="12" r="10"/><path d="M12 8v8M8 12h8"/>
        </svg>
        Add Expense
      </a>
      <a class="nav-item" href="balances.html" aria-label="Balances">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="m16 16 3-8 3 8c-.87.65-1.92 1-3 1s-2.13-.35-3-1Z"/>
          <path d="m2 16 3-8 3 8c-.87.65-1.92 1-3 1s-2.13-.35-3-1Z"/>
          <path d="M7 21h10M12 3v13M3 7h2c2 0 5 1 7 1s5-1 7-1h2"/>
        </svg>
        Balances
      </a>
      <a class="nav-item" href="settlements.html" aria-label="Settlements">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M12 2v20M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/>
        </svg>
        Settlements
      </a>
    </nav>

    <!-- People nav -->
    <nav class="sidebar-section" aria-label="People">
      <div class="sidebar-section-title">People</div>
      <a class="nav-item" href="members.html" aria-label="Members">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/>
          <circle cx="12" cy="7" r="4"/>
        </svg>
        Members
      </a>
    </nav>

    <!-- Import nav -->
    <nav class="sidebar-section" aria-label="Import">
      <div class="sidebar-section-title">Import & Reports</div>
      <a class="nav-item" href="import-csv.html" aria-label="Import CSV">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
          <path d="M14 2v6h6M12 18v-6M9 15l3 3 3-3"/>
        </svg>
        Import CSV
      </a>
      <a class="nav-item" href="anomalies.html" aria-label="Anomalies">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3Z"/>
          <path d="M12 9v4M12 17h.01"/>
        </svg>
        Anomalies
        <span class="nav-badge">3</span>
      </a>
      <a class="nav-item" href="import-report.html" aria-label="Import Report">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
          <path d="M14 2v6h6M16 13H8M16 17H8M10 9H8"/>
        </svg>
        Import Report
      </a>
    </nav>

    <!-- Sidebar footer / user -->
    <div class="sidebar-footer">
      <div class="user-card" tabindex="0" role="button" aria-label="User profile">
        <div class="user-avatar" aria-hidden="true">JD</div>
        <div>
          <div class="user-name">Jane Doe</div>
          <div class="user-email">jane@example.com</div>
        </div>
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="margin-left:auto;color:var(--text-muted)">
          <path d="m6 9 6 6 6-6"/>
        </svg>
      </div>
    </div>
  </aside>
  `;

  const topbarHTML = `
  <header class="topbar" role="banner">
    <div class="topbar-left">
      <button class="menu-toggle" id="menuToggle" aria-label="Open menu" aria-controls="sidebar">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M3 6h18M3 12h18M3 18h18"/>
        </svg>
      </button>
      <div>
        <div class="topbar-title">${title}</div>
        ${subtitle ? `<div class="topbar-subtitle">${subtitle}</div>` : ''}
      </div>
    </div>
    <div class="topbar-right">
      ${topbarActions}
      <!-- Notification bell -->
      <button class="btn btn-ghost btn-icon" aria-label="Notifications" id="notifBtn" title="Notifications">
        <svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M6 8a6 6 0 0 1 12 0c0 7 3 9 3 9H3s3-2 3-9"/>
          <path d="M10.3 21a1.94 1.94 0 0 0 3.4 0"/>
        </svg>
      </button>
      <!-- Log out -->
      <a href="login.html" class="btn btn-ghost btn-sm" aria-label="Sign out">
        <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/>
          <polyline points="16 17 21 12 16 7"/>
          <line x1="21" y1="12" x2="9" y2="12"/>
        </svg>
        Sign out
      </a>
    </div>
  </header>
  `;

  /* Inject sidebar before main-content */
  const shell = document.querySelector('.app-shell');
  if (shell) {
    shell.insertAdjacentHTML('afterbegin', sidebarHTML);
    const mainContent = shell.querySelector('.main-content');
    if (mainContent) mainContent.insertAdjacentHTML('afterbegin', topbarHTML);
  }

  /* Wire notification button */
  document.getElementById('notifBtn')?.addEventListener('click', () => {
    ToastSystem.info({ title: 'Notifications', message: 'You have 2 new settlement requests.' });
  });
}
