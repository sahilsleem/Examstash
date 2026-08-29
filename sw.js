const CACHE_NAME = 'examstash-v3';
const STATIC_ASSETS = [
  '/',
  '/assets/css/global.css',
  '/assets/js/search-index.js',
  '/assets/js/search.js',
  '/assets/js/bookmarks.js',
  '/assets/js/pwa.js',
  '/assets/js/request-paper.js',
  '/assets/icons/icon.svg',
  '/manifest.json'
];

self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME).then(cache => {
      return cache.addAll(STATIC_ASSETS);
    }).then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(keys => {
      return Promise.all(
        keys.map(key => {
          if (key !== CACHE_NAME) {
            return caches.delete(key);
          }
        })
      );
    }).then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', event => {
  const url = new URL(event.request.url);

  // Network-first with cache fallback for HTML pages
  if (event.request.mode === 'navigate') {
    event.respondWith(
      fetch(event.request).then(response => {
        if (response.status === 200) {
          const clone = response.clone();
          caches.open(CACHE_NAME).then(cache => cache.put(event.request, clone));
        }
        return response;
      }).catch(() => {
        return caches.match(event.request).then(cached => {
          return cached || caches.match('/');
        });
      })
    );
    return;
  }

  // Network-first for static updates with cache fallback
  event.respondWith(
    fetch(event.request).then(response => {
      if (response.status === 200) {
        const clone = response.clone();
        caches.open(CACHE_NAME).then(cache => cache.put(event.request, clone));
      }
      return response;
    }).catch(() => {
      return caches.match(event.request);
    })
  );
});
