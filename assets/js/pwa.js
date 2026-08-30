/**
 * Islamia College Portal — PWA Service Worker Registration
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

  // 2. Install App Prompt Banner (Unobtrusive)
  let deferredPrompt = null;

  window.addEventListener('beforeinstallprompt', (e) => {
    e.preventDefault();
    deferredPrompt = e;
  });
})();
