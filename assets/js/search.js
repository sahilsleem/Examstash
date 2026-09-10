/**
 * ExamStash Global Search & Autocomplete
 */

(function () {
  // Global Shortcut: Ctrl+K or / to focus search
  window.addEventListener('keydown', (e) => {
    if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'k') {
      e.preventDefault();
      focusSearch();
    } else if (e.key === '/' && !['INPUT', 'TEXTAREA'].includes(document.activeElement?.tagName)) {
      e.preventDefault();
      focusSearch();
    }
  });

  function focusSearch() {
    const input = document.querySelector('#site-search-input, .search-container input, .search-wrap input');
    if (input) {
      input.scrollIntoView({ behavior: 'smooth', block: 'center' });
      setTimeout(() => input.focus(), 150);
    }
  }

  document.addEventListener('DOMContentLoaded', () => {
    const searchInputs = document.querySelectorAll('#site-search-input, .search-container input, .search-wrap input');
    if (!searchInputs.length) return;

    searchInputs.forEach(input => {
      setupAutocomplete(input);
    });
  });

  function setupAutocomplete(input) {
    const wrapper = input.closest('.search-container, .search-wrap') || input.parentElement;
    if (!wrapper) return;

    // Wrap in relative container if needed
    let parent = wrapper.parentElement;
    if (!parent.classList.contains('search-wrapper-relative')) {
      const container = document.createElement('div');
      container.className = 'search-wrapper-relative';
      parent.insertBefore(container, wrapper);
      container.appendChild(wrapper);
      parent = container;
    }

    // Create dropdown container
    const dropdown = document.createElement('div');
    dropdown.className = 'search-dropdown';
    parent.appendChild(dropdown);

    let focusedIndex = -1;
    let currentResults = [];

    function search(query) {
      if (!window.EXAMSTASH_SEARCH_INDEX) return [];
      const clean = query.toLowerCase().trim();
      if (!clean) return [];

      const terms = clean.split(/\s+/).filter(Boolean);

      return window.EXAMSTASH_SEARCH_INDEX.filter(item => {
        const titleMatch = terms.every(t => item.title.toLowerCase().includes(t));
        const tagMatch = item.tags && item.tags.some(tag => terms.some(t => tag.includes(t)));
        const catMatch = item.category.toLowerCase().includes(clean);
        return titleMatch || tagMatch || catMatch;
      }).slice(0, 8); // Top 8 matches
    }

    function renderDropdown(results, query) {
      currentResults = results;
      focusedIndex = -1;

      if (!results.length) {
        dropdown.innerHTML = `
          <div class="search-no-results">
            No papers or sections found for "<strong>${escapeHtml(query)}</strong>"
          </div>
        `;
        dropdown.classList.add('active');
        return;
      }

      // Group by category
      const groups = {};
      results.forEach(r => {
        if (!groups[r.category]) groups[r.category] = [];
        groups[r.category].push(r);
      });

      let html = '';
      let itemIdx = 0;

      for (const [category, items] of Object.entries(groups)) {
        html += `<div class="search-category-group">`;
        html += `<div class="search-category-header">${escapeHtml(category)}</div>`;
        items.forEach(item => {
          html += `
            <a href="${item.url}" class="search-item" data-index="${itemIdx}">
              <span class="search-item-icon">${item.icon || '📄'}</span>
              <div class="search-item-info">
                <div class="search-item-title">${highlightMatch(item.title, query)}</div>
                <div class="search-item-subtitle">${item.tags ? item.tags.slice(0, 4).join(' • ') : ''}</div>
              </div>
            </a>
          `;
          itemIdx++;
        });
        html += `</div>`;
      }

      dropdown.innerHTML = html;
      dropdown.classList.add('active');

      dropdown.querySelectorAll('.search-item').forEach(el => {
        el.addEventListener('mouseenter', () => {
          dropdown.querySelectorAll('.search-item').forEach(i => i.classList.remove('focused'));
          el.classList.add('focused');
          focusedIndex = parseInt(el.getAttribute('data-index'), 10);
        });
      });
    }

    function hideDropdown() {
      dropdown.classList.remove('active');
      focusedIndex = -1;
    }

    function highlightMatch(text, query) {
      if (!query.trim()) return escapeHtml(text);
      const terms = query.trim().split(/\s+/).filter(Boolean);
      let pattern = terms.map(t => escapeRegExp(t)).join('|');
      const regex = new RegExp(`(${pattern})`, 'gi');
      return escapeHtml(text).replace(regex, '<strong style="color: var(--accent-teal); font-weight:700;">$1</strong>');
    }

    function escapeHtml(str) {
      return (str || '').replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
    }

    function escapeRegExp(str) {
      return str.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
    }

    // Event listeners
    input.addEventListener('input', () => {
      const q = input.value.trim();
      if (q.length > 0) {
        const results = search(q);
        renderDropdown(results, q);
      } else {
        hideDropdown();
      }
    });

    input.addEventListener('keydown', (e) => {
      const items = dropdown.querySelectorAll('.search-item');
      if (!dropdown.classList.contains('active') || !items.length) {
        if (e.key === 'Enter') {
          // If enter pressed and has query
          const q = input.value.trim();
          if (q) {
            const results = search(q);
            if (results.length > 0) {
              window.location.href = results[0].url;
            }
          }
        }
        return;
      }

      if (e.key === 'ArrowDown') {
        e.preventDefault();
        focusedIndex = (focusedIndex + 1) % items.length;
        updateFocus(items);
      } else if (e.key === 'ArrowUp') {
        e.preventDefault();
        focusedIndex = (focusedIndex - 1 + items.length) % items.length;
        updateFocus(items);
      } else if (e.key === 'Enter') {
        e.preventDefault();
        if (focusedIndex >= 0 && focusedIndex < items.length) {
          items[focusedIndex].click();
        } else if (currentResults.length > 0) {
          window.location.href = currentResults[0].url;
        }
      } else if (e.key === 'Escape') {
        hideDropdown();
      }
    });

    function updateFocus(items) {
      items.forEach((item, idx) => {
        if (idx === focusedIndex) {
          item.classList.add('focused');
          item.scrollIntoView({ block: 'nearest' });
        } else {
          item.classList.remove('focused');
        }
      });
    }

    // Close on click outside
    document.addEventListener('click', (e) => {
      if (!parent.contains(e.target)) {
        hideDropdown();
      }
    });

    input.addEventListener('focus', () => {
      const q = input.value.trim();
      if (q.length > 0) {
        const results = search(q);
        renderDropdown(results, q);
      }
    });
  }
})();
