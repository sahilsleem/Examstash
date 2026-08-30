/**
 * Islamia College Portal — Clean PWA & Cache Clearer
 */

(function () {
  // Prevent any browser install prompts or popups
  window.addEventListener('beforeinstallprompt', (e) => {
    e.preventDefault();
    return false;
  });

  // Auto-clear stale caches from previous site versions
  if ('caches' in window) {
    caches.keys().then((names) => {
      names.forEach((name) => {
        if (name.includes('examstash')) {
          caches.delete(name);
        }
      });
    });
  }

  // Remove any legacy service worker if present to prevent caching stale pages
  if ('serviceWorker' in navigator) {
    navigator.serviceWorker.getRegistrations().then((registrations) => {
      for (let registration of registrations) {
        registration.update();
      }
    });
  }
})();
