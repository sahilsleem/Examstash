/**
 * ExamStash "Request a Paper" & Contribution Controller
 * Self-contained styles and modal logic to prevent unstyled flash
 */

(function () {
  function ensureStyles() {
    if (document.getElementById('examstash-request-style')) return;
    const style = document.createElement('style');
    style.id = 'examstash-request-style';
    style.textContent = `
      .request-modal {
        position: fixed !important;
        inset: 0 !important;
        background: rgba(0, 0, 0, 0.5) !important;
        backdrop-filter: blur(6px) !important;
        z-index: 100000 !important;
        display: none;
        align-items: center !important;
        justify-content: center !important;
        padding: 16px !important;
        font-family: 'Segoe UI', system-ui, -apple-system, sans-serif !important;
      }
      .request-modal.open {
        display: flex !important;
      }
      .request-modal-container {
        background: #ffffff !important;
        width: 100% !important;
        max-width: 500px !important;
        border-radius: 20px !important;
        border: 1.5px solid #f0f0f0 !important;
        box-shadow: 0 20px 45px rgba(0, 0, 0, 0.15) !important;
        overflow: hidden !important;
        display: flex !important;
        flex-direction: column !important;
        animation: reqModalIn 0.2s cubic-bezier(0.16, 1, 0.3, 1) !important;
      }
      @keyframes reqModalIn {
        from { transform: scale(0.95); opacity: 0; }
        to { transform: scale(1); opacity: 1; }
      }
      .request-modal-header {
        padding: 22px 24px 16px !important;
        border-bottom: 1px solid #f0f0f0 !important;
        display: flex !important;
        align-items: flex-start !important;
        justify-content: space-between !important;
        background: #ffffff !important;
      }
      .req-tag {
        display: inline-block !important;
        background: #f0fdfa !important;
        color: #0d9488 !important;
        font-size: 11px !important;
        font-weight: 700 !important;
        padding: 3px 10px !important;
        border-radius: 20px !important;
        margin-bottom: 8px !important;
        letter-spacing: 0.04em !important;
      }
      .req-title {
        font-size: 22px !important;
        font-weight: 800 !important;
        color: #0f0f0f !important;
        letter-spacing: -0.5px !important;
        line-height: 1.2 !important;
        margin: 0 0 4px 0 !important;
      }
      .req-title span { color: #0d9488 !important; }
      .req-desc {
        font-size: 13px !important;
        color: #666666 !important;
        line-height: 1.4 !important;
        margin: 0 !important;
      }
      .request-modal-close {
        background: #f5f5f5 !important;
        border: 1px solid #e8e8e8 !important;
        width: 32px !important;
        height: 32px !important;
        border-radius: 50% !important;
        font-size: 18px !important;
        color: #777 !important;
        cursor: pointer !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        line-height: 1 !important;
        transition: all 0.15s !important;
        flex-shrink: 0 !important;
        margin-left: 12px !important;
      }
      .request-modal-close:hover {
        background: #f0fdfa !important;
        border-color: #0d9488 !important;
        color: #0d9488 !important;
      }
      .request-modal-body {
        padding: 20px 24px !important;
        display: flex !important;
        flex-direction: column !important;
        gap: 12px !important;
        overflow-y: auto !important;
        max-height: 75vh !important;
        background: #ffffff !important;
      }
      .req-form-group {
        display: flex !important;
        flex-direction: column !important;
        gap: 5px !important;
        text-align: left !important;
      }
      .req-form-group label {
        font-size: 13px !important;
        font-weight: 600 !important;
        color: #1a1a1a !important;
      }
      .req-form-group input, .req-form-group textarea {
        background: #f5f5f5 !important;
        border: 1.5px solid #e8e8e8 !important;
        border-radius: 12px !important;
        font-size: 14px !important;
        color: #1a1a1a !important;
        padding: 10px 14px !important;
        outline: none !important;
        font-family: inherit !important;
        transition: all 0.2s !important;
        box-sizing: border-box !important;
        width: 100% !important;
      }
      .req-form-group input:focus, .req-form-group textarea:focus {
        border-color: #0d9488 !important;
        background: #ffffff !important;
      }
      .req-form-group input::placeholder, .req-form-group textarea::placeholder {
        color: #999999 !important;
      }
      .req-form-row {
        display: grid !important;
        grid-template-columns: 1fr 1fr !important;
        gap: 12px !important;
      }
      @media (max-width: 480px) {
        .req-form-row { grid-template-columns: 1fr !important; }
      }
      .req-contrib-tip {
        background: #f0fdfa !important;
        border: 1.5px solid #ccfbf1 !important;
        border-radius: 12px !important;
        padding: 10px 14px !important;
        font-size: 12px !important;
        color: #0d9488 !important;
        line-height: 1.5 !important;
      }
      .req-actions-row {
        display: flex !important;
        gap: 8px !important;
        margin-top: 4px !important;
        flex-wrap: wrap !important;
      }
      .btn-req-tg {
        flex: 1.2 !important;
        min-width: 150px !important;
        display: inline-flex !important;
        align-items: center !important;
        justify-content: center !important;
        gap: 8px !important;
        background: #0088cc !important;
        color: #ffffff !important;
        border: none !important;
        padding: 12px 18px !important;
        border-radius: 10px !important;
        font-size: 14px !important;
        font-weight: 600 !important;
        cursor: pointer !important;
        transition: background 0.15s !important;
        font-family: inherit !important;
      }
      .btn-req-tg:hover { background: #0077b5 !important; }
      .btn-req-email {
        flex: 1.2 !important;
        min-width: 140px !important;
        display: inline-flex !important;
        align-items: center !important;
        justify-content: center !important;
        gap: 8px !important;
        background: #0d9488 !important;
        color: #ffffff !important;
        border: none !important;
        padding: 12px 18px !important;
        border-radius: 10px !important;
        font-size: 14px !important;
        font-weight: 600 !important;
        cursor: pointer !important;
        transition: background 0.15s !important;
        font-family: inherit !important;
      }
      .btn-req-email:hover { background: #0f766e !important; }
      .btn-req-copy {
        display: inline-flex !important;
        align-items: center !important;
        justify-content: center !important;
        gap: 6px !important;
        background: #ffffff !important;
        color: #555555 !important;
        border: 1.5px solid #e8e8e8 !important;
        padding: 12px 16px !important;
        border-radius: 10px !important;
        font-size: 14px !important;
        font-weight: 600 !important;
        cursor: pointer !important;
        transition: all 0.15s !important;
        font-family: inherit !important;
      }
      .btn-req-copy:hover {
        border-color: #0d9488 !important;
        color: #0d9488 !important;
      }
      .req-feedback-msg {
        display: none;
        font-size: 13px !important;
        font-weight: 600 !important;
        text-align: center !important;
        padding: 4px 0 !important;
      }
    `;
    document.head.appendChild(style);
  }

  function ensureModalInDOM() {
    ensureStyles();
    if (document.getElementById('examstash-request-modal')) return;

    const modalHTML = `
      <div id="examstash-request-modal" class="request-modal" style="display: none;">
        <div class="request-modal-container">
          <div class="request-modal-header">
            <div class="request-header-content">
              <span class="req-tag">📩 FREE REQUEST</span>
              <h2 class="req-title">Request a <span>Paper</span></h2>
              <p class="req-desc">Can't find your exam paper? Tell us what you need and we'll track it down.</p>
            </div>
            <button type="button" class="request-modal-close" id="btn-request-close" aria-label="Close modal">&times;</button>
          </div>
          
          <form class="request-modal-body" id="paper-request-form">
            <div class="req-form-group">
              <label for="req-board">Board / University / College <span style="color: #ea580c;">*</span></label>
              <input type="text" id="req-board" placeholder="e.g. JKBOSE, Islamia College, CBSE, Kashmir University" required />
            </div>

            <div class="req-form-row">
              <div class="req-form-group">
                <label for="req-class">Class / Course / Sem <span style="color: #ea580c;">*</span></label>
                <input type="text" id="req-class" placeholder="e.g. Class 10, BCA 3rd Sem" required />
              </div>
              <div class="req-form-group">
                <label for="req-year">Year / Series</label>
                <input type="text" id="req-year" placeholder="e.g. 2025, 2024, Series A" />
              </div>
            </div>

            <div class="req-form-group">
              <label for="req-subject">Subject Name <span style="color: #ea580c;">*</span></label>
              <input type="text" id="req-subject" placeholder="e.g. Mathematics, Science, English" required />
            </div>

            <div class="req-form-group">
              <label for="req-notes">Additional Details (Optional)</label>
              <textarea id="req-notes" rows="2" placeholder="Any specific requirements or comments..."></textarea>
            </div>

            <div class="req-contrib-tip">
              💡 <strong>Have past papers with you?</strong> You can also send question paper photos/PDFs on Telegram to help fellow students!
            </div>

            <div class="req-actions-row">
              <button type="button" class="btn-req-tg" id="btn-send-telegram">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm4.64 6.8c-.15 1.58-.8 5.42-1.13 7.19-.14.75-.42 1-.68 1.03-.58.05-1.02-.38-1.58-.75-.88-.58-1.38-.94-2.23-1.5-.99-.65-.35-1.01.22-1.59.15-.15 2.71-2.48 2.76-2.69a.2.2 0 00-.05-.18c-.06-.05-.14-.03-.21-.02-.09.02-1.49.95-4.22 2.79-.4.27-.76.41-1.08.4-.36-.01-1.04-.2-1.55-.37-.63-.2-1.12-.31-1.08-.66.02-.18.27-.36.74-.55 2.92-1.27 4.86-2.11 5.83-2.51 2.78-1.16 3.35-1.36 3.73-1.36.08 0 .27.02.39.12.1.08.13.19.14.27-.01.06.01.24 0 .37z"/></svg>
                Send on Telegram
              </button>
              <button type="button" class="btn-req-email" id="btn-send-email">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"></path><polyline points="22,6 12,13 2,6"></polyline></svg>
                Send via Email
              </button>
              <button type="button" class="btn-req-copy" id="btn-copy-req" title="Copy to Clipboard">
                📋 Copy
              </button>
            </div>
            <div id="request-feedback" class="req-feedback-msg"></div>
          </form>
        </div>
      </div>
    `;

    document.body.insertAdjacentHTML('beforeend', modalHTML);

    // Event handlers
    document.getElementById('btn-request-close').addEventListener('click', closeModal);
    document.getElementById('examstash-request-modal').addEventListener('click', (e) => {
      if (e.target === document.getElementById('examstash-request-modal')) {
        closeModal();
      }
    });

    document.getElementById('btn-send-telegram').addEventListener('click', () => dispatch('telegram'));
    document.getElementById('btn-send-email').addEventListener('click', () => dispatch('email'));
    document.getElementById('btn-copy-req').addEventListener('click', () => dispatch('copy'));
  }

  function openModal(defaultBoard = '', defaultClass = '') {
    ensureModalInDOM();
    if (defaultBoard) document.getElementById('req-board').value = defaultBoard;
    if (defaultClass) document.getElementById('req-class').value = defaultClass;
    
    const modal = document.getElementById('examstash-request-modal');
    modal.style.display = 'flex';
    modal.classList.add('open');
    document.body.style.overflow = 'hidden';
    setTimeout(() => document.getElementById('req-board').focus(), 100);
  }

  function closeModal() {
    const modal = document.getElementById('examstash-request-modal');
    if (modal) {
      modal.style.display = 'none';
      modal.classList.remove('open');
    }
    document.body.style.overflow = '';
  }

  function getFormData() {
    const board = document.getElementById('req-board').value.trim();
    const cls = document.getElementById('req-class').value.trim();
    const subject = document.getElementById('req-subject').value.trim();
    const year = document.getElementById('req-year').value.trim();
    const notes = document.getElementById('req-notes').value.trim();

    if (!board || !cls || !subject) {
      showFeedback('Please fill in Board, Class/Course, and Subject name.', true);
      return null;
    }

    return { board, cls, subject, year, notes };
  }

  function formatMessage(data) {
    let msg = `📚 ExamStash Paper Request\n\n`;
    msg += `🏛️ Board/College: ${data.board}\n`;
    msg += `🎓 Class/Course: ${data.cls}\n`;
    msg += `📝 Subject: ${data.subject}\n`;
    if (data.year) msg += `📅 Year/Series: ${data.year}\n`;
    if (data.notes) msg += `💬 Notes: ${data.notes}\n`;
    msg += `\n🔗 Requested from: ${window.location.href}`;
    return msg;
  }

  function dispatch(target) {
    const data = getFormData();
    if (!data) return;

    const formattedText = formatMessage(data);

    if (target === 'telegram') {
      const tgUrl = `https://t.me/sahilsleem?text=${encodeURIComponent(formattedText)}`;
      window.open(tgUrl, '_blank', 'noopener');
      showFeedback('Opening Telegram...', false);
    } else if (target === 'email') {
      const subject = encodeURIComponent(`[Paper Request] ${data.board} ${data.cls} - ${data.subject}`);
      const body = encodeURIComponent(formattedText);
      const mailtoUrl = `mailto:examstash1@gmail.com?subject=${subject}&body=${body}`;
      window.location.href = mailtoUrl;
      showFeedback('Opening Email client...', false);
    } else if (target === 'copy') {
      if (navigator.clipboard) {
        navigator.clipboard.writeText(formattedText).then(() => {
          showFeedback('✅ Request details copied to clipboard!', false);
        });
      } else {
        showFeedback('✅ Ready to send!', false);
      }
    }
  }

  function showFeedback(text, isError) {
    const fb = document.getElementById('request-feedback');
    if (!fb) return;
    fb.textContent = text;
    fb.style.color = isError ? '#ef4444' : '#0d9488';
    fb.style.display = 'block';
  }

  window.ExamStashRequest = {
    open: openModal,
    close: closeModal
  };

  document.addEventListener('DOMContentLoaded', () => {
    ensureModalInDOM();

    document.querySelectorAll('.open-paper-request-btn, .cta-btn[href*="t.me"]').forEach(btn => {
      btn.addEventListener('click', (e) => {
        e.preventDefault();
        const board = btn.getAttribute('data-board') || '';
        const cls = btn.getAttribute('data-class') || '';
        openModal(board, cls);
      });
    });
  });
})();
