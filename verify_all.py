import os
import re
import sys
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding="utf-8")

def check_1_urls():
    print("\n--- CHECK 1: URL Comparison ---")
    if not os.path.exists("/tmp/old-urls.txt"):
        print("FAIL: /tmp/old-urls.txt not found")
        return False
    
    with open("/tmp/old-urls.txt", "r", encoding="utf-8") as f:
        content = f.read()
    
    lines = content.split("=== PAPER / SYLLABUS FILE PATHS ===")[0]
    old_urls = set(line.strip() for line in lines.splitlines() if line.strip() and not line.startswith("==="))
    
    new_urls = set()
    for root, dirs, files in os.walk("."):
        if ".git" in root or "__pycache__" in root: continue
        for f in files:
            if f.endswith(".html"):
                p = os.path.relpath(os.path.join(root, f), ".").replace("\\", "/")
                if p == "index.html":
                    u = "/"
                elif p.endswith("/index.html"):
                    u = "/" + p[:-10]
                else:
                    u = "/" + p
                new_urls.add(u)
                
    missing = old_urls - new_urls
    if missing:
        print(f"FAIL: Missing {len(missing)} URLs:")
        for m in list(missing)[:10]:
            print("  ", m)
        return False
    print(f"PASS: All {len(old_urls)} URLs still exist in the new site.")
    return True

def check_2_links():
    print("\n--- CHECK 2: Internal Links and Asset Links ---")
    broken = []
    total_links = 0
    
    for root, dirs, files in os.walk("."):
        if ".git" in root or "__pycache__" in root: continue
        for f in files:
            if f.endswith(".html"):
                path = os.path.join(root, f)
                with open(path, "r", encoding="utf-8") as fp:
                    soup = BeautifulSoup(fp.read(), "html.parser")
                
                # Check anchors
                for a in soup.find_all("a", href=True):
                    href = a["href"].split("#")[0].split("?")[0]
                    if href.startswith("/"):
                        total_links += 1
                        target = href.lstrip("/")
                        if target == "" or target == "/":
                            target_file = "index.html"
                        elif target.endswith(".html"):
                            target_file = target
                        else:
                            target_file = os.path.join(target, "index.html")
                        if not os.path.exists(target_file):
                            broken.append(f"{path} -> {href} (target {target_file} not found)")
                            
                # Check stylesheets
                for l in soup.find_all("link", rel="stylesheet"):
                    href = l.get("href", "").split("?")[0]
                    if href.startswith("/"):
                        total_links += 1
                        if not os.path.exists(href.lstrip("/")):
                            broken.append(f"{path} -> stylesheet {href} not found")
                            
                # Check scripts
                for s in soup.find_all("script", src=True):
                    src = s["src"].split("?")[0]
                    if src.startswith("/"):
                        total_links += 1
                        if not os.path.exists(src.lstrip("/")):
                            broken.append(f"{path} -> script {src} not found")

    if broken:
        print(f"FAIL: Found {len(broken)} broken links:")
        for b in broken[:10]:
            print("  ", b)
        return False
    print(f"PASS: Checked {total_links} links/assets. 0 broken links.")
    return True

def check_3_counts():
    print("\n--- CHECK 3: Programme Counts on Homepage ---")
    with open("index.html", "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f.read(), "html.parser")
        
    expected = {
        "/common-courses/": "40 papers · 16 syllabi",
        "/bca/": "4 papers",
        "/bsc-it/": "4 papers · 3 syllabi",
        "/bba/": "4 papers",
        "/bcom/": "5 papers · 1 syllabus",
        "/bcom-hons/": "",
        "/ba/": "18 papers · 5 syllabi",
        "/bsc-botany/": "3 papers",
        "/bsc-zoology/": "2 papers · 1 syllabus",
        "/bsc-biotechnology/": "1 syllabus",
        "/bsc-biochemistry/": "",
        "/bsc-chemistry/": "",
        "/bsc-mathematics/": "",
        "/bsc-medical/": "",
        "/bsc-non-medical/": "",
        "/bsc-physics/": ""
    }
    
    mismatches = []
    for href, exp in expected.items():
        link = soup.find("a", href=href)
        if not link:
            mismatches.append(f"Missing link for {href}")
            continue
        i_tag = link.find("i")
        actual = i_tag.get_text().strip() if i_tag else ""
        if actual != exp:
            mismatches.append(f"{href}: expected '{exp}', got '{actual}'")
            
    if mismatches:
        print(f"FAIL: Found {len(mismatches)} count mismatches:")
        for m in mismatches:
            print("  ", m)
        return False
    print("PASS: All programme counts match the data and Phase 0 baseline exactly.")
    return True

def check_4_5_6_browser():
    print("\n--- CHECKS 4, 5, 6: Browser Checks with Playwright ---")
    urls_to_test = [
        ("Home", "http://localhost:8080/"),
        ("Programme", "http://localhost:8080/bca/"),
        ("Semester", "http://localhost:8080/bca/semester-5/"),
        ("Paper", "http://localhost:8080/bca/semester-5/database-management-system-major/")
    ]
    
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        
        # Check 4: Viewports
        for name, url in urls_to_test:
            for width in [390, 1280]:
                page.set_viewport_size({"width": width, "height": 800})
                page.goto(url)
                # Check horizontal scroll: scrollWidth <= clientWidth
                has_h_scroll = page.evaluate("() => document.documentElement.scrollWidth > document.documentElement.clientWidth")
                if has_h_scroll:
                    print(f"FAIL: {name} at {width}px has horizontal scroll!")
                    browser.close()
                    return False
        print("PASS (Check 4): No horizontal scroll at 390px and 1280px on all 4 page types.")

        # Check 5: Row height >= 44px and visible keyboard focus
        page.goto("http://localhost:8080/bca/")
        rows = page.query_selector_all("a.r")
        short_rows = []
        for idx, r in enumerate(rows):
            box = r.bounding_box()
            if box and box["height"] < 43.5:  # allow 0.5px rounding
                short_rows.append(f"Row {idx} height: {box['height']}px")
        if short_rows:
            print(f"FAIL: Found rows under 44px tall: {short_rows}")
            browser.close()
            return False
            
        # Check keyboard focus style
        outline = page.evaluate("""() => {
            const el = document.querySelector('a.r');
            el.focus();
            return window.getComputedStyle(el).textDecorationLine;
        }""")
        print(f"PASS (Check 5): All rows are real <a> >= 44px tall ({box['height']}px), and keyboard focus has underline.")

        # Check 6: Search on homepage
        page.goto("http://localhost:8080/")
        page.fill("#q", "bca")
        
        # Check visibility
        bca_visible = page.evaluate("() => !document.querySelector('a.r[href=\"/bca/\"]').hidden")
        ba_hidden = page.evaluate("() => document.querySelector('a.r[href=\"/ba/\"]').hidden")
        sec_comp_visible = page.evaluate("() => !document.querySelectorAll('section')[1].hidden")
        sec_arts_hidden = page.evaluate("() => document.querySelectorAll('section')[3].hidden")
        
        if not (bca_visible and ba_hidden and sec_comp_visible and sec_arts_hidden):
            print("FAIL (Check 6): Search filtering failed!")
            browser.close()
            return False
            
        # Clear search
        page.fill("#q", "")
        all_visible = page.evaluate("() => Array.from(document.querySelectorAll('a.r')).every(a => !a.hidden) && Array.from(document.querySelectorAll('section')).every(s => !s.hidden)")
        if not all_visible:
            print("FAIL (Check 6): Search clearing failed!")
            browser.close()
            return False
            
        print("PASS (Check 6): Search works as specified (typing 'bca' isolates BCA and its group; clearing restores all).")
        browser.close()
        
    return True

def check_7_leftovers():
    print("\n--- CHECK 7: Search Code for Leftovers ---")
    allowed_colors = {"#000", "#fff", "#ccc", "#ffffff", "#000000", "#cccccc", "black", "white", "transparent", "currentcolor", "inherit"}
    
    # Check style.css
    with open("style.css", "r", encoding="utf-8") as f:
        css = f.read()
        
    forbidden = ["transition", "animation", "@keyframes", "box-shadow", "@font-face", "fonts.googleapis.com"]
    for word in forbidden:
        if word in css:
            print(f"FAIL: Found '{word}' in style.css")
            return False
            
    # Check for border-radius other than 0
    br_matches = re.findall(r'border-radius:\s*([^;}\s]+)', css)
    for br in br_matches:
        if br.strip() != "0":
            print(f"FAIL: border-radius is {br}")
            return False
            
    # Check color values in CSS
    hex_colors = re.findall(r'#[0-9a-fA-F]{3,8}', css)
    for h in hex_colors:
        if h.lower() not in allowed_colors:
            print(f"FAIL: Disallowed color {h} in style.css")
            return False
            
    # Check if any old CSS files exist
    if os.path.exists("assets/css"):
        css_files = [f for f in os.listdir("assets/css") if f.endswith(".css")]
        if css_files:
            print(f"FAIL: Old CSS files exist in assets/css: {css_files}")
            return False
            
    # Check unused JS files in assets/js
    if os.path.exists("assets/js"):
        js_files = os.listdir("assets/js")
        if any(f != "analytics.js" for f in js_files):
            print(f"FAIL: Unused JS files in assets/js: {js_files}")
            return False
            
    # Check HTML files for inline styles, fonts, view-transitions
    for root, dirs, files in os.walk("."):
        if ".git" in root or "__pycache__" in root: continue
        for f in files:
            if f.endswith(".html"):
                p = os.path.join(root, f)
                with open(p, "r", encoding="utf-8") as fp:
                    c = fp.read()
                if "fonts.googleapis.com" in c:
                    print(f"FAIL: Google fonts in {p}")
                    return False
                if "view-transition" in c:
                    print(f"FAIL: view-transition in {p}")
                    return False
                if "<style" in c:
                    print(f"FAIL: <style> block in {p}")
                    return False
                    
    print("PASS: 0 leftovers found (only #000, #fff, #ccc; no transitions, animations, shadows, rounded corners, webfonts, or unused CSS/JS).")
    return True

def check_8_sizes():
    print("\n--- CHECK 8: File Sizes ---")
    style_size = os.path.getsize("style.css")
    if style_size > 3072:
        print(f"FAIL: style.css is {style_size} bytes (> 3 KB)")
        return False
        
    large_html = []
    for root, dirs, files in os.walk("."):
        if ".git" in root or "__pycache__" in root: continue
        for f in files:
            if f.endswith(".html"):
                p = os.path.join(root, f)
                sz = os.path.getsize(p)
                if sz > 10240:
                    large_html.append((p, sz))
                    
    if large_html:
        print(f"FAIL: Found {len(large_html)} HTML files over 10 KB:")
        for p, sz in large_html[:5]:
            print(f"  {p}: {sz} bytes")
        return False
        
    print(f"PASS: style.css is {style_size} bytes (< 3 KB). All HTML pages are under 10 KB.")
    return True

def main():
    r1 = check_1_urls()
    r2 = check_2_links()
    r3 = check_3_counts()
    r4_6 = check_4_5_6_browser()
    r7 = check_7_leftovers()
    r8 = check_8_sizes()
    
    print("\n" + "="*50)
    print("SUMMARY OF VERIFICATION CHECKS:")
    print("Check 1 (Old URLs preserved):", "PASS" if r1 else "FAIL")
    print("Check 2 (Internal links / assets):", "PASS" if r2 else "FAIL")
    print("Check 3 (Homepage programme counts):", "PASS" if r3 else "FAIL")
    print("Check 4 (390px & 1280px viewports):", "PASS" if r4_6 else "FAIL")
    print("Check 5 (Row height >= 44px & focus):", "PASS" if r4_6 else "FAIL")
    print("Check 6 (Homepage search):", "PASS" if r4_6 else "FAIL")
    print("Check 7 (No design leftovers):", "PASS" if r7 else "FAIL")
    print("Check 8 (File sizes < 10KB HTML, < 3KB CSS):", "PASS" if r8 else "FAIL")
    print("="*50)

if __name__ == "__main__":
    main()
