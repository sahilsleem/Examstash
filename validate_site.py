#!/usr/bin/env python3
"""
ExamStash Site Health & Link Validator
Scans all HTML pages, internal links, assets, Google Drive IDs, and sitemap.xml.
"""

import os
import re
import sys
import xml.etree.ElementTree as ET

# Force UTF-8 stdout for Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

WORKSPACE = os.path.dirname(os.path.abspath(__file__))

def validate_site():
    print("=" * 60)
    print(" ExamStash Site Health & Integrity Validator")
    print("=" * 60)

    html_files = []
    for root, dirs, files in os.walk(WORKSPACE):
        if ".git" in root or "assets" in root:
            continue
        for file in files:
            if file.endswith(".html"):
                html_files.append(os.path.join(root, file))

    print(f"\nFound {len(html_files)} HTML pages to scan.\n")

    errors = []
    warnings = []
    checked_links = 0
    checked_assets = 0

    drive_id_regex = re.compile(r'https://drive\.google\.com/(?:file/d/|uc\?export=download&id=)([a-zA-Z0-9_-]{20,})')

    for filepath in html_files:
        rel_file = os.path.relpath(filepath, WORKSPACE).replace("\\", "/")
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        # 1. Check Asset links (CSS, JS, SVG, Icons)
        assets = re.findall(r'(?:href|src)=["\'](/assets/[^"\']+)["\']', content)
        for asset in assets:
            checked_assets += 1
            clean_asset = asset.split("?")[0].split("#")[0]
            local_asset_path = os.path.join(WORKSPACE, clean_asset.lstrip("/"))
            if not os.path.exists(local_asset_path):
                errors.append(f"[BROKEN ASSET] {rel_file} -> {asset} does not exist!")

        # 2. Check internal anchor href links
        internal_links = re.findall(r'<a\s+[^>]*href=["\'](/[^"\']*)["\']', content)
        for link in internal_links:
            # Ignore hash-only, mailto, tel, telegram
            if link.startswith("/#") or link.startswith("#"):
                continue
            
            clean_link = link.split("#")[0].split("?")[0]
            if not clean_link or clean_link == "/":
                continue

            checked_links += 1
            # Check if directory with index.html or exact file exists
            target_path = os.path.join(WORKSPACE, clean_link.lstrip("/"))
            target_index = os.path.join(target_path, "index.html")
            
            if not os.path.exists(target_path) and not os.path.exists(target_index):
                errors.append(f"[BROKEN LINK] {rel_file} -> {link}")

        # 3. Check Google Drive Links
        drive_links = re.findall(r'https://drive\.google\.com/[^"\'\s<>]+', content)
        for dlink in drive_links:
            if not drive_id_regex.search(dlink):
                warnings.append(f"[INVALID DRIVE LINK] {rel_file} -> {dlink}")

    # 4. Check Sitemap.xml
    sitemap_path = os.path.join(WORKSPACE, "sitemap.xml")
    if os.path.exists(sitemap_path):
        try:
            tree = ET.parse(sitemap_path)
            urls = tree.findall(".//{http://www.sitemaps.org/schemas/sitemap/0.9}loc")
            print(f"Sitemap check: {len(urls)} URLs registered in sitemap.xml.")
        except Exception as e:
            errors.append(f"[SITEMAP ERROR] Failed to parse sitemap.xml: {e}")
    else:
        errors.append("[SITEMAP ERROR] sitemap.xml is missing!")

    # Print Summary
    print("-" * 60)
    print(f"Checked {checked_links} internal links")
    print(f"Checked {checked_assets} static asset references")
    print("-" * 60)

    if errors:
        print(f"\nFAILED: Found {len(errors)} error(s):")
        for err in errors[:20]:
            print(f"  * {err}")
        if len(errors) > 20:
            print(f"  ... and {len(errors) - 20} more errors.")
        return False
    else:
        print("\nPASSED: 0 broken links, 0 missing assets!")

    if warnings:
        print(f"\n{len(warnings)} Warning(s):")
        for w in warnings[:10]:
            print(f"  * {w}")

    print("\nSite health is in excellent condition!\n")
    return True

if __name__ == "__main__":
    validate_site()
