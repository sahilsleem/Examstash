/**
 * ExamStash Privacy-Friendly Analytics & Event Tracking
 * Tracks pageviews, searches, paper downloads, previews, and shares
 */

(function () {
  // Enter your Google Analytics 4 Measurement ID here when ready (e.g. 'G-XXXXXXXXXX')
  const GA_MEASUREMENT_ID = '';

  // 1. Initialize GA4 if ID is provided
  if (GA_MEASUREMENT_ID) {
    const script = document.createElement('script');
    script.async = true;
    script.src = `https://www.googletagmanager.com/gtag/js?id=${GA_MEASUREMENT_ID}`;
    document.head.appendChild(script);

    window.dataLayer = window.dataLayer || [];
    function gtag(){dataLayer.push(arguments);}
    window.gtag = gtag;
    gtag('js', new Date());
    gtag('config', GA_MEASUREMENT_ID);
  }

  // 2. Event Dispatcher Helper
  function trackEvent(eventName, eventParams = {}) {
    if (window.gtag) {
      window.gtag('event', eventName, eventParams);
    }
  }

  window.ExamStashAnalytics = {
    track: trackEvent
  };

  // 3. Auto-track user actions on page
  document.addEventListener('DOMContentLoaded', () => {
    // Track Paper Downloads
    document.querySelectorAll('.download-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        const title = document.querySelector('h1')?.textContent || document.title;
        trackEvent('download_paper', {
          paper_title: title,
          paper_url: window.location.pathname
        });
      });
    });

    // Track Online PDF Previews
    const previewBtn = document.getElementById('preview-pdf-btn');
    if (previewBtn) {
      previewBtn.addEventListener('click', () => {
        const title = document.querySelector('h1')?.textContent || document.title;
        trackEvent('preview_paper', {
          paper_title: title,
          paper_url: window.location.pathname
        });
      });
    }

    // Track WhatsApp Shares
    document.querySelectorAll('.btn-share-wa').forEach(btn => {
      btn.addEventListener('click', () => {
        trackEvent('share_whatsapp', {
          paper_url: window.location.pathname
        });
      });
    });

    // Track Telegram Shares
    document.querySelectorAll('.btn-share-tg').forEach(btn => {
      btn.addEventListener('click', () => {
        trackEvent('share_telegram', {
          paper_url: window.location.pathname
        });
      });
    });

    // Track Bookmarks
    document.querySelectorAll('.bookmark-toggle-trigger').forEach(btn => {
      btn.addEventListener('click', () => {
        const title = btn.getAttribute('data-title') || document.title;
        trackEvent('bookmark_paper', {
          paper_title: title,
          paper_id: btn.getAttribute('data-id')
        });
      });
    });
  });
})();
