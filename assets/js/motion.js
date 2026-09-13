/**
 * ExamStash 2.0 — Premium Motion System
 * Lightweight IntersectionObserver for scroll reveals.
 */

document.addEventListener('DOMContentLoaded', () => {
  // Respect reduced motion preference
  const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (prefersReducedMotion) return;

  // Elements to reveal on scroll
  // Add .reveal-on-scroll to sections that are likely below the fold
  const elementsToReveal = document.querySelectorAll('.details-section, .share-box, footer');

  elementsToReveal.forEach(el => {
    el.classList.add('reveal-on-scroll');
  });

  const observerOptions = {
    root: null,
    rootMargin: '0px 0px -40px 0px',
    threshold: 0.05
  };

  const revealObserver = new IntersectionObserver((entries, observer) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('is-visible');
        observer.unobserve(entry.target); // Only animate once
      }
    });
  }, observerOptions);

  document.querySelectorAll('.reveal-on-scroll').forEach(el => {
    revealObserver.observe(el);
  });
});
