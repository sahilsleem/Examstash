import os
from datetime import date

BASE_URL = "https://examstash.pages.dev"
today = date.today().isoformat()

# Collect all index.html files and convert to URLs
urls = []

for root, dirs, files in os.walk("."):
    for file in files:
        if file == "index.html":
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