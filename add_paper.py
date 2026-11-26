#!/usr/bin/env python3
"""
ExamStash Auto-Add Paper (add_paper.py)
Automates adding a contributed question paper or syllabus to ExamStash.

Usage:
    python add_paper.py --course bca --semester semester-1 --subject "Data Structures 2023" --type paper --link "https://drive.google.com/file/d/123/view?usp=sharing"
"""
import os
import re
import sys
import argparse
import generate_all_pages
import generate_sitemap

# Force UTF-8 on Windows
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

def slugify(text):
    text = text.lower()
    text = re.sub(r'[^\w\s-]', '', text).strip()
    return re.sub(r'[-\s]+', '-', text)

def smart_title(text):
    text = text.strip()
    if text.islower():
        words = text.split()
        capitalized = []
        acronyms = {"it", "bca", "bba", "bcom", "ba", "bsc", "dbms", "ai", "ml", "os", "sql", "iot", "c++", "c#", "php"}
        roman = {"i", "ii", "iii", "iv", "v", "vi"}
        for w in words:
            if w.lower() in acronyms:
                capitalized.append(w.upper())
            elif w.lower() in roman:
                capitalized.append(w.upper())
            else:
                capitalized.append(w.capitalize())
        return " ".join(capitalized)
    return text

def extract_drive_id(link_or_id):
    if not link_or_id:
        return None
    link_or_id = link_or_id.strip()
    match = re.search(r'(?:file/d/|id=)([a-zA-Z0-9_-]{20,})', link_or_id)
    if match:
        return match.group(1)
    if re.match(r'^[a-zA-Z0-9_-]{20,}$', link_or_id):
        return link_or_id
    return None

def normalize_drive_link(link_or_id):
    drive_id = extract_drive_id(link_or_id)
    if drive_id:
        return f"https://drive.google.com/file/d/{drive_id}/view?usp=sharing"
    return link_or_id

def add_paper(course, semester, subject, resource_type, link):
    course = course.lower().strip()
    # Normalize course slug if full name was given
    for prog in generate_all_pages.PROGRAMMES:
        if course in [prog["slug"], prog["name"].lower(), prog["short_name"].lower()]:
            course = prog["slug"]
            break

    # Normalize semester
    m_sem = re.search(r'[1-6]', str(semester))
    sem_num = m_sem.group(0) if m_sem else "1"
    sem_slug = f"semester-{sem_num}"

    # Normalize drive link
    drive_url = normalize_drive_link(link)

    # Determine title & slug
    is_syllabus = "syllabus" in resource_type.lower() or "syllabus" in subject.lower()
    base_slug = slugify(subject)
    if is_syllabus and "syllabus" not in base_slug:
        base_slug = f"{base_slug}-syllabus"

    # Target directory
    target_dir = os.path.join(course, sem_slug, base_slug)
    
    # Handle duplicates by appending counter
    counter = 1
    actual_slug = base_slug
    while os.path.exists(target_dir):
        # If already exists with exact same link, update existing
        index_file = os.path.join(target_dir, "index.html")
        if os.path.exists(index_file):
            with open(index_file, "r", encoding="utf-8") as f:
                if drive_url in f.read():
                    print(f"Paper already exists at {target_dir}")
                    break
        counter += 1
        actual_slug = f"{base_slug}-{counter}"
        target_dir = os.path.join(course, sem_slug, actual_slug)

    os.makedirs(target_dir, exist_ok=True)
    target_index = os.path.join(target_dir, "index.html")

    # Clean title
    title = smart_title(subject)
    if is_syllabus and "syllabus" not in title.lower():
        title = f"{title} Syllabus"

    # Find course display name
    course_display = course.upper()
    for prog in generate_all_pages.PROGRAMMES:
        if prog["slug"] == course:
            course_display = prog["short_name"]
            break

    # Initial HTML for generate_all_pages to ingest
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} — {course_display} Semester {sem_num} | ExamStash</title>
<meta name="description" content="View or download {title} for {course_display}, Semester {sem_num} at Islamia College of Science & Commerce (ICSC), Srinagar. Free student resource.">
<link rel="canonical" href="https://examstash.online/{course}/{sem_slug}/{actual_slug}/">
</head>
<body>
<main>
<p class="college">Islamia College of Science &amp; Commerce, Srinagar</p>
<p class="bc"><a href="/">Home</a> › <a href="/{course}/">{course_display}</a> › <a href="/{course}/{sem_slug}/">Semester {sem_num}</a> › {title}</p>
<h1>{title}</h1>
<a class="r" href="{drive_url}" target="_blank" rel="noopener"><b>Download PDF</b><i>View</i></a>
</main>
</body>
</html>"""

    with open(target_index, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"Created paper entry: {target_dir}")

    # Regenerate all pages (updates semester table, programme counts, homepage, mirrors)
    print("Regenerating all pages...")
    generate_all_pages.main()

    # Regenerate sitemap
    print("Regenerating sitemap...")
    generate_sitemap.main()

    print(f"Successfully added '{title}' to {course}/{sem_slug}/{actual_slug}/")
    return target_dir

def main():
    parser = argparse.ArgumentParser(description="Add paper or syllabus to ExamStash")
    parser.add_argument("--course", required=True, help="Course slug, e.g., bca, bsc-it, bba, bcom")
    parser.add_argument("--semester", required=True, help="Semester, e.g. semester-1 or 1")
    parser.add_argument("--subject", required=True, help="Subject name and exam year")
    parser.add_argument("--type", default="paper", help="paper or syllabus")
    parser.add_argument("--link", required=True, help="Google Drive link or file ID")

    args = parser.parse_args()
    add_paper(args.course, args.semester, args.subject, args.type, args.link)

if __name__ == "__main__":
    main()
