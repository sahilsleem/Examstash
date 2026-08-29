/**
 * ExamStash Bookmarks Controller
 * Allows students to save question papers and subjects locally
 */

(function () {
  const STORAGE_KEY = 'examstash_saved_papers';

  function ensureStyles() {
    if (document.getElementById('examstash-bookmarks-style')) return;
    const style = document.createElement('style');
    style.id = 'examstash-bookmarks-style';
    style.textContent = `
      .drawer-overlay {
        position: fixed !important;
        inset: 0 !important;
        background: rgba(15, 23, 42, 0.5) !important;
        backdrop-filter: blur(4px) !important;
        z-index: 99998 !important;
        opacity: 0 !important;
        pointer-events: none !important;
        transition: opacity 0.25s ease !important;
      }
      .drawer-overlay.open {
        opacity: 1 !important;
        pointer-events: auto !important;
      }
      .drawer-panel {
        position: fixed !important;
        top: 0 !important;
        right: -420px !important;
        width: 100% !important;
        max-width: 380px !important;
        height: 100vh !important;
        background: #ffffff !important;
        box-shadow: -5px 0 25px rgba(0, 0, 0, 0.15) !important;
        z-index: 99999 !important;
        display: flex !important;
        flex-direction: column !important;
        transition: right 0.3s cubic-bezier(0.16, 1, 0.3, 1) !important;
        font-family: 'Segoe UI', system-ui, sans-serif !important;
      }
      .drawer-panel.open {
        right: 0 !important;
      }
      .drawer-header {
        padding: 20px 24px !important;
        border-bottom: 1px solid #e2e8f0 !important;
        display: flex !important;
        align-items: center !important;
        justify-content: space-between !important;
        background: #ffffff !important;
      }
      .drawer-header h3 {
        font-size: 18px !important;
        font-weight: 700 !important;
        color: #0f172a !important;
        display: flex !important;
        align-items: center !important;
        gap: 8px !important;
        margin: 0 !important;
      }
      .drawer-close {
        background: #f1f5f9 !important;
        border: 1px solid #e2e8f0 !important;
        color: #64748b !important;
        width: 32px !important;
        height: 32px !important;
        border-radius: 50% !important;
        font-size: 20px !important;
        cursor: pointer !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        line-height: 1 !important;
        transition: all 0.15s !important;
      }
      .drawer-close:hover {
        background: #f0fdfa !important;
        border-color: #0d9488 !important;
        color: #0d9488 !important;
      }
      .drawer-body {
        flex: 1 !important;
        overflow-y: auto !important;
        padding: 16px 20px !important;
        background: #ffffff !important;
      }
      .bookmark-card {
        display: flex !important;
        align-items: center !important;
        justify-content: space-between !important;
        padding: 12px 14px !important;
        border-radius: 12px !important;
        border: 1.5px solid #e2e8f0 !important;
        background: #f8fafc !important;
        margin-bottom: 10px !important;
        gap: 12px !important;
        transition: all 0.2s ease !important;
        text-decoration: none !important;
      }
      .bookmark-card:hover {
        border-color: #0d9488 !important;
        background: #f0fdfa !important;
      }
      .bookmark-card a {
        text-decoration: none !important;
        color: #0f172a !important;
        font-size: 13px !important;
        font-weight: 600 !important;
        flex: 1 !important;
        display: block !important;
      }
      .bookmark-remove-btn {
        background: transparent !important;
        border: none !important;
        color: #94a3b8 !important;
        cursor: pointer !important;
        font-size: 18px !important;
        padding: 4px !important;
        transition: color 0.15s !important;
        line-height: 1 !important;
      }
      .bookmark-remove-btn:hover {
        color: #ef4444 !important;
      }
      .bookmarks-empty {
        text-align: center !important;
        padding: 48px 20px !important;
        color: #64748b !important;
      }
      .bookmarks-empty-icon {
        font-size: 40px !important;
        margin-bottom: 12px !important;
      }
      .drawer-footer {
        padding: 16px 24px !important;
        border-top: 1px solid #e2e8f0 !important;
        display: flex !important;
        justify-content: space-between !important;
        align-items: center !important;
        background: #ffffff !important;
      }
      .btn-clear-all {
        background: transparent !important;
        border: none !important;
        color: #ef4444 !important;
        font-size: 13px !important;
        font-weight: 600 !important;
        cursor: pointer !important;
      }
      .btn-clear-all:hover {
        text-decoration: underline !important;
      }
    `;
    document.head.appendChild(style);
  }

  function getBookmarks() {
    try {
      return JSON.parse(localStorage.getItem(STORAGE_KEY)) || [];
    } catch (e) {
      return [];
    }
  }

  function saveBookmarks(list) {
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(list));
    } catch (e) {
      console.error('Failed to save bookmark', e);
    }
    updateUI();
  }

  function ensureDrawerInDOM() {
    ensureStyles();
    if (document.getElementById('examstash-bookmarks-drawer')) return;

    const drawerHTML = `
      <div id="examstash-bookmarks-overlay" class="drawer-overlay"></div>
      <div id="examstash-bookmarks-drawer" class="drawer-panel">
        <div class="drawer-header">
          <h3>🔖 Saved Papers</h3>
          <button class="drawer-close" aria-label="Close saved papers">&times;</button>
        </div>
        <div class="drawer-body" id="bookmarks-drawer-body"></div>
        <div class="drawer-footer">
          <span id="bookmarks-count-text" style="font-size: 13px; color: #64748b;">0 papers saved</span>
          <button class="btn-clear-all" id="bookmarks-clear-btn">Clear All</button>
        </div>
      </div>
    `;

    document.body.insertAdjacentHTML('beforeend', drawerHTML);

    document.getElementById('examstash-bookmarks-overlay').addEventListener('click', closeDrawer);
    document.querySelector('#examstash-bookmarks-drawer .drawer-close').addEventListener('click', closeDrawer);
    document.getElementById('bookmarks-clear-btn').addEventListener('click', () => {
      if (confirm('Clear all saved papers?')) {
        saveBookmarks([]);
      }
    });
  }

  function openDrawer() {
    ensureDrawerInDOM();
    renderBookmarksList();
    document.getElementById('examstash-bookmarks-overlay').classList.add('open');
    document.getElementById('examstash-bookmarks-drawer').classList.add('open');
    document.body.style.overflow = 'hidden';
  }

  function closeDrawer() {
    const overlay = document.getElementById('examstash-bookmarks-overlay');
    const drawer = document.getElementById('examstash-bookmarks-drawer');
    if (overlay) overlay.classList.remove('open');
    if (drawer) drawer.classList.remove('open');
    document.body.style.overflow = '';
  }

  function renderBookmarksList() {
    const body = document.getElementById('bookmarks-drawer-body');
    const countText = document.getElementById('bookmarks-count-text');
    if (!body) return;

    const list = getBookmarks();
    countText.textContent = `${list.length} paper${list.length === 1 ? '' : 's'} saved`;

    if (list.length === 0) {
      body.innerHTML = `
        <div class="bookmarks-empty">
          <div class="bookmarks-empty-icon">📂</div>
          <h4 style="font-size: 16px; margin-bottom: 6px; color: #0f172a;">No saved papers yet</h4>
          <p style="font-size: 13px; color: #64748b; line-height: 1.5;">Click the "☆ Save Paper" button on any paper page to keep it here for fast access.</p>
        </div>
      `;
      return;
    }

    body.innerHTML = list.map(item => {
      let cleanUrl = item.url || '/';
      if (!cleanUrl.startsWith('/')) cleanUrl = '/' + cleanUrl;
      return `
        <div class="bookmark-card">
          <a href="${cleanUrl}">
            <div style="font-size: 13px; font-weight: 700; color: #0f172a; margin-bottom: 2px;">${item.title}</div>
            <div style="font-size: 11px; color: #64748b; font-weight: 500;">${item.category || ''} ${item.year ? '• ' + item.year : ''}</div>
          </a>
          <button type="button" class="bookmark-remove-btn" data-id="${item.id}" title="Remove bookmark" aria-label="Remove bookmark">
            &times;
          </button>
        </div>
      `;
    }).join('');

    body.querySelectorAll('.bookmark-remove-btn').forEach(btn => {
      btn.addEventListener('click', (e) => {
        e.stopPropagation();
        const id = btn.getAttribute('data-id');
        removeBookmark(id);
      });
    });
  }

  function removeBookmark(id) {
    const list = getBookmarks().filter(item => item.id !== id);
    saveBookmarks(list);
    renderBookmarksList();
  }

  function updateUI() {
    const list = getBookmarks();
    
    // Update badge counts in headers
    document.querySelectorAll('.bookmark-badge-count').forEach(badge => {
      badge.textContent = list.length;
      badge.style.display = list.length > 0 ? 'inline-flex' : 'none';
    });

    // Update bookmark buttons on current page
    document.querySelectorAll('.bookmark-toggle-trigger').forEach(btn => {
      const id = btn.getAttribute('data-id');
      const isSaved = list.some(item => item.id === id);
      if (isSaved) {
        btn.classList.add('saved');
        btn.innerHTML = '⭐ Saved';
      } else {
        btn.classList.remove('saved');
        btn.innerHTML = '☆ Save Paper';
      }
    });

    if (document.getElementById('examstash-bookmarks-drawer')?.classList.contains('open')) {
      renderBookmarksList();
    }
  }

  window.ExamStashBookmarks = {
    toggle: function (item) {
      let list = getBookmarks();
      const exists = list.some(p => p.id === item.id);
      if (exists) {
        list = list.filter(p => p.id !== item.id);
      } else {
        if (!item.url.startsWith('/')) item.url = '/' + item.url;
        list.unshift(item);
      }
      saveBookmarks(list);
    },
    isSaved: function (id) {
      return getBookmarks().some(p => p.id === id);
    },
    getAll: getBookmarks,
    openDrawer: openDrawer,
    closeDrawer: closeDrawer
  };

  document.addEventListener('DOMContentLoaded', () => {
    ensureDrawerInDOM();
    updateUI();

    // Event delegation for opening bookmarks drawer
    document.addEventListener('click', (e) => {
      const btn = e.target.closest('.bookmarks-open-btn, #mobile-nav-saved');
      if (btn) {
        e.preventDefault();
        openDrawer();
      }
    });

    document.querySelectorAll('.bookmark-toggle-trigger').forEach(btn => {
      btn.addEventListener('click', () => {
        let url = btn.getAttribute('data-url') || window.location.pathname;
        if (!url.startsWith('/')) url = '/' + url;

        const item = {
          id: btn.getAttribute('data-id'),
          title: btn.getAttribute('data-title'),
          url: url,
          category: btn.getAttribute('data-category'),
          year: btn.getAttribute('data-year')
        };
        ExamStashBookmarks.toggle(item);
      });
    });
  });
})();
