#!/usr/bin/env python3
"""
ExamStash 1-Step Quick Paper Addition for Islamia College (quick_add.py)
Just paste the Drive link and describe the subject/paper.
Handles parsing, HTML compilation, search indexing, sitemap generation, and auto-deployment.
"""

import os
import re
import sys
import subprocess

# Force UTF-8 stdout on Windows
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

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

def add_paper_to_semester(parsed, drive_id):
    course_slug = parsed["course_slug"]
    sem_num = parsed["semester"]
    subject_title = parsed["subject_title"]
    is_syllabus = parsed["is_syllabus"]

    sem_dir = os.path.join(course_slug, f"semester-{sem_num}")
    sem_index = os.path.join(sem_dir, "index.html")

    if not os.path.exists(sem_index):
        print(f"❌ Target semester page not found: {sem_index}")
        return

    with open(sem_index, "r", encoding="utf-8") as f:
        content = f.read()

    drive_link = f"https://drive.google.com/file/d/{drive_id}/view?usp=sharing"
    btn_text = "📋 View Syllabus PDF" if is_syllabus else "⬇️ Download Paper"
    btn_class = "btn-syl" if is_syllabus else "btn-paper"
    type_label = "Syllabus" if is_syllabus else "Question Paper"

    new_item_card = f"""    <div class="item-card">
      <div class="item-info">
        <h3>{subject_title}</h3>
        <p>{parsed['course_name']} · Semester {sem_num} {type_label}</p>
      </div>
      <div class="btn-wrap">
        <a href="{drive_link}" target="_blank" rel="noopener" class="btn {btn_class}">{btn_text}</a>
      </div>
    </div>\n"""

    # If page previously had notice-card, replace it with item-list structure
    if "notice-card" in content:
        section_label = "📋 Official Syllabus" if is_syllabus else "📄 Question Papers"
        replacement_block = f"""  <div class="type-label">{section_label}</div>
  <div class="item-list">
{new_item_card}  </div>"""
        content = re.sub(r'<div class="notice-card">.*?</div>\s*</div>', replacement_block + "\n</div>", content, flags=re.DOTALL)
    elif '<div class="item-list">' in content:
        # Append into existing item-list
        content = content.replace('<div class="item-list">', '<div class="item-list">\n' + new_item_card, 1)
    else:
        section_label = "📋 Official Syllabus" if is_syllabus else "📄 Question Papers"
        replacement_block = f"""  <div class="type-label">{section_label}</div>
  <div class="item-list">
{new_item_card}  </div>
</div>"""
        content = content.replace('</div>\n\n<footer>', replacement_block + '\n\n<footer>')

    # Save to root and mirror in islamia-college/
    with open(sem_index, "w", encoding="utf-8") as f:
        f.write(content)

    mirror_index = os.path.join("islamia-college", sem_dir, "index.html")
    if os.path.exists(os.path.dirname(mirror_index)):
        with open(mirror_index, "w", encoding="utf-8") as f:
            f.write(content)

    print(f"✅ Added {subject_title} ({type_label}) to {course_slug}/semester-{sem_num}/")

def main():
    print("=" * 60)
    print(" ⚡ Islamia College Paper Ingestion Assistant")
    print("=" * 60)

    desc = input("\n👉 Enter Paper Description (e.g. 'BCA Semester 2 Data Structures' or 'Physics Sem 1'): ").strip()
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

    add_paper_to_semester(parsed, drive_id)

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
