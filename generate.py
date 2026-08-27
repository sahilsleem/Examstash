import os

# ============================================================
# PAPER LIST — this is the only thing you edit to add papers
# Format: (board, class, subject, year, pdf_link)
# For pdf_link put "#" for now, we'll replace with real links later
# ============================================================
papers = [
    ("jkbose", "class-10", "maths",          "2023", "#"),
    ("jkbose", "class-10", "maths",          "2022", "#"),
    ("jkbose", "class-10", "maths",          "2021", "#"),
    ("jkbose", "class-10", "maths",          "2020", "#"),
    ("jkbose", "class-10", "science",        "2023", "#"),
    ("jkbose", "class-10", "science",        "2022", "#"),
    ("jkbose", "class-10", "science",        "2021", "#"),
    ("jkbose", "class-10", "english",        "2023", "#"),
    ("jkbose", "class-10", "english",        "2022", "#"),
    ("jkbose", "class-10", "social-science", "2023", "#"),
    ("jkbose", "class-10", "social-science", "2022", "#"),
    ("jkbose", "class-12", "physics",        "2023", "#"),
    ("jkbose", "class-12", "physics",        "2022", "#"),
    ("jkbose", "class-12", "physics",        "2021", "#"),
    ("jkbose", "class-12", "maths",          "2023", "#"),
    ("jkbose", "class-12", "maths",          "2022", "#"),
    ("jkbose", "class-12", "chemistry",      "2023", "#"),
    ("jkbose", "class-12", "chemistry",      "2022", "#"),
    ("jkbose", "class-12", "biology",        "2023", "#"),
    ("jkbose", "class-12", "biology",        "2022", "#"),
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
def make_paper_page(board, cls, subject, year, pdf_link):
    board_name   = board_names.get(board, board.upper())
    class_name   = class_names.get(cls, cls)
    subject_name = subject_names.get(subject, subject.title())
    icon         = subject_icons.get(subject, "📄")

    # Find related papers from same subject, different years
    related_years = ["2023", "2022", "2021", "2020"]
    related_html  = ""
    for ry in related_years:
        if ry != year:
            related_html += f"""
    <a href="/{board}/{cls}/{subject}/{ry}/" class="related-card">
      <div class="related-icon">📄</div>
      <div>
        <h4>{board_name} {class_name} {subject_name}</h4>
        <p>Annual Exam {ry}</p>
      </div>
    </a>"""

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{board_name} {class_name} {subject_name} Question Paper {year} PDF Download | ExamStash</title>
  <meta name="description" content="Download {board_name} {class_name} {subject_name} question paper {year} PDF for free. Annual examination paper. No login required." />
  <>
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    body {{ font-family: 'Segoe UI', system-ui, sans-serif; background: #fff; color: #1a1a1a; }}
    header {{
      padding: 16px 32px; display: flex; align-items: center;
      justify-content: space-between; border-bottom: 1px solid #f0f0f0;
      position: sticky; top: 0; background: #fff; z-index: 100;
    }}
    .logo {{ font-size: 20px; font-weight: 800; color: #1a1a1a; text-decoration: none; letter-spacing: -0.5px; }}
    .logo span {{ color: #2563eb; }}
    nav a {{ font-size: 14px; color: #555; text-decoration: none; margin-left: 24px; }}
    nav a:hover {{ color: #2563eb; }}
    .breadcrumb {{ max-width: 860px; margin: 20px auto; padding: 0 24px; font-size: 13px; color: #999; }}
    .breadcrumb a {{ color: #999; text-decoration: none; }}
    .breadcrumb a:hover {{ color: #2563eb; }}
    .breadcrumb span {{ margin: 0 6px; }}
    .container {{ max-width: 860px; margin: 0 auto; padding: 0 24px 60px; }}
    .paper-hero {{
      border: 1.5px solid #f0f0f0; border-radius: 16px;
      padding: 32px; margin-bottom: 24px;
      display: flex; gap: 24px; align-items: flex-start;
    }}
    .paper-thumb {{
      width: 90px; height: 120px; background: #eff6ff;
      border-radius: 10px; display: flex; align-items: center;
      justify-content: center; font-size: 40px; flex-shrink: 0;
    }}
    .paper-info {{ flex: 1; }}
    .paper-info h1 {{ font-size: 22px; font-weight: 700; line-height: 1.3; margin-bottom: 10px; letter-spacing: -0.3px; }}
    .meta-row {{ display: flex; flex-wrap: wrap; gap: 8px; margin-bottom: 16px; }}
    .pill {{ font-size: 12px; font-weight: 600; padding: 4px 10px; border-radius: 20px; }}
    .pill-blue {{ background: #eff6ff; color: #2563eb; }}
    .pill-green {{ background: #f0fdf4; color: #16a34a; }}
    .pill-orange {{ background: #fff7ed; color: #ea580c; }}
    .pill-purple {{ background: #faf5ff; color: #7c3aed; }}
    .download-btn {{
      display: inline-flex; align-items: center; gap: 8px;
      background: #2563eb; color: white; padding: 12px 24px;
      border-radius: 10px; font-size: 15px; font-weight: 600;
      text-decoration: none; transition: background 0.2s;
    }}
    .download-btn:hover {{ background: #1d4ed8; }}
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
    .related-card:hover {{ border-color: #2563eb; box-shadow: 0 4px 12px rgba(37,99,235,0.08); }}
    .related-icon {{
      width: 38px; height: 38px; background: #eff6ff; border-radius: 8px;
      display: flex; align-items: center; justify-content: center;
      font-size: 18px; flex-shrink: 0;
    }}
    .related-card h4 {{ font-size: 13px; font-weight: 600; margin-bottom: 3px; }}
    .related-card p {{ font-size: 12px; color: #999; }}
    footer {{
      background: #fafafa; border-top: 1px solid #f0f0f0;
      padding: 32px 24px; text-align: center; font-size: 13px; color: #aaa; margin-top: 32px;
    }}
    footer a {{ color: #aaa; text-decoration: none; margin: 0 10px; }}
        footer a:hover {{ color: #2563eb; }}
    @media (max-width: 600px) {{
      header {{ padding: 12px 16px; }}
      nav {{ display: none; }}
      .container {{ padding: 0 12px 40px; }}
      .paper-hero {{ flex-direction: column; padding: 20px; gap: 16px; }}
      .paper-thumb {{ width: 60px; height: 80px; font-size: 28px; }}
      .paper-info h1 {{ font-size: 17px; }}
      .download-btn {{ width: 100%; justify-content: center; padding: 14px; font-size: 14px; }}
      .details td {{ font-size: 13px; padding: 10px 14px; }}
      .related-grid {{ grid-template-columns: 1fr; }}
      .breadcrumb {{ padding: 0 12px; font-size: 12px; }}
    }}
  </style>
</head>
<body>

<header>
  <a class="logo" href="/">Exam<span>Stash</span></a>
  <nav>
    <a href="/jkbose/">JKBOSE</a>
    <a href="/kashmir-university/">KU</a>
    <a href="/cbse/">CBSE</a>
    <a href="/competitive/">Competitive</a>
  </nav>
</header>

<div class="breadcrumb">
  <a href="/">Home</a><span>›</span>
  <a href="/{board}/">{board_name}</a><span>›</span>
  <a href="/{board}/{cls}/">{class_name}</a><span>›</span>
  <a href="/{board}/{cls}/{subject}/">{subject_name}</a><span>›</span>
  {year}
</div>

<div class="container">
  <div class="paper-hero">
    <div class="paper-thumb">{icon}</div>
    <div class="paper-info">
      <h1>{board_name} {class_name} {subject_name} Question Paper {year}</h1>
      <div class="meta-row">
        <span class="pill pill-blue">{board_name}</span>
        <span class="pill pill-green">{class_name}</span>
        <span class="pill pill-orange">{subject_name}</span>
        <span class="pill pill-purple">{year}</span>
        <span class="pill pill-green">Annual Exam</span>
      </div>
      <a href="{pdf_link}" class="download-btn" target="_blank">⬇️ Download PDF — Free</a>
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
      <tr><td>Exam Type</td><td>Annual Examination</td></tr>
      <tr><td>File Format</td><td>PDF</td></tr>
      <tr><td>Download</td><td>Free — No login required</td></tr>
    </table>
  </div>

  <div class="ad-slot">Advertisement</div>

  <div class="related">
    <h2>Related Papers</h2>
    <div class="related-grid">{related_html}</div>
  </div>
</div>

<footer>
  <p style="margin-bottom:10px;">
    <strong>ExamStash</strong> &nbsp;|&nbsp;
    <a href="/about/">About</a>
    <a href="/contact/">Contact</a>
    <a href="/privacy/">Privacy Policy</a>
    <a href="/dmca/">DMCA</a>
  </p>
  <p>Free past exam papers for Indian students. No registration required. Always free.</p>
</footer>

</body>
</html>"""


# ============================================================
# RUN — generates all folders and files automatically
# ============================================================
generated = 0
skipped   = 0

for board, cls, subject, year, pdf_link in papers:
    folder = os.path.join(board, cls, subject, year)
    filepath = os.path.join(folder, "index.html")

    # Skip if the file already exists so we don't overwrite manual edits
    if os.path.exists(filepath):
        print(f"  SKIP (exists): {filepath}")
        skipped += 1
        continue

    os.makedirs(folder, exist_ok=True)
    html = make_paper_page(board, cls, subject, year, pdf_link)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"  CREATED: {filepath}")
    generated += 1

print(f"\nDone! {generated} pages created, {skipped} skipped.")