/**
 * ExamStash PWA & Mobile Navigation Controller
 */

(function () {
  // 1. Service Worker Registration
  if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
      navigator.serviceWorker.register('/sw.js')
        .then(reg => {
          // Registered
        })
        .catch(err => {
          console.warn('SW registration failed:', err);
        });
    });
  }

  // 2. Mobile Bottom Navigation Bar Injection
  function ensureMobileBottomNav() {
    if (document.getElementById('mobile-bottom-nav')) return;

    const navHTML = `
      <nav id="mobile-bottom-nav" class="mobile-bottom-nav" aria-label="Mobile Navigation">
        <a href="/" class="mobile-nav-item ${window.location.pathname === '/' ? 'active' : ''}">
          <span class="mobile-nav-icon">🏠</span>
          <span class="mobile-nav-label">Home</span>
        </a>
        <a href="${window.location.pathname === '/' ? 'javascript:void(0)' : '/jkbose/'}" class="mobile-nav-item" id="mobile-nav-boards">
          <span class="mobile-nav-icon">🏫</span>
          <span class="mobile-nav-label">Boards</span>
        </a>
        <a href="${window.location.pathname === '/' ? 'javascript:void(0)' : '/islamia-college/'}" class="mobile-nav-item" id="mobile-nav-colleges">
          <span class="mobile-nav-icon">🏛️</span>
          <span class="mobile-nav-label">Colleges</span>
        </a>
        <button type="button" class="mobile-nav-item" id="mobile-nav-saved">
          <span class="mobile-nav-icon" style="position: relative;">
            🔖
            <span class="badge-count bookmark-badge-count" style="top: -8px; right: -8px;">0</span>
          </span>
          <span class="mobile-nav-label">Saved</span>
        </button>
        <button type="button" class="mobile-nav-item" id="mobile-nav-search">
          <span class="mobile-nav-icon">🔍</span>
          <span class="mobile-nav-label">Search</span>
        </button>
      </nav>
    `;

    document.body.insertAdjacentHTML('beforeend', navHTML);

    // Wire events
    const boardsBtn = document.getElementById('mobile-nav-boards');
    if (boardsBtn && window.location.pathname === '/') {
      boardsBtn.addEventListener('click', () => {
        if (typeof showTab === 'function') showTab(0);
        document.querySelector('.tabs')?.scrollIntoView({ behavior: 'smooth' });
      });
    }

    const collegesBtn = document.getElementById('mobile-nav-colleges');
    if (collegesBtn && window.location.pathname === '/') {
      collegesBtn.addEventListener('click', () => {
        if (typeof showTab === 'function') showTab(1);
        document.querySelector('.tabs')?.scrollIntoView({ behavior: 'smooth' });
      });
    }

    const savedBtn = document.getElementById('mobile-nav-saved');
    if (savedBtn) {
      savedBtn.addEventListener('click', () => {
        if (window.ExamStashBookmarks) {
          window.ExamStashBookmarks.openDrawer();
        }
      });
    }

    const searchBtn = document.getElementById('mobile-nav-search');
    if (searchBtn) {
      searchBtn.addEventListener('click', () => {
        const input = document.querySelector('.search-wrap input');
        if (input) {
          input.scrollIntoView({ behavior: 'smooth', block: 'center' });
          setTimeout(() => input.focus(), 300);
        } else {
          window.location.href = '/';
        }
      });
    }
  }

  // 3. Install App Prompt Banner
  let deferredPrompt = null;

  window.addEventListener('beforeinstallprompt', (e) => {
    e.preventDefault();
    deferredPrompt = e;
    showInstallBanner();
  });

  function showInstallBanner() {
    if (document.getElementById('pwa-install-banner') || sessionStorage.getItem('pwa_prompt_dismissed')) return;

    const bannerHTML = `
      <div id="pwa-install-banner" class="pwa-install-banner">
        <div class="pwa-banner-icon">
          <img src="/assets/icons/icon.svg" alt="ExamStash App" width="36" height="36" />
        </div>
        <div class="pwa-banner-text">
          <strong>Install ExamStash</strong>
          <span>Access question papers offline on your phone</span>
        </div>
        <div class="pwa-banner-actions">
          <button type="button" class="btn-pwa-install" id="btn-pwa-install">Install</button>
          <button type="button" class="btn-pwa-dismiss" id="btn-pwa-dismiss">&times;</button>
        </div>
      </div>
    `;

    document.body.insertAdjacentHTML('beforeend', bannerHTML);

    document.getElementById('btn-pwa-install').addEventListener('click', async () => {
      if (deferredPrompt) {
        deferredPrompt.prompt();
        const { outcome } = await deferredPrompt.userChoice;
        deferredPrompt = null;
        dismissInstallBanner();
      }
    });

    document.getElementById('btn-pwa-dismiss').addEventListener('click', () => {
      sessionStorage.setItem('pwa_prompt_dismissed', 'true');
      dismissInstallBanner();
    });
  }

  function dismissInstallBanner() {
    const banner = document.getElementById('pwa-install-banner');
    if (banner) banner.remove();
  }

  document.addEventListener('DOMContentLoaded', () => {
    ensureMobileBottomNav();
  });
})();
