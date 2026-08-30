#!/usr/bin/env python3
"""
ExamStash 1-Step Quick Paper Addition for Islamia College (quick_add.py)
Creates dedicated paper download page with monetization ad slots, links to semester page,
rebuilds search index & sitemap, and deploys live.
"""

import os
import re
import sys
import subprocess

# Force UTF-8 stdout on Windows
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

def slugify(text):
    text = text.lower()
    text = re.sub(r'[^\w\s-]', '', text).strip()
    return re.sub(r'[-\s]+', '-', text)

def extract_drive_id(link_or_id):
    link_or_id = link_or_id.strip()
    match = re.search(r'(?:file/d/|id=)([a-zA-Z0-9_-]{20,})', link_or_id)
    if match:
        return match.group(1)
    if re.match(r'^[a-zA-Z0-9_-]{20,}$', link_or_id):
        return link_or_id
    return None

def parse_paper_string(text):
    text_lower = text.lower()

    # 1. Detect Course / Department
    course_slug = "bca"
    course_name = "BCA"

    if "bsc it" in text_lower or "b.sc it" in text_lower or "b.sc. it" in text_lower or "information technology" in text_lower:
        course_slug, course_name = "bsc-it", "B.Sc. IT"
    elif "bba" in text_lower or "business administration" in text_lower:
        course_slug, course_name = "bba", "BBA"
    elif "bcom" in text_lower or "b.com" in text_lower or "commerce" in text_lower:
        course_slug, course_name = "bcom", "B.Com"
    elif "ba" in text_lower or "b.a" in text_lower or "arts" in text_lower or "english" in text_lower or "kashmiri" in text_lower:
        course_slug, course_name = "ba", "B.A."
    elif "physics" in text_lower:
        course_slug, course_name = "bsc-physics", "B.Sc. Physics"
    elif "chemistry" in text_lower:
        course_slug, course_name = "bsc-chemistry", "B.Sc. Chemistry"
    elif "math" in text_lower:
        course_slug, course_name = "bsc-mathematics", "B.Sc. Mathematics"
    elif "botany" in text_lower:
        course_slug, course_name = "bsc-botany", "B.Sc. Botany"
    elif "zoology" in text_lower:
        course_slug, course_name = "bsc-zoology", "B.Sc. Zoology"
    elif "biotech" in text_lower:
        course_slug, course_name = "bsc-biotechnology", "B.Sc. Biotechnology"
    elif "biochem" in text_lower:
        course_slug, course_name = "bsc-biochemistry", "B.Sc. Biochemistry"
    elif "bca" in text_lower or "computer" in text_lower:
        course_slug, course_name = "bca", "BCA"

    # 2. Detect Semester
    sem_match = re.search(r'(?:sem(?:ester)?|s)\s*([1-6])\b|\b([1-6])(?:st|nd|rd|th)?\s*sem', text_lower)
    sem_num = sem_match.group(1) or sem_match.group(2) if sem_match else "1"

    # 3. Detect Paper vs Syllabus
    is_syllabus = "syllabus" in text_lower or "curriculum" in text_lower

    # 4. Clean Subject Title
    clean = text
    for token in ["islamia", "college", "icsc", "srinagar", "bca", "bba", "bcom", "ba", "bsc", "it", "physics", "chemistry", "mathematics", "maths", "botany", "zoology", "biotechnology", "biochemistry", "sem", "semester", "1st", "2nd", "3rd", "4th", "5th", "6th", "1", "2", "3", "4", "5", "6", "paper", "syllabus", "question"]:
        clean = re.sub(r'\b' + re.escape(token) + r'\b', '', clean, flags=re.IGNORECASE)

    clean = re.sub(r'[^\w\s-]', '', clean).strip()
    clean = re.sub(r'\s+', ' ', clean)
    subject_title = clean.title() if clean else f"{course_name} Paper"

    return {
        "course_slug": course_slug,
        "course_name": course_name,
        "semester": sem_num,
        "is_syllabus": is_syllabus,
        "subject_title": subject_title
    }

paper_page_template = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{subject_title} — {course_title} Semester {sem_num} ({item_type}) | Islamia College</title>
  <meta name="description" content="Download {subject_title} {item_type} for {course_title} Semester {sem_num} at Islamia College of Science & Commerce (ICSC), Srinagar. Free PDF download." />
  <link rel="canonical" href="https://examstash.pages.dev/{course_slug}/semester-{sem_num}/{paper_slug}/" />
  <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-5315343862609383" crossorigin="anonymous"></script>

  <link rel="manifest" href="/manifest.json" />
  <meta name="theme-color" content="#0d9488" />
  <link rel="icon" type="image/svg+xml" href="/assets/icons/icon.svg" />
  <link rel="apple-touch-icon" href="/assets/icons/icon.svg" />
  <link rel="stylesheet" href="/assets/css/global.css" />

  <style>
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    body {{ font-family: 'Segoe UI', system-ui, sans-serif; background: #fff; color: #1a1a1a; }}
    header {{
      padding: 16px 20px; border-bottom: 1px solid #f0f0f0;
      display: flex; align-items: center; justify-content: space-between;
      position: sticky; top: 0; background: #fff; z-index: 100;
    }}
    .header-inner {{ max-width: 960px; margin: 0 auto; width: 100%; display: flex; align-items: center; }}
    .logo {{ font-size: 19px; font-weight: 800; color: #1a1a1a; text-decoration: none; letter-spacing: -0.4px; }}
    .logo span {{ color: #0d9488; }}
    .breadcrumb {{ padding: 14px 20px; font-size: 13px; color: #999; max-width: 960px; margin: 0 auto; }}
    .breadcrumb a {{ color: #999; text-decoration: none; }}
    .breadcrumb a:hover {{ color: #0d9488; }}
    .breadcrumb span {{ margin: 0 6px; }}
    .container {{ padding: 0 20px 60px; max-width: 960px; margin: 0 auto; }}
    .page-header {{
      background: linear-gradient(135deg, #115e59 0%, #0d9488 100%);
      border-radius: 16px; padding: 28px 24px; margin-bottom: 24px; color: white;
      box-shadow: 0 4px 20px rgba(13, 148, 136, 0.12);
    }}
    .college-tag {{
      font-size: 11px; font-weight: 600; background: rgba(255,255,255,0.2);
      display: inline-block; padding: 3px 10px; border-radius: 20px;
      margin-bottom: 10px; letter-spacing: 0.05em;
    }}
    .page-header h1 {{ font-size: 24px; font-weight: 800; margin-bottom: 6px; line-height: 1.3; }}
    .page-header p {{ font-size: 14px; opacity: 0.85; line-height: 1.5; }}
    
    .download-card {{
      border: 1.5px solid #ccfbf1;
      background: linear-gradient(180deg, #f0fdfa 0%, #ffffff 100%);
      border-radius: 16px; padding: 32px 24px; text-align: center;
      margin: 24px 0; box-shadow: 0 4px 20px rgba(13, 148, 136, 0.08);
    }}
    .file-icon {{ font-size: 44px; margin-bottom: 12px; }}
    .file-title {{ font-size: 20px; font-weight: 800; margin-bottom: 6px; color: #115e59; }}
    .file-meta {{ font-size: 13px; color: #0f766e; margin-bottom: 24px; }}
    .btn-download-main {{
      display: inline-flex; align-items: center; justify-content: center; gap: 10px;
      background: #0d9488; color: white; padding: 14px 32px; border-radius: 12px;
      font-size: 15px; font-weight: 700; text-decoration: none; transition: all 0.2s;
      box-shadow: 0 4px 14px rgba(13, 148, 136, 0.3);
    }}
    .btn-download-main:hover {{ background: #0f766e; transform: translateY(-2px); box-shadow: 0 6px 20px rgba(13, 148, 136, 0.4); }}
    
    .info-grid {{
      display: grid; grid-template-columns: repeat(3, 1fr);
      gap: 12px; margin: 24px 0;
    }}
    .info-box {{
      border: 1px solid #f0f0f0; border-radius: 10px; padding: 14px; text-align: center; background: #fff;
    }}
    .info-box-label {{ font-size: 11px; color: #888; text-transform: uppercase; font-weight: 600; margin-bottom: 4px; }}
    .info-box-val {{ font-size: 14px; font-weight: 700; color: #1a1a1a; }}

    .back-btn {{
      display: inline-flex; align-items: center; gap: 6px;
      color: #0d9488; text-decoration: none; font-size: 14px; font-weight: 600;
      margin-top: 10px;
    }}
    .back-btn:hover {{ text-decoration: underline; }}

    footer {{
      background: #fafafa; border-top: 1px solid #f0f0f0;
      padding: 24px 16px; text-align: center; font-size: 13px; color: #aaa;
    }}
    footer a {{ color: #aaa; text-decoration: none; margin: 0 8px; }}
    footer a:hover {{ color: #0d9488; }}
    @media (max-width: 600px) {{
      .info-grid {{ grid-template-columns: 1fr; }}
      .btn-download-main {{ width: 100%; }}
    }}
  </style>
</head>
<body>

<header>
  <div class="header-inner">
    <a class="logo" href="/">Islamia College <span>of Science & Commerce</span></a>
  </div>
</header>

<div class="breadcrumb">
  <a href="/">Home</a><span>›</span>
  <a href="/{course_slug}/">{course_title}</a><span>›</span>
  <a href="/{course_slug}/semester-{sem_num}/">Semester {sem_num}</a><span>›</span>
  {subject_title}
</div>

<div class="container">
  <div class="page-header">
    <span class="college-tag">{course_title} — SEMESTER {sem_num}</span>
    <h1>{subject_title}</h1>
    <p>Islamia College of Science & Commerce, Srinagar — {item_type}</p>
  </div>

  <!-- Top Monetization Ad Placement -->
  <div class="ad-slot">
    <div class="ad-slot-label">Advertisement</div>
    <div class="ad-slot-inner">
      <ins class="adsbygoogle"
           style="display:block; text-align:center;"
           data-ad-layout="in-article"
           data-ad-format="fluid"
           data-ad-client="ca-pub-5315343862609383"></ins>
      <script>
           (adsbygoogle = window.adsbygoogle || []).push({{}});
      </script>
    </div>
  </div>

  <!-- Download Card -->
  <div class="download-card">
    <div class="file-icon">{icon}</div>
    <div class="file-title">{subject_title}</div>
    <div class="file-meta">{course_title} · Semester {sem_num} · {item_type} · Official PDF</div>

    <a href="{drive_link}" target="_blank" rel="noopener" class="btn-download-main">
      ⬇️ Download {item_type} PDF
    </a>
  </div>

  <!-- File Specs Info Grid -->
  <div class="info-grid">
    <div class="info-box">
      <div class="info-box-label">College</div>
      <div class="info-box-val">ICSC Srinagar</div>
    </div>
    <div class="info-box">
      <div class="info-box-label">Format</div>
      <div class="info-box-val">High-Quality PDF</div>
    </div>
    <div class="info-box">
      <div class="info-box-label">Access</div>
      <div class="info-box-val">Free / No Login</div>
    </div>
  </div>

  <a href="/{course_slug}/semester-{sem_num}/" class="back-btn">
    ← Back to {course_title} Semester {sem_num} Papers
  </a>

  <!-- Bottom Monetization Ad Placement -->
  <div class="ad-slot">
    <div class="ad-slot-label">Advertisement</div>
    <div class="ad-slot-inner">
      <ins class="adsbygoogle"
           style="display:block; text-align:center;"
           data-ad-layout="in-article"
           data-ad-format="fluid"
           data-ad-client="ca-pub-5315343862609383"></ins>
      <script>
           (adsbygoogle = window.adsbygoogle || []).push({{}});
      </script>
    </div>
  </div>

</div>

<footer>
  <div style="margin-bottom: 8px;">
    <a href="/about/">About</a>
    <a href="/contact/">Contact</a>
    <a href="/privacy/">Privacy Policy</a>
    <a href="/dmca/">DMCA</a>
  </div>
  <p>© 2026 Islamia College of Science and Commerce, Srinagar</p>
</footer>

<script src="/assets/js/search-index.js?v=4"></script>
<script src="/assets/js/search.js?v=4"></script>
<script src="/assets/js/pwa.js?v=4"></script>
<script src="/assets/js/analytics.js"></script>
</body>
</html>
"""

def add_paper(parsed, drive_id):
    course_slug = parsed["course_slug"]
    course_name = parsed["course_name"]
    sem_num = parsed["semester"]
    subject_title = parsed["subject_title"]
    is_syllabus = parsed["is_syllabus"]
    item_type = "Syllabus" if is_syllabus else "Question Paper"
    icon = "📋" if is_syllabus else "📄"

    paper_slug = slugify(subject_title)
    if is_syllabus and not paper_slug.endswith("syllabus"):
        paper_slug += "-syllabus"

    drive_link = f"https://drive.google.com/file/d/{drive_id}/view?usp=sharing"

    # 1. Create Dedicated Download Page
    page_html = paper_page_template.format(
        subject_title=subject_title,
        course_title=course_name,
        course_slug=course_slug,
        sem_num=sem_num,
        item_type=item_type,
        paper_slug=paper_slug,
        icon=icon,
        drive_link=drive_link
    )

    out_dir = os.path.join(course_slug, f"semester-{sem_num}", paper_slug)
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, "index.html"), "w", encoding="utf-8") as f:
        f.write(page_html)

    mirror_dir = os.path.join("islamia-college", out_dir)
    os.makedirs(mirror_dir, exist_ok=True)
    with open(os.path.join(mirror_dir, "index.html"), "w", encoding="utf-8") as f:
        f.write(page_html)

    # 2. Update Semester Page Link
    sem_dir = os.path.join(course_slug, f"semester-{sem_num}")
    sem_index = os.path.join(sem_dir, "index.html")

    with open(sem_index, "r", encoding="utf-8") as f:
        sem_content = f.read()

    btn_text = "View Syllabus →" if is_syllabus else "View & Download →"
    btn_class = "btn-syl" if is_syllabus else "btn-paper"

    item_card = f"""    <div class="item-card">
      <div class="item-info">
        <h3>{subject_title}</h3>
        <p>{course_name} · Semester {sem_num} {item_type}</p>
      </div>
      <div class="btn-wrap">
        <a href="/{course_slug}/semester-{sem_num}/{paper_slug}/" class="btn {btn_class}">{btn_text}</a>
      </div>
    </div>\n"""

    if "notice-card" in sem_content:
        section_label = "📋 Official Syllabus" if is_syllabus else "📄 Question Papers"
        replacement_block = f"""  <div class="type-label">{section_label}</div>
  <div class="item-list">
{item_card}  </div>"""
        sem_content = re.sub(r'<div class="notice-card">.*?</div>\s*<!-- Monetization Placeholder -->', replacement_block + "\n\n  <!-- Monetization Placeholder -->", sem_content, flags=re.DOTALL)
        sem_content = re.sub(r'<div class="notice-card">.*?</div>\s*</div>', replacement_block + "\n</div>", sem_content, flags=re.DOTALL)
    elif '<div class="item-list">' in sem_content:
        sem_content = sem_content.replace('<div class="item-list">', '<div class="item-list">\n' + item_card, 1)
    else:
        section_label = "📋 Official Syllabus" if is_syllabus else "📄 Question Papers"
        replacement_block = f"""  <div class="type-label">{section_label}</div>
  <div class="item-list">
{item_card}  </div>\n"""
        sem_content = sem_content.replace('  <!-- Monetization Placeholder -->', replacement_block + '\n  <!-- Monetization Placeholder -->')

    with open(sem_index, "w", encoding="utf-8") as f:
        f.write(sem_content)

    sem_mirror = os.path.join("islamia-college", sem_dir, "index.html")
    if os.path.exists(os.path.dirname(sem_mirror)):
        with open(sem_mirror, "w", encoding="utf-8") as f:
            f.write(sem_content)

    print(f"✅ Created dedicated paper page: /{course_slug}/semester-{sem_num}/{paper_slug}/")
    print(f"✅ Linked in semester page: /{course_slug}/semester-{sem_num}/")

def main():
    print("=" * 60)
    print(" ⚡ Islamia College Paper Ingestion Assistant (2-Tier Monetized)")
    print("=" * 60)

    desc = input("\n👉 Enter Paper Description (e.g. 'BCA Sem 2 Data Structures' or 'Physics Sem 1 Mechanics'): ").strip()
    if not desc:
        print("❌ No description entered.")
        return

    drive_input = input("👉 Paste Google Drive Link: ").strip()
    drive_id = extract_drive_id(drive_input)
    if not drive_id:
        print("❌ Invalid Google Drive link or ID.")
        return

    parsed = parse_paper_string(desc)
    print("\n📋 Detected Information:")
    print(f"  • Course:   {parsed['course_name']} ({parsed['course_slug']})")
    print(f"  • Semester: Semester {parsed['semester']}")
    print(f"  • Subject:  {parsed['subject_title']}")
    print(f"  • Type:     {'Syllabus' if parsed['is_syllabus'] else 'Question Paper'}")
    print(f"  • Drive ID: {drive_id}")

    confirm = input("\nProceed? [Y/n]: ").strip().lower()
    if confirm in ["n", "no"]:
        print("Cancelled.")
        return

    add_paper(parsed, drive_id)

    # Rebuild search and sitemap
    subprocess.run(["python", "generate_sitemap.py"])
    
    push = input("\n🚀 Commit and push live to Cloudflare Pages? [Y/n]: ").strip().lower()
    if push not in ["n", "no"]:
        commit_msg = f"Add {parsed['course_name']} Sem {parsed['semester']} {parsed['subject_title']}"
        subprocess.run(["git", "add", "."])
        subprocess.run(["git", "commit", "-m", commit_msg])
        subprocess.run(["git", "push", "origin", "main"])
        print("\n✅ Deployed live to https://examstash.pages.dev/ !")

if __name__ == "__main__":
    main()
