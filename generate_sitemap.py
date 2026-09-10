import os
import re
from datetime import date

BASE_URL = "https://examstash.online"
today = date.today().isoformat()

# Collect all index.html files and convert to URLs
urls = []

for root, dirs, files in os.walk("."):
    # Skip git, scratch, hidden folders, and mirror routes
    if ".git" in root or "scratch" in root or "islamia-college" in root:
        continue
    for file in files:
        if file == "index.html":
            file_path = os.path.join(root, file)
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                # If page is marked noindex, exclude from sitemap
                if re.search(r'<meta\s+name=["\']robots["\']\s+content=["\'][^"\']*noindex', content, re.IGNORECASE):
                    continue
            except Exception:
                pass

            # Convert file path to URL
            path = root.replace("\\", "/").replace("./", "/").lower()
            if path == ".":
                path = "/"
            elif not path.startswith("/"):
                path = "/" + path
            # Make sure path ends with /
            if not path.endswith("/"):
                path += "/"
            if path not in urls:
                urls.append(path)

# Sort URLs so sitemap is clean
urls.sort()

# Build XML
xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
xml += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'

for url in urls:
    # Skip generate scripts themselves
    if "generate" in url:
        continue
    xml += f"""  <url>
    <loc>{BASE_URL}{url}</loc>
    <lastmod>{today}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.8</priority>
  </url>\n"""

xml += '</urlset>'

with open("sitemap.xml", "w", encoding="utf-8") as f:
    f.write(xml)

print(f"Sitemap generated with {len(urls)} URLs")
print("Saved as sitemap.xml")