# Examstash

> Previous-year question papers and study resources, organized in one place.

* **Live Website:** [https://examstash.pages.dev](https://examstash.pages.dev)
* **GitHub Repository:** [https://github.com/sahilsleem/Examstash](https://github.com/sahilsleem/Examstash)

Examstash is a fast, clean, and distraction-free web platform where school and college students can find previous-year board exam papers, university semester papers, and syllabus material without dealing with spam, mandatory logins, or broken download links.

---

## Why I Built This

I built Examstash with a simple idea: finding previous-year papers shouldn't be harder than studying for the exam itself.

During exam preparation, students often spend hours digging through random websites, dead links, shady redirect ads, and cluttered WhatsApp groups just to find a single question paper. Most existing sites are filled with aggressive popups or require creating an account before downloading anything.

Examstash solves that by organizing all question papers and syllabi into a clean, searchable hierarchy where everything is 100% free and accessible in one click.

---

## What Examstash Does

* **Previous-Year Question Papers:** Direct access to past exam papers with clean PDF downloads.
* **In-Browser PDF Previews:** Preview question papers in a popup reader directly on the site before downloading.
* **Instant Autocomplete Search:** Fast search across boards, classes, courses, and subjects with keyboard navigation (`Ctrl + K` or `/` shortcut).
* **Saved Papers (Offline Bookmarks):** Save papers to your browser storage and view them anytime in a slide-over drawer.
* **Classroom Sharing:** 1-tap WhatsApp and Telegram share buttons to send papers directly to study groups and classmates.
* **"Request a Paper" Flow:** An interactive form that lets students request missing papers via Telegram (`@sahilsleem`) or Email.
* **Progressive Web App (PWA):** Installable on Android and iOS devices with offline asset caching and a sticky mobile bottom navigation bar.
* **Responsive Layout:** Optimized for mobile phones, tablets, and desktop screens.
* **Zero Pop-Ups & No Login:** Every document is directly viewable and downloadable without signing up.

---

## Academic Organization

The website is structured logically to mirror how academic boards and universities organize their curriculum:

```text
School Boards (JKBOSE, CBSE, ICSE)
└── Classes (Class 10, Class 12)
    └── Streams & Subjects (Science, Commerce, Arts, Vocational)
        └── Years & Series (e.g. 2026 Series A, B, C / 2023)
            └── Direct PDF Download & Online Preview

Colleges & Universities (Islamia College, Kashmir University)
└── Degree Programs (BCA, BBA, B.Com, B.A, B.Sc IT, MBA)
    └── Semesters (Semester 1 to 6)
        └── Subjects & Syllabus
```

---

## Current Coverage

### School Boards
* **JKBOSE:**
  * **Class 10:** Mathematics (2023, 2026 Series A/B/C), Science (2026 Series A/B), English (2026 Series C), Social Science (2026 Series A), Hindi, Urdu.
  * **Class 12:** Science (Physics, Chemistry, Biology, Maths, Computer Science, Biotechnology, etc.), Commerce (Accountancy, Business Studies, Economics, etc.), Arts (History, Political Science, Economics, Sociology, etc.), Home Science, Vocational streams, and Open School.
* **CBSE:** Class 10 & Class 12 portals.
* **ICSE:** Class 10 & Class 12 portals.

### Colleges & Universities
* **Islamia College of Science & Commerce (ICSC):**
  * BCA (Semesters 1–6)
  * BBA (Semesters 1–6)
  * B.Com (Semesters 1–6)
  * B.A (Semesters 1–6)
  * B.Sc IT (Semesters 1–6)
  * MBA (Semesters 1–4)
* **University Portals:** Kashmir University, Cluster University, BGSBU.
* **Competitive Exams:** NEET, JEE Main, CUET, JKPSC.

---

## Tech Stack

Examstash is intentionally built with vanilla web technologies and lightweight static generation for maximum speed and zero bloat:

* **Frontend:** Vanilla HTML5, Modern CSS3 (Grid, Flexbox, custom properties), ES6+ JavaScript.
* **Offline & PWA:** Service Worker (`sw.js`), Web App Manifest (`manifest.json`), LocalStorage API.
* **Static Generation & CLI:** Python 3 (`generate.py`, `generate_sitemap.py`, `validate_site.py`, `add_paper.py`).
* **Storage & Embeds:** Google Drive Cloud Storage (stream embeds & direct downloads).
* **Hosting & CDN:** Cloudflare Pages with edge caching headers (`_headers`).
* **CI/CD:** GitHub Actions workflow for automated link verification and sitemap generation.

---

## Project Structure

```text
Examstash/
├── index.html              # Homepage with tabs & search
├── manifest.json           # PWA Web App Manifest
├── sw.js                   # Service Worker for offline caching
├── robots.txt              # Search engine crawler rules
├── sitemap.xml             # Auto-generated XML sitemap
├── _headers                # Cloudflare Pages edge cache rules
│
├── assets/
│   ├── css/
│   │   └── global.css      # Design system, modals, bookmarks, PWA styles
│   ├── js/
│   │   ├── search.js       # Search autocomplete controller & keyboard shortcuts
│   │   ├── search-index.js # In-memory search database
│   │   ├── bookmarks.js    # Saved papers drawer & localStorage manager
│   │   ├── pwa.js          # Service worker registration & mobile navigation
│   │   ├── request-paper.js# Interactive paper request modal
│   │   └── analytics.js    # Engagement event tracker
│   ├── icons/              # Vector PWA icons
│   └── images/             # Social sharing preview cards (1200x630)
│
├── jkbose/                 # JKBOSE board paper hierarchies
├── cbse/                   # CBSE board paper hierarchies
├── icse/                   # ICSE board paper hierarchies
├── islamia-college/        # Islamia College degree & semester pages
├── kashmir-university/     # Kashmir University section
│
├── add_paper.py            # CLI tool to ingest new question papers
├── generate.py             # Paper page compiler & recommendation engine
├── generate_sitemap.py     # XML sitemap generator
└── validate_site.py        # Automated link & asset integrity checker
```

---

## Local Development

No heavy build tools or npm dependencies are required. You only need Python 3 installed.

### 1. Clone the repository
```bash
git clone https://github.com/sahilsleem/Examstash.git
cd Examstash
```

### 2. Start a local server
```bash
python -m http.server 8000
```
Open **[http://localhost:8000](http://localhost:8000)** in your browser.

---

## Helper Scripts

### Adding a New Question Paper
Run the interactive CLI tool:
```bash
python add_paper.py
```
Or pass arguments directly:
```bash
python add_paper.py --board jkbose --class class-10 --subject maths --year 2026 --series a --drive-id <GOOGLE_DRIVE_FILE_ID>
```
*This updates `generate.py`, compiles the HTML page, adds the paper to the search index, and refreshes `sitemap.xml` automatically.*

### Validating Site Health
Crawl all internal links and asset references to ensure zero broken links:
```bash
python validate_site.py
```

### Rebuilding Pages & Sitemap
```bash
python generate.py
python generate_sitemap.py
```

---

## Contributing

If you have question papers or syllabi from your school, college, or university:

1. **Send papers directly:**
   * Telegram: **[@sahilsleem](https://t.me/sahilsleem)**
   * Email: **`examstash1@gmail.com`**
2. **Submit via GitHub:**
   * Fork the repository, use `python add_paper.py` to add your paper, and open a Pull Request.

---

## License

This project is open-source under the [MIT License](LICENSE).
