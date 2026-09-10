#!/usr/bin/env python3
"""
ExamStash Paper Ingestion Assistant (add_paper.py)
Automates adding new question papers, generating pages, updating search index, and sitemap.
"""

import os
import re
import sys
import subprocess
import argparse

# Force UTF-8 stdout for Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

WORKSPACE = os.path.dirname(os.path.abspath(__file__))

KNOWN_BOARDS = {
    "1": ("jkbose", "JKBOSE"),
    "2": ("cbse", "CBSE"),
    "3": ("icse", "ICSE"),
    "4": ("islamia-college", "Islamia College"),
    "5": ("kashmir-university", "Kashmir University"),
    "6": ("bgsbu", "BGSBU"),
    "7": ("cluster-university", "Cluster University"),
    "8": ("neet", "NEET"),
    "9": ("jee", "JEE"),
    "10": ("jkpsc", "JKPSC")
}

KNOWN_CLASSES = {
    "1": ("class-10", "Class 10"),
    "2": ("class-12", "Class 12"),
    "3": ("bca", "BCA"),
    "4": ("bba", "BBA"),
    "5": ("bcom", "B.Com"),
    "6": ("ba", "B.A"),
    "7": ("bsc-it", "B.Sc IT"),
    "8": ("mba", "MBA")
}

def extract_drive_id(link_or_id):
    link_or_id = link_or_id.strip()
    match = re.search(r'(?:file/d/|id=)([a-zA-Z0-9_-]{20,})', link_or_id)
    if match:
        return match.group(1)
    if re.match(r'^[a-zA-Z0-9_-]{20,}$', link_or_id):
        return link_or_id
    return None

def prompt_choice(title, options):
    print(f"\n{title}")
    for k, v in options.items():
        print(f"  [{k}] {v[1]} ({v[0]})")
    print("  [0] Custom / Other")
    
    choice = input("Select option (number): ").strip()
    if choice in options:
        return options[choice]
    else:
        slug = input("Enter slug (e.g. jkbose, class-10): ").strip().lower().replace(" ", "-")
        name = input("Enter display name (e.g. JKBOSE, Class 10): ").strip()
        return slug, name

def interactive_add():
    print("=" * 60)
    print(" ExamStash Question Paper Ingestion Assistant")
    print("=" * 60)

    # 1. Board
    board_slug, board_name = prompt_choice("Select Education Board / University:", KNOWN_BOARDS)

    # 2. Class
    cls_slug, cls_name = prompt_choice("Select Class / Course:", KNOWN_CLASSES)

    # 3. Subject
    print("\nSubject Information:")
    subject_name = input("Enter Subject Name (e.g. Mathematics, Physics): ").strip()
    subject_slug = input(f"Enter Subject Slug (default: {subject_name.lower().replace(' ', '-')}): ").strip().lower()
    if not subject_slug:
        subject_slug = subject_name.lower().replace(" ", "-")

    # 4. Year
    year = input("\nEnter Exam Year (e.g. 2026, 2025): ").strip()
    if not year.isdigit():
        year = "2026"

    # 5. Series
    series_input = input("Enter Series (e.g. A, B, C or leave empty for single paper): ").strip().lower()
    series = f"series-{series_input}" if series_input and not series_input.startswith("series-") else series_input

    # 6. Drive Link
    while True:
        drive_input = input("\nEnter Google Drive Share Link or File ID: ").strip()
        drive_id = extract_drive_id(drive_input)
        if drive_id:
            break
        print("❌ Invalid Google Drive URL or ID. Please check and try again.")

    add_paper_to_system(board_slug, board_name, cls_slug, cls_name, subject_slug, subject_name, year, series, drive_id)

def add_paper_to_system(board_slug, board_name, cls_slug, cls_name, subject_slug, subject_name, year, series, drive_id):
    # Construct Paper ID
    series_part = f"-{series}" if series else ""
    paper_id = f"{board_slug}-{cls_slug}-{subject_slug}-{year}{series_part}"

    print(f"\nAdding paper: {paper_id}")
    print(f"  Board: {board_name} ({board_slug})")
    print(f"  Class: {cls_name} ({cls_slug})")
    print(f"  Subject: {subject_name} ({subject_slug})")
    print(f"  Year: {year} {series.upper() if series else ''}")
    print(f"  Drive ID: {drive_id}")

    # 1. Update generate.py PAPERS dictionary
    generate_path = os.path.join(WORKSPACE, "generate.py")
    with open(generate_path, "r", encoding="utf-8") as f:
        gen_content = f.read()

    new_paper_entry = f"""    "{paper_id}": {{
        "board": "{board_slug}",
        "board_name": "{board_name}",
        "class": "{cls_slug}",
        "class_name": "{cls_name}",
        "subject": "{subject_slug}",
        "subject_name": "{subject_name}",
        "year": "{year}",
        "series": "{series}",
        "drive_id": "{drive_id}",
        "icon": "📄",
    }},"""

    if f'"{paper_id}"' in gen_content:
        print(f"\n⚠️ Paper ID '{paper_id}' already exists in generate.py. Updating Drive ID...")
        pattern = rf'"{paper_id}":\s*\{{[^}}]*\}}'
        gen_content = re.sub(pattern, new_paper_entry.strip(), gen_content)
    else:
        # Insert before PAPERS closing brace
        gen_content = gen_content.replace("PAPERS = {", f"PAPERS = {{\n{new_paper_entry}")

    with open(generate_path, "w", encoding="utf-8") as f:
        f.write(gen_content)

    print("  ✓ Updated generate.py")

    # 2. Run generate.py
    print("  ⚙️  Compiling HTML paper page...")
    subprocess.run([sys.executable, os.path.join(WORKSPACE, "generate.py")], cwd=WORKSPACE, check=True)

    # 3. Update search-index.js
    update_search_index(board_name, cls_name, subject_name, year, series, board_slug, cls_slug, subject_slug)

    # 4. Regenerate sitemap
    print("  ⚙️  Regenerating sitemap.xml...")
    subprocess.run([sys.executable, os.path.join(WORKSPACE, "generate_sitemap.py")], cwd=WORKSPACE, check=True)

    # Calculate Canonical Path
    series_url_part = f"/{series}" if series else ""
    canonical_url = f"http://localhost:8000/{board_slug}/{cls_slug}/{subject_slug}/{year}{series_url_part}/"

    print("\n" + "=" * 60)
    print("🎉 SUCCESS! Paper successfully ingested and published.")
    print(f"👉 Local Preview: {canonical_url}")
    print("=" * 60 + "\n")

def update_search_index(board_name, cls_name, subject_name, year, series, board_slug, cls_slug, subject_slug):
    search_index_path = os.path.join(WORKSPACE, "assets", "js", "search-index.js")
    if not os.path.exists(search_index_path):
        return

    series_label = f" ({series.replace('-', ' ').title()})" if series else ""
    series_path = f"{series}/" if series else ""
    entry_title = f"{board_name} {cls_name} {subject_name} {year}{series_label}"
    entry_url = f"/{board_slug}/{cls_slug}/{subject_slug}/{year}/{series_path}"

    with open(search_index_path, "r", encoding="utf-8") as f:
        content = f.read()

    if entry_url in content:
        print("  ✓ Search index already contains this URL.")
        return

    new_entry = f"""  {{
    title: "{entry_title}",
    subtitle: "{board_name} · {cls_name} · Question Paper",
    category: "paper",
    url: "{entry_url}",
    keywords: ["{board_slug}", "{cls_slug}", "{subject_slug}", "{year}", "{board_name.lower()}", "{cls_name.lower()}"]
  }},"""

    content = content.replace("const EXAMSTASH_SEARCH_INDEX = [", f"const EXAMSTASH_SEARCH_INDEX = [\n{new_entry}")

    with open(search_index_path, "w", encoding="utf-8") as f:
        f.write(content)

    print("  ✓ Updated client-side search index (assets/js/search-index.js)")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="ExamStash Paper Ingestion Assistant")
    parser.add_argument("--board", help="Board slug (e.g. jkbose)")
    parser.add_argument("--board-name", help="Board display name (e.g. JKBOSE)")
    parser.add_argument("--class", dest="cls", help="Class slug (e.g. class-10)")
    parser.add_argument("--class-name", help="Class display name (e.g. Class 10)")
    parser.add_argument("--subject", help="Subject slug (e.g. maths)")
    parser.add_argument("--subject-name", help="Subject display name (e.g. Mathematics)")
    parser.add_argument("--year", help="Exam year (e.g. 2026)")
    parser.add_argument("--series", default="", help="Series (e.g. series-a, series-b, or empty)")
    parser.add_argument("--drive-id", help="Google Drive File ID or Share URL")

    args = parser.parse_args()

    if args.board and args.cls and args.subject and args.year and args.drive_id:
        b_name = args.board_name or args.board.upper()
        c_name = args.class_name or args.cls.replace("-", " ").title()
        s_name = args.subject_name or args.subject.replace("-", " ").title()
        d_id = extract_drive_id(args.drive_id)
        if not d_id:
            print("❌ Invalid Google Drive URL or File ID.")
            sys.exit(1)
        add_paper_to_system(args.board, b_name, args.cls, c_name, args.subject, s_name, args.year, args.series, d_id)
    else:
        interactive_add()
