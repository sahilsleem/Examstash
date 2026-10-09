# ExamStash

> Academic archive providing free past semester question papers and syllabus resources for undergraduate degree programs at Islamia College of Science & Commerce (ICSC Srinagar).

[![Site Health](https://img.shields.io/badge/Site%20Health-Passing%20(408%20Pages)-0d9488?style=flat-square)](https://examstash.online)
[![License: MIT](https://img.shields.io/badge/License-MIT-slate?style=flat-square)](LICENSE)
[![PWA Ready](https://img.shields.io/badge/PWA-Installable%20%26%20Offline-teal?style=flat-square)](https://examstash.online)

---

## 🌐 Live Website

**[https://examstash.online](https://examstash.online)**

---

## 📖 What is ExamStash?

**ExamStash** is an open, student-built academic resource designed to simplify exam preparation. Instead of searching through fragmented group chats, dead file-storage links, or cluttered portals, ExamStash offers direct, structured, and free access to previous year question papers and syllabus resources.

The collection is primarily tailored for students enrolled in undergraduate degree programs under the National Education Policy (NEP 2020) and CBCS curricula at **Islamia College of Science & Commerce, Srinagar (ICSC)**.

---

## 📚 Available Programs & Streams

ExamStash organizes educational materials across major undergraduate degree streams and all semesters:

* **Common Courses (NEP 2020)**: Multidisciplinary (MDC), Skill Enhancement (SEC), Value-Added (VAC), and Ability Enhancement (AEC) subjects for Semesters 1, 2, and 3 across all degree streams.
* **Computer Applications & IT**:
  * **BCA** (Bachelor of Computer Applications): Problem Solving through C, Data Structures, Database Management Systems, Discrete Mathematics, etc.
  * **B.Sc. IT** (Information Technology): Computer Architecture, Object-Oriented Programming, Data Communications, etc.
* **Business & Commerce**:
  * **BBA** (Bachelor of Business Administration): Principles of Management, Financial Accounting, Marketing Management, Public Finance, etc.
  * **B.Com & B.Com Honours**: Financial Accounting, Business Law, Company Law, Banking & Insurance, Cost Accounting, etc.
* **Arts & Humanities**:
  * **B.A. & English Honours**: Introductory Microeconomics, History of English Literature, Political Theory, Linguistics, Short Stories across Cultures, Kashmiri Literature, etc.
* **Science Disciplines (B.Sc.)**:
  * **B.Sc. Botany**: Biodiversity, Anatomy of Angiosperms, Morphology.
  * **B.Sc. Zoology**: Diversity of Non-Chordates, Diversity of Chordates.
  * **B.Sc. Biotechnology**: Biomolecules, Structure and Function, Cell Biology.
  * **B.Sc. Chemistry, Physics, Mathematics & Biochemistry**.

---

## ⚡ Features

* **🔍 Real-Time Search & Autocomplete**: In-memory client-side search indexed across 100+ subject resources with instant keyboard shortcut access (`/` or `Ctrl+K`), keyword highlighting, and arrow-key navigation.
* **⚡ Direct PDF Access**: One-click download links pointing directly to Google Drive document storage without registration, link-shorteners, or paywalls.
* **📱 Progressive Web App (PWA)**: Installable on Android, iOS, Windows, and macOS with service-worker caching (`sw.js`) for reliable offline review.
* **🎨 Responsive Design System**: Lightweight, typography-driven UI built with semantic HTML5, custom CSS design tokens, and smooth entrance transitions.
* **🛡️ SEO & Web Standards**: Full Schema.org JSON-LD structured data on all pages, Open Graph previews, XML sitemap (`sitemap.xml`), and Cloudflare cache headers (`_headers`).
* **⚖️ Legal & Policy Pages**: Comprehensive About (`/about/`), Contact (`/contact/`), Privacy Policy (`/privacy/`), Terms of Use (`/terms/`), and DMCA / Copyright (`/dmca/`) notices.

---

## 📁 Repository Structure

```text
Examstash/
├── index.html               # Main homepage & degree stream directory
├── 404.html                 # Custom responsive 404 error page
├── CNAME                    # Custom domain deployment configuration
├── _headers                 # Cloudflare Pages caching & security headers
├── manifest.json            # Web App Manifest for PWA installation
├── sw.js                    # Service worker for offline shell caching
├── sitemap.xml              # XML sitemap for search engine crawlers
├── robots.txt               # Robot crawler directives
├── assets/
│   ├── css/                 # Global styles, typography & motion tokens
│   ├── js/                  # Search engine, autocomplete, PWA & motion handlers
│   ├── icons/               # SVG & PWA application icons
│   └── images/              # Open Graph social preview banners
├── common-courses/          # Multidisciplinary & Skill course directories
├── bca/                     # BCA semester & subject download pages
├── bsc-it/                  # B.Sc. IT semester & subject download pages
├── bba/                     # BBA semester & subject download pages
├── bcom/                    # B.Com semester & subject download pages
├── ba/                      # B.A. & English Honours download pages
├── bsc-*/                   # Science stream semester download directories
├── about/                   # About ExamStash page
├── contact/                 # Contact & feedback page
├── privacy/                 # Privacy policy
├── terms/                   # Terms of service
├── dmca/                    # Copyright & DMCA takedown policy
├── validate_site.py         # Automated link health & asset verification scanner
├── generate_sitemap.py      # Sitemap generator script
├── rebuild_search.py        # Search index compiler
├── quick_add.py             # CLI utility for adding new paper pages
└── CONTRIBUTING.md          # Guide for contributing question papers
```

---

## 💻 Running Locally

ExamStash is built entirely with vanilla web standards (HTML5, CSS3, ES6 JavaScript) and requires no build pipeline or node package installations.

1. **Clone the repository**:
   ```bash
   git clone https://github.com/sahilsleem/Examstash.git
   cd Examstash
   ```

2. **Serve the directory with any local static server**:
   ```bash
   # Using Python 3
   python -m http.server 8080

   # Or using Node.js npx serve
   npx serve .
   ```

3. **Open in your browser**:
   ```text
   http://localhost:8080
   ```

---

## 🛠️ Maintenance & Automation Scripts

The repository includes a suite of Python utilities to keep links, search indices, and sitemaps verified:

* **Site Health & Link Integrity Validator**:
  ```bash
  python validate_site.py
  ```
  Scans all 400+ HTML files to verify that every internal link, static asset reference, and Google Drive identifier is valid.

* **Rebuild Search Index**:
  ```bash
  python rebuild_search.py
  ```
  Parses all subject pages to update `assets/js/search-index.js`.

* **Generate Sitemap**:
  ```bash
  python generate_sitemap.py
  ```
  Traverses the directory structure and outputs an updated `sitemap.xml`.

* **Quick Add Paper**:
  ```bash
  python quick_add.py
  ```
  Interactive CLI to scaffold a new subject page, link it into the corresponding semester index, and update the search index.

---

## ⚖️ Content Notice & Disclaimer

ExamStash is an independent student educational resource and is **not affiliated with, endorsed by, or an official website of Islamia College of Science and Commerce, Srinagar**. All college names, course titles, degree abbreviations, and syllabi materials are referenced strictly for educational, informational, and identification purposes.

If you are a copyright holder and wish to request the modification or removal of any document, please review our [DMCA & Copyright Policy](https://examstash.online/dmca/) or contact `examstash1@gmail.com`.

---

## 🤝 Contributing

Contributions of past question papers and syllabi are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for instructions on submitting clear scans or adding new paper entries via pull requests.

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

## 👤 Built By

**Sahil Saleem**
* GitHub: [@sahilsleem](https://github.com/sahilsleem)
* Telegram: [@sahilsleem](https://t.me/sahilsleem)
