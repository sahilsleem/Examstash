/**
 * ExamStash 2.0 — Motion System & Physical Floating Brand Engine
 */

document.addEventListener('DOMContentLoaded', () => {
  // Respect reduced motion preference
  const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  // ------------------------------------------------------------
  // 1. Scroll Reveal Observer
  // ------------------------------------------------------------
  if (!prefersReducedMotion) {
    const elementsToReveal = document.querySelectorAll('.details-section, .share-box, footer');
    elementsToReveal.forEach(el => el.classList.add('reveal-on-scroll'));

    const observerOptions = {
      root: null,
      rootMargin: '0px 0px -40px 0px',
      threshold: 0.05
    };

    const revealObserver = new IntersectionObserver((entries, observer) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-visible');
          observer.unobserve(entry.target);
        }
      });
    }, observerOptions);

    document.querySelectorAll('.reveal-on-scroll').forEach(el => {
      revealObserver.observe(el);
    });
  }

  // ------------------------------------------------------------
  // 2. Physical Floating Brand Engine (EXAMSTASH)
  // ------------------------------------------------------------
  const logoWrap = document.querySelector('.logo-physical-wrap');
  if (!logoWrap || prefersReducedMotion) return;

  // Physical State
  let targetX = 0;
  let targetY = 0;
  let targetRot = 0;

  let currentX = 0;
  let currentY = 0;
  let currentRot = 0;

  let shakeX = 0;
  let shakeY = 0;
  let shakeRot = 0;

  let idleAngle = 0;
  let hasSensorData = false;
  let lastShakeTime = 0;
  let lastAcc = { x: 0, y: 0, z: 0 };

  // Damping constants
  const damping = 0.085;      // smooth lag, weight and momentum
  const shakeDamping = 0.88;   // spring decay for shake impulses

  // Clamping helper
  const clamp = (val, min, max) => Math.min(Math.max(val, min), max);

  // ------------------------------------------------------------
  // Animation Loop (requestAnimationFrame)
  // ------------------------------------------------------------
  const updatePhysics = () => {
    // 1. Idle breathing float (subtle harmonic oscillation: ±1.4px, ±0.16deg)
    idleAngle += 0.024;
    const idleY = Math.sin(idleAngle) * 1.4;
    const idleRot = Math.sin(idleAngle * 0.7) * 0.16;

    // 2. Damped spring interpolation (smooth physical inertia)
    currentX += (targetX + shakeX - currentX) * damping;
    currentY += (targetY + idleY + shakeY - currentY) * damping;
    currentRot += (targetRot + idleRot + shakeRot - currentRot) * damping;

    // 3. Decay shake impulses
    shakeX *= shakeDamping;
    shakeY *= shakeDamping;
    shakeRot *= shakeDamping;

    // 4. Dynamic Physical Shadow (opposes direction & softens on rise)
    const shadowX = (-currentX * 0.45).toFixed(2);
    const shadowY = (3.5 - currentY * 0.35).toFixed(2);
    const shadowBlur = Math.max(3.5, 7.5 - currentY * 0.45).toFixed(2);
    const shadowAlpha = clamp(0.065 + currentY * 0.004, 0.03, 0.12).toFixed(3);
    const glowAlpha = clamp(0.18 - currentY * 0.012, 0.08, 0.28).toFixed(3);

    // Apply transform & lighting
    logoWrap.style.transform = `translate3d(${currentX.toFixed(2)}px, ${currentY.toFixed(2)}px, 0) rotate(${currentRot.toFixed(2)}deg)`;
    logoWrap.style.filter = `drop-shadow(${shadowX}px ${shadowY}px ${shadowBlur}px rgba(15, 23, 42, ${shadowAlpha})) drop-shadow(0 2px 7px rgba(13, 148, 136, ${glowAlpha}))`;

    requestAnimationFrame(updatePhysics);
  };

  // Start loop after entrance animation settles (~650ms)
  setTimeout(() => {
    requestAnimationFrame(updatePhysics);
  }, 650);

  // ------------------------------------------------------------
  // Mobile Device Orientation (Tilt Response)
  // ------------------------------------------------------------
  const handleOrientation = (e) => {
    if (e.gamma === null || e.beta === null) return;
    hasSensorData = true;

    // Gamma: Left / Right tilt (-90 to +90). Typical phone hold: -30 to +30
    // Map to ±14px max movement with smooth scaling
    const rawGamma = clamp(e.gamma, -45, 45);
    targetX = (rawGamma / 45) * 14;

    // Beta: Front / Back tilt (-180 to +180). Typical reading angle: 40° to 55°
    // Center at 45° resting tilt
    const rawBeta = clamp(e.beta - 45, -35, 35);
    targetY = (rawBeta / 35) * 6;

    // Subtle rotational inertia with tilt
    targetRot = (rawGamma / 45) * 1.2;
  };

  // ------------------------------------------------------------
  // Mobile Device Motion (Physical Shake Response)
  // ------------------------------------------------------------
  const handleMotion = (e) => {
    const acc = e.accelerationIncludingGravity || e.acceleration;
    if (!acc || acc.x === null) return;

    const deltaX = Math.abs(acc.x - lastAcc.x);
    const deltaY = Math.abs(acc.y - lastAcc.y);
    const deltaZ = Math.abs(acc.z - lastAcc.z);
    lastAcc = { x: acc.x, y: acc.y, z: acc.z };

    const totalDelta = deltaX + deltaY + deltaZ;
    const now = performance.now();

    // Significant shake threshold with 1.0s cooldown
    if (totalDelta > 24 && (now - lastShakeTime > 1000)) {
      lastShakeTime = now;
      const dir = Math.random() > 0.5 ? 1 : -1;
      shakeX = dir * (6 + Math.random() * 4);
      shakeY = (Math.random() - 0.5) * 6;
      shakeRot = dir * (2.5 + Math.random() * 2);
    }
  };

  // ------------------------------------------------------------
  // Sensor Initialization & iOS Permission Handling
  // ------------------------------------------------------------
  let sensorsInitialized = false;
  const initSensors = async () => {
    if (sensorsInitialized) return;
    sensorsInitialized = true;

    if (typeof DeviceOrientationEvent !== 'undefined' && typeof DeviceOrientationEvent.requestPermission === 'function') {
      try {
        const response = await DeviceOrientationEvent.requestPermission();
        if (response === 'granted') {
          window.addEventListener('deviceorientation', handleOrientation, { passive: true });
          window.addEventListener('devicemotion', handleMotion, { passive: true });
        }
      } catch (_) {
        // Fallback gracefully without throwing
      }
    } else if (window.DeviceOrientationEvent) {
      window.addEventListener('deviceorientation', handleOrientation, { passive: true });
      window.addEventListener('devicemotion', handleMotion, { passive: true });
    }
  };

  // Standard orientation listener for Android / non-permission browsers
  if (window.DeviceOrientationEvent && typeof DeviceOrientationEvent.requestPermission !== 'function') {
    initSensors();
  }

  // iOS 13+ requires user gesture
  window.addEventListener('touchstart', initSensors, { once: true, passive: true });
  window.addEventListener('click', initSensors, { once: true, passive: true });

  // ------------------------------------------------------------
  // Desktop Pointer Fallback (Magnetic Header Parallax)
  // ------------------------------------------------------------
  const header = document.querySelector('header');
  if (header) {
    const handlePointerMove = (e) => {
      if (hasSensorData) return; // Don't conflict with mobile sensor
      const rect = header.getBoundingClientRect();
      const relX = clamp((e.clientX - (rect.left + rect.width / 2)) / (rect.width / 2), -1, 1);
      const relY = clamp((e.clientY - (rect.top + rect.height / 2)) / (rect.height / 2), -1, 1);

      targetX = relX * 9;
      targetY = relY * 4;
      targetRot = relX * 0.75;
    };

    const handlePointerLeave = () => {
      if (hasSensorData) return;
      targetX = 0;
      targetY = 0;
      targetRot = 0;
    };

    header.addEventListener('mousemove', handlePointerMove, { passive: true });
    header.addEventListener('mouseleave', handlePointerLeave, { passive: true });
  }
});
