import os

# ============================================================
# PAPER LIST — this is the only thing you edit to add papers
# Format: (board, class, subject, year, pdf_link)
# For pdf_link put "#" for now, we'll replace with real links later
# ============================================================
papers = [
    # Format: (board, class, subject, year, series, pdf_link)
    # ONLY real papers with actual PDF/document links are listed here
    ("jkbose", "class-10", "maths",          "2023", None,  "https://drive.google.com/uc?export=download&id=17Qal9EEBuNvwWv67AtFT0dqjHMMClrXh"),
    ("jkbose", "class-10", "maths",          "2026", "a",   "https://drive.google.com/uc?export=download&id=1qNOaPNBuYvWbEV0ZTC61uzPCgMiDCBYQ"),
    ("jkbose", "class-10", "maths",          "2026", "b",   "https://drive.google.com/uc?export=download&id=1bawVt7btvOm36zbTPTXwdqZJuYyq62-S"),
    ("jkbose", "class-10", "maths",          "2026", "c",   "https://drive.google.com/uc?export=download&id=1J8rS3GcbXl3ffZF4V124fvRIniHcWibk"),
    ("jkbose", "class-10", "science",        "2026", "a",   "https://drive.google.com/uc?export=download&id=1Lfy6tjXrbE6nOPQwxdZcUgIEqO0JyTEx"),
    ("jkbose", "class-10", "science",        "2026", "b",   "https://drive.google.com/uc?export=download&id=1R_eBrcKJkyoKw5iQhx0zlHejHIOjqOHI"),
    ("jkbose", "class-10", "english",        "2026", "c",   "https://drive.google.com/uc?export=download&id=10KtHfQVSDcfXndQjgjXA-XbWdR5J9RBd"),
    ("jkbose", "class-10", "social-science", "2026", "a",   "https://drive.google.com/uc?export=download&id=1h9wv8YpX2MdSBP7jxupV3IgsztG0e4FB"),
]

# ============================================================
# DISPLAY NAMES — makes "social-science" show as "Social Science"
# ============================================================
subject_names = {
    "maths":          "Mathematics",
    "science":        "Science",
    "english":        "English",
    "social-science": "Social Science",
    "physics":        "Physics",
    "chemistry":      "Chemistry",
    "biology":        "Biology",
    "urdu":           "Urdu",
    "hindi":          "Hindi",
}

board_names = {
    "jkbose": "JKBOSE",
    "cbse":   "CBSE",
    "icse":   "ICSE",
}

class_names = {
    "class-10": "Class 10",
    "class-12": "Class 12",
}

subject_icons = {
    "maths":          "📐",
    "science":        "🔬",
    "english":        "📝",
    "social-science": "🌍",
    "physics":        "⚛️",
    "chemistry":      "🧪",
    "biology":        "🧬",
    "urdu":           "✒️",
    "hindi":          "🔤",
}

# ============================================================
# HTML TEMPLATE — this is what every paper page looks like
# ============================================================
def make_paper_page(board, cls, subject, year, series, pdf_link):
    if not pdf_link or pdf_link == "#":
        return None

    board_name   = board_names.get(board, board.upper())
    class_name   = class_names.get(cls, cls)
    subject_name = subject_names.get(subject, subject.title())
    icon         = subject_icons.get(subject, "📄")
    series_label = f" Series {series.upper()}" if series else ""
    series_pill  = f'<span class="pill pill-green">Series {series.upper()}</span>' if series else ""

    # Related papers - only link to real available papers
    same_subject = [(b, c, s, y, se, l) for b, c, s, y, se, l in papers 
                    if b == board and c == cls and s == subject and y != year and l and l != "#"]
    related_years_set = sorted(set(y for _, _, _, y, _, _ in same_subject), reverse=True)
    related_html = ""
    for ry in related_years_set:
        related_html += f"""
    <a href="/{board}/{cls}/{subject}/{ry}/" class="related-card">
      <div class="related-icon">📄</div>
      <div>
        <h4>{board_name} {class_name} {subject_name}</h4>
        <p>Annual Exam {ry}</p>
      </div>
    </a>"""

    if related_html:
        related_section = f"""
  <div class="related">
    <h2>Related Papers</h2>
    <div class="related-grid">{related_html}</div>
  </div>"""
    else:
        related_section = f"""
  <div class="related">
    <h2>More Papers</h2>
    <p style="color:#666; font-size:14px; margin-top:8px;">Looking for other subjects? <a href="/{board}/{cls}/" style="color:#0d9488; font-weight:600; text-decoration:none;">Browse all {board_name} {class_name} papers →</a></p>
  </div>"""

    # Download action button handling - MUST be a real link
    download_action = f"""<a href="{pdf_link}" class="download-btn" target="_blank" rel="noopener">⬇️ Download PDF — Free</a>"""
    download_status = "Free — Instant PDF Download"

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{board_name} {class_name} {subject_name} Question Paper {year}{series_label} PDF Download | ExamStash</title>
  <meta name="description" content="Download {board_name} {class_name} {subject_name} question paper {year}{series_label} PDF for free. Annual examination paper. No login required." />
  <style>
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    body {{ font-family: 'Segoe UI', system-ui, sans-serif; background: #fff; color: #1a1a1a; }}
    header {{
      padding: 14px 20px; border-bottom: 1px solid #f0f0f0;
      display: flex; align-items: center; justify-content: center;
      position: sticky; top: 0; background: #fff; z-index: 100;
    }}
    .logo {{ font-size: 22px; font-weight: 800; color: #1a1a1a; text-decoration: none; letter-spacing: -0.5px; }}
    .logo span {{ color: #0d9488; }}
    .breadcrumb {{ padding: 14px 20px; font-size: 13px; color: #999; max-width: 860px; margin: 0 auto; }}
    .breadcrumb a {{ color: #999; text-decoration: none; }}
    .breadcrumb a:hover {{ color: #0d9488; }}
    .breadcrumb span {{ margin: 0 6px; }}
    .container {{ max-width: 860px; margin: 0 auto; padding: 0 20px 60px; }}
    .paper-hero {{
      border: 1.5px solid #f0f0f0; border-radius: 16px;
      padding: 32px; margin-bottom: 24px;
      display: flex; gap: 24px; align-items: flex-start;
    }}
    .paper-thumb {{
      width: 90px; height: 120px; background: #f0fdfa;
      border-radius: 10px; display: flex; align-items: center;
      justify-content: center; font-size: 40px; flex-shrink: 0;
    }}
    .paper-info {{ flex: 1; }}
    .paper-info h1 {{ font-size: 22px; font-weight: 700; line-height: 1.3; margin-bottom: 10px; letter-spacing: -0.3px; }}
    .meta-row {{ display: flex; flex-wrap: wrap; gap: 8px; margin-bottom: 16px; }}
    .pill {{ font-size: 12px; font-weight: 600; padding: 4px 10px; border-radius: 20px; }}
    .pill-blue {{ background: #f0fdfa; color: #0d9488; }}
    .pill-green {{ background: #f0fdf4; color: #16a34a; }}
    .pill-orange {{ background: #fff7ed; color: #ea580c; }}
    .pill-purple {{ background: #faf5ff; color: #7c3aed; }}
    .download-btn {{
      display: inline-flex; align-items: center; gap: 8px;
      background: #0d9488; color: white; padding: 12px 24px;
      border-radius: 10px; font-size: 15px; font-weight: 600;
      text-decoration: none; transition: background 0.2s;
    }}
    .download-btn:hover {{ background: #0f766e; }}
    .ad-slot {{
      background: #f9f9f9; border: 1.5px dashed #e0e0e0;
      border-radius: 12px; height: 100px; display: flex;
      align-items: center; justify-content: center;
      color: #bbb; font-size: 13px; margin-bottom: 24px;
    }}
    .details {{ border: 1.5px solid #f0f0f0; border-radius: 16px; overflow: hidden; margin-bottom: 24px; }}
    .details h2 {{ font-size: 16px; font-weight: 700; padding: 16px 20px; border-bottom: 1px solid #f0f0f0; background: #fafafa; }}
    .details table {{ width: 100%; border-collapse: collapse; }}
    .details td {{ padding: 12px 20px; font-size: 14px; border-bottom: 1px solid #f5f5f5; }}
    .details td:first-child {{ color: #888; width: 40%; }}
    .details td:last-child {{ font-weight: 500; }}
    .details tr:last-child td {{ border-bottom: none; }}
    .related h2 {{ font-size: 18px; font-weight: 700; margin-bottom: 14px; letter-spacing: -0.3px; }}
    .related-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(240px, 1fr)); gap: 12px; }}
    .related-card {{
      border: 1.5px solid #f0f0f0; border-radius: 12px; padding: 14px 16px;
      text-decoration: none; color: #1a1a1a; display: flex;
      align-items: center; gap: 12px; transition: all 0.2s;
    }}
    .related-card:hover {{ border-color: #0d9488; box-shadow: 0 4px 12px rgba(13,148,136,0.08); }}
    .related-icon {{
      width: 38px; height: 38px; background: #f0fdfa; border-radius: 8px;
      display: flex; align-items: center; justify-content: center;
      font-size: 18px; flex-shrink: 0;
    }}
    .related-card h4 {{ font-size: 13px; font-weight: 600; margin-bottom: 3px; }}
    .related-card p {{ font-size: 12px; color: #999; }}
    /* MOBILE */
    @media (max-width: 768px) {{
      header {{ padding: 12px 16px; }}
      nav {{ display: none; }}
      .breadcrumb {{ padding: 0 16px; margin: 16px auto; }}
      .container {{ padding: 0 16px 40px; }}
      .paper-hero {{ flex-direction: column; padding: 20px; gap: 16px; }}
      .paper-thumb {{ width: 64px; height: 84px; font-size: 30px; }}
      .paper-info h1 {{ font-size: 18px; }}
      .meta-row {{ gap: 6px; }}
      .pill {{ font-size: 11px; padding: 3px 8px; }}
      .download-btn {{ width: 100%; justify-content: center; padding: 14px; font-size: 14px; }}
      .details td {{ font-size: 13px; padding: 10px 14px; }}
      .related-grid {{ grid-template-columns: 1fr; }}
      .ad-slot {{ height: 80px; }}
      footer {{ padding: 24px 16px; }}
      footer a {{ margin: 0 6px; }}
    }}
    @media (max-width: 360px) {{
      header {{ padding: 10px 12px; }}
      .breadcrumb {{ padding: 0 12px; font-size: 12px; }}
      .container {{ padding: 0 12px 36px; }}
      .paper-hero {{ padding: 16px; gap: 12px; }}
      .paper-thumb {{ width: 52px; height: 70px; font-size: 24px; }}
      .paper-info h1 {{ font-size: 16px; }}
      .pill {{ font-size: 10px; padding: 2px 7px; }}
      .download-btn {{ padding: 12px; font-size: 13px; }}
      .details td {{ font-size: 12px; padding: 8px 12px; }}
      .related-card {{ padding: 12px 14px; }}
      .related-card h4 {{ font-size: 12px; }}
      footer {{ padding: 20px 12px; font-size: 12px; }}
    }}
    footer {{
      background: #fafafa; border-top: 1px solid #f0f0f0;
      padding: 32px 24px; text-align: center; font-size: 13px; color: #aaa; margin-top: 32px;
    }}
    footer a {{ color: #aaa; text-decoration: none; margin: 0 10px; }}
    footer a:hover {{ color: #0d9488; }}
  </style>
</head>
<body>

<header>
  <a class="logo" href="/">Exam<span>Stash</span></a>
</header>

<div class="breadcrumb">
  <a href="/">Home</a><span>›</span>
  <a href="/{board}/">{board_name}</a><span>›</span>
  <a href="/{board}/{cls}/">{class_name}</a><span>›</span>
  <a href="/{board}/{cls}/{subject}/">{subject_name}</a><span>›</span>
  {year}{series_label}
</div>

<div class="container">
  <div class="paper-hero">
    <div class="paper-thumb">{icon}</div>
    <div class="paper-info">
      <h1>{board_name} {class_name} {subject_name} Question Paper {year}{series_label}</h1>
      <div class="meta-row">
        <span class="pill pill-blue">{board_name}</span>
        <span class="pill pill-green">{class_name}</span>
        <span class="pill pill-orange">{subject_name}</span>
        <span class="pill pill-purple">{year}</span>
        {series_pill}
        <span class="pill pill-green">Annual Exam</span>
      </div>
      {download_action}
    </div>
  </div>

  <div class="ad-slot">Advertisement</div>

  <div class="details">
    <h2>Paper Details</h2>
    <table>
      <tr><td>Board</td><td>{board_name}</td></tr>
      <tr><td>Class</td><td>{class_name}</td></tr>
      <tr><td>Subject</td><td>{subject_name}</td></tr>
      <tr><td>Year</td><td>{year}</td></tr>
      <tr><td>Series</td><td>{series.upper() if series else "N/A"}</td></tr>
      <tr><td>Exam Type</td><td>Annual Examination</td></tr>
      <tr><td>File Format</td><td>PDF</td></tr>
      <tr><td>Download</td><td>{download_status}</td></tr>
    </table>
  </div>

  <div class="ad-slot">Advertisement</div>

  {related_section}
</div>

<footer>
  <div style="margin-bottom: 14px;">
    <strong>ExamStash</strong> &nbsp;|&nbsp;
    <a href="/about/">About</a>
    <a href="/contact/">Contact</a>
    <a href="/privacy/">Privacy Policy</a>
    <a href="/dmca/">DMCA</a>
  </div>
  <div style="margin-bottom: 12px; display: flex; justify-content: center; align-items: center; gap: 12px;">
    <a href="https://www.instagram.com/sahilsleem/" target="_blank" rel="noopener" aria-label="Instagram" title="Instagram" style="display: inline-flex; align-items: center; justify-content: center; width: 38px; height: 38px; border-radius: 50%; background: #f0fdfa; color: #0d9488; transition: all 0.2s; text-decoration: none;">
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="2" width="20" height="20" rx="5" ry="5"></rect><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"></path><line x1="17.5" y1="6.5" x2="17.51" y2="6.5"></line></svg>
    </a>
    <a href="https://t.me/sahilsleem" target="_blank" rel="noopener" aria-label="Telegram" title="Telegram" style="display: inline-flex; align-items: center; justify-content: center; width: 38px; height: 38px; border-radius: 50%; background: #f0fdfa; color: #0d9488; transition: all 0.2s; text-decoration: none;">
      <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm4.64 6.8c-.15 1.58-.8 5.42-1.13 7.19-.14.75-.42 1-.68 1.03-.58.05-1.02-.38-1.58-.75-.88-.58-1.38-.94-2.23-1.5-.99-.65-.35-1.01.22-1.59.15-.15 2.71-2.48 2.76-2.69a.2.2 0 00-.05-.18c-.06-.05-.14-.03-.21-.02-.09.02-1.49.95-4.22 2.79-.4.27-.76.41-1.08.4-.36-.01-1.04-.2-1.55-.37-.63-.2-1.12-.31-1.08-.66.02-.18.27-.36.74-.55 2.92-1.27 4.86-2.11 5.83-2.51 2.78-1.16 3.35-1.36 3.73-1.36.08 0 .27.02.39.12.1.08.13.19.14.27-.01.06.01.24 0 .37z"/></svg>
    </a>
    <a href="mailto:examstash1@gmail.com" aria-label="Email" title="Email" style="display: inline-flex; align-items: center; justify-content: center; width: 38px; height: 38px; border-radius: 50%; background: #f0fdfa; color: #0d9488; transition: all 0.2s; text-decoration: none;">
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"></path><polyline points="22,6 12,13 2,6"></polyline></svg>
    </a>
  </div>
  <p style="font-size: 12px; color: #888;">Built for students. Free past exam papers & syllabus.</p>
</footer>

</body>
</html>"""


# ============================================================
# RUN — generates all folders and files automatically
# ============================================================
generated = 0

for board, cls, subject, year, series, pdf_link in papers:
    if not pdf_link or pdf_link == "#":
        continue

    html = make_paper_page(board, cls, subject, year, series, pdf_link)
    if not html:
        continue

    # Build folder path — add series subfolder if series exists
    if series:
        folder = os.path.join(board, cls, subject, year, f"series-{series}")
    else:
        folder = os.path.join(board, cls, subject, year)

    filepath = os.path.join(folder, "index.html")

    os.makedirs(folder, exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"  CREATED: {filepath}")
    generated += 1

print(f"\nDone! {generated} pages created/updated.")