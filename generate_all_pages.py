import os
import re
import shutil
from bs4 import BeautifulSoup

PROGRAMMES = [
    {
        "slug": "common-courses",
        "name": "Multidisciplinary & Skill Courses",
        "short_name": "Multidisciplinary & Skill Courses",
        "group": "1. Common",
        "semesters": ["semester-1", "semester-2", "semester-3"]
    },
    {
        "slug": "bca",
        "name": "BCA",
        "short_name": "BCA",
        "group": "2. Computer & IT",
        "semesters": ["semester-1", "semester-2", "semester-3", "semester-4", "semester-5", "semester-6"]
    },
    {
        "slug": "bsc-it",
        "name": "B.Sc. IT",
        "short_name": "B.Sc. IT",
        "group": "2. Computer & IT",
        "semesters": ["semester-1", "semester-2", "semester-3", "semester-4", "semester-5", "semester-6"]
    },
    {
        "slug": "bba",
        "name": "BBA",
        "short_name": "BBA",
        "group": "3. Business",
        "semesters": ["semester-1", "semester-2", "semester-3", "semester-4", "semester-5", "semester-6"]
    },
    {
        "slug": "bcom",
        "name": "B.Com",
        "short_name": "B.Com",
        "group": "3. Business",
        "semesters": ["semester-1", "semester-2", "semester-3", "semester-4", "semester-5", "semester-6"]
    },
    {
        "slug": "bcom-hons",
        "name": "B.Com. (Honours)",
        "short_name": "B.Com. (Honours)",
        "group": "3. Business",
        "semesters": ["semester-1", "semester-2", "semester-3", "semester-4", "semester-5", "semester-6"]
    },
    {
        "slug": "ba",
        "name": "B.A. & English Honours",
        "short_name": "B.A. & English Honours",
        "group": "4. Arts",
        "semesters": ["semester-1", "semester-2", "semester-3", "semester-4", "semester-5", "semester-6"]
    },
    {
        "slug": "bsc-botany",
        "name": "B.Sc. Botany",
        "short_name": "B.Sc. Botany",
        "group": "5. Sciences",
        "semesters": ["semester-1", "semester-2", "semester-3", "semester-4", "semester-5", "semester-6"]
    },
    {
        "slug": "bsc-zoology",
        "name": "B.Sc. Zoology",
        "short_name": "B.Sc. Zoology",
        "group": "5. Sciences",
        "semesters": ["semester-1", "semester-2", "semester-3", "semester-4", "semester-5", "semester-6"]
    },
    {
        "slug": "bsc-biotechnology",
        "name": "B.Sc. Biotechnology",
        "short_name": "B.Sc. Biotechnology",
        "group": "5. Sciences",
        "semesters": ["semester-1", "semester-2", "semester-3", "semester-4", "semester-5", "semester-6"]
    },
    {
        "slug": "bsc-biochemistry",
        "name": "B.Sc. Biochemistry",
        "short_name": "B.Sc. Biochemistry",
        "group": "5. Sciences",
        "semesters": ["semester-1", "semester-2", "semester-3", "semester-4", "semester-5", "semester-6"]
    },
    {
        "slug": "bsc-chemistry",
        "name": "B.Sc. Chemistry",
        "short_name": "B.Sc. Chemistry",
        "group": "5. Sciences",
        "semesters": ["semester-1", "semester-2", "semester-3", "semester-4", "semester-5", "semester-6"]
    },
    {
        "slug": "bsc-mathematics",
        "name": "B.Sc. Mathematics",
        "short_name": "B.Sc. Mathematics",
        "group": "5. Sciences",
        "semesters": ["semester-1", "semester-2", "semester-3", "semester-4", "semester-5", "semester-6"]
    },
    {
        "slug": "bsc-medical",
        "name": "B.Sc. Medical",
        "short_name": "B.Sc. Medical",
        "group": "5. Sciences",
        "semesters": ["semester-1", "semester-2", "semester-3", "semester-4", "semester-5", "semester-6"]
    },
    {
        "slug": "bsc-non-medical",
        "name": "B.Sc. Non-Medical",
        "short_name": "B.Sc. Non-Medical",
        "group": "5. Sciences",
        "semesters": ["semester-1", "semester-2", "semester-3", "semester-4", "semester-5", "semester-6"]
    },
    {
        "slug": "bsc-physics",
        "name": "B.Sc. Physics",
        "short_name": "B.Sc. Physics",
        "group": "5. Sciences",
        "semesters": ["semester-1", "semester-2", "semester-3", "semester-4", "semester-5", "semester-6"]
    }
]

FOOTER_HTML = """<footer>
<p><a href="https://t.me/sahilsleem">Share a paper</a></p>
<nav class="soc" aria-label="Social links">
<a href="https://t.me/sahilsleem" aria-label="Telegram" title="Telegram"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21.5 3 2.5 10.4l6 2.3 2.3 6.2 3.2-4 4.8 3.6z"/><path d="m8.5 12.7 13-9.7"/></svg></a>
<a href="https://www.instagram.com/sahilsleem/" aria-label="Instagram" title="Instagram"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><line x1="17.5" y1="6.5" x2="17.51" y2="6.5"/></svg></a>
<a href="mailto:examstash1@gmail.com" aria-label="Email" title="Email"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/><polyline points="22,6 12,13 2,6"/></svg></a>
</nav>
</footer>"""

def format_count(papers, syllabi):
    parts = []
    if papers > 0:
        parts.append(f"{papers} paper" if papers == 1 else f"{papers} papers")
    if syllabi > 0:
        parts.append(f"{syllabi} syllabus" if syllabi == 1 else f"{syllabi} syllabi")
    return " · ".join(parts)

def build_head(title, description, canonical_url, og_title=None, og_desc=None, extra_meta=""):
    og_title = og_title or title
    og_desc = og_desc or description
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<meta name="description" content="{description}">
<link rel="canonical" href="{canonical_url}">
{extra_meta}<!-- Open Graph / Facebook -->
<meta property="og:type" content="website">
<meta property="og:site_name" content="ExamStash">
<meta property="og:title" content="{og_title}">
<meta property="og:description" content="{og_desc}">
<meta property="og:url" content="{canonical_url}">
<meta property="og:image" content="https://examstash.online/assets/images/og-preview.svg">
<!-- Twitter -->
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{og_title}">
<meta name="twitter:description" content="{og_desc}">
<meta name="twitter:image" content="https://examstash.online/assets/images/og-preview.svg">
<link rel="manifest" href="/manifest.json">
<meta name="theme-color" content="#ffffff">
<link rel="icon" type="image/svg+xml" href="/assets/icons/icon.svg">
<link rel="apple-touch-icon" href="/assets/icons/icon.svg">
<link rel="stylesheet" href="/style.css">
<script defer src="/assets/js/analytics.js"></script>
</head>"""

def main():
    print("Collecting resource data across all programmes...")
    data = {}
    
    for prog in PROGRAMMES:
        slug = prog["slug"]
        prog_data = {"semesters": {}, "total_papers": 0, "total_syllabi": 0}
        
        for sem in prog["semesters"]:
            sem_path = os.path.join(slug, sem)
            sem_data = {"papers": [], "syllabi": []}
            
            if os.path.exists(sem_path):
                subdirs = sorted([d for d in os.listdir(sem_path) if os.path.isdir(os.path.join(sem_path, d))])
                for d in subdirs:
                    sub_index = os.path.join(sem_path, d, "index.html")
                    if os.path.exists(sub_index):
                        with open(sub_index, "r", encoding="utf-8") as f:
                            c = f.read()
                        
                        soup = BeautifulSoup(c, "html.parser")
                        h1_tag = soup.find("h1")
                        title = h1_tag.get_text().strip() if h1_tag else d.replace("-", " ").title()
                        
                        # Preserve existing page title, description, and canonical
                        page_title = soup.title.string.strip() if soup.title else f"{title} | ExamStash"
                        meta_desc = soup.find("meta", attrs={"name": "description"})
                        page_desc = meta_desc["content"].strip() if meta_desc and "content" in meta_desc.attrs else f"View or download {title} for {prog['short_name']} at Islamia College."
                        
                        m_drive = re.search(r'href=[\x22\x27](https://drive\.google\.com/[^\x22\x27\s>]+)[\x22\x27]', c)
                        drive_link = m_drive.group(1) if m_drive else "#"
                        
                        is_syllabus = "syllabus" in d.lower()
                        
                        item = {
                            "slug": d,
                            "title": title,
                            "page_title": page_title,
                            "page_desc": page_desc,
                            "drive_link": drive_link,
                            "url": f"/{slug}/{sem}/{d}/"
                        }
                        
                        if is_syllabus:
                            sem_data["syllabi"].append(item)
                        else:
                            sem_data["papers"].append(item)
                            
            p_cnt = len(sem_data["papers"])
            s_cnt = len(sem_data["syllabi"])
            sem_data["count_str"] = format_count(p_cnt, s_cnt)
            prog_data["semesters"][sem] = sem_data
            prog_data["total_papers"] += p_cnt
            prog_data["total_syllabi"] += s_cnt
            
        prog_data["count_str"] = format_count(prog_data["total_papers"], prog_data["total_syllabi"])
        data[slug] = prog_data
        print(f"  {slug}: {prog_data['total_papers']} papers, {prog_data['total_syllabi']} syllabi -> '{prog_data['count_str']}'")

    print("\n1. Generating Home Page (index.html)...")
    home_extra = """<meta name="google-site-verification" content="-XvMSdU_BJpLdQ2gJreW-AkOWLhSFMGMdVF2F_nroP4">
<script async crossorigin="anonymous" src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-1741354477413638"></script>
<!-- Schema.org JSON-LD -->
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "WebSite",
  "name": "ExamStash \u2014 Islamia College Past Papers & Syllabus",
  "url": "https://examstash.online/"
}
</script>
"""
    home_head = build_head(
        title="Islamia College of Science and Commerce — Past Papers & Syllabus",
        description="Download free previous year question papers and syllabus for Islamia College of Science and Commerce (ICSC) Srinagar. BCA, B.Sc. IT, BBA, B.Com, B.A. and B.Sc. streams.",
        canonical_url="https://examstash.online/",
        extra_meta=home_extra
    )
    
    sections_html = []
    
    # 1. Common
    cc_count = data["common-courses"]["count_str"]
    cc_i = f"<i>{cc_count}</i>" if cc_count else "<i></i>"
    sections_html.append(f"""<section>
<h2>1. Common</h2>
<a class="r" href="/common-courses/"><b>Multidisciplinary &amp; Skill Courses</b>{cc_i}</a>
</section>""")

    # 2. Computer & IT
    bca_c = data["bca"]["count_str"]
    bca_i = f"<i>{bca_c}</i>" if bca_c else "<i></i>"
    bscit_c = data["bsc-it"]["count_str"]
    bscit_i = f"<i>{bscit_c}</i>" if bscit_c else "<i></i>"
    sections_html.append(f"""<section>
<h2>2. Computer &amp; IT</h2>
<a class="r" href="/bca/"><b>BCA</b>{bca_i}</a>
<a class="r" href="/bsc-it/"><b>B.Sc. IT</b>{bscit_i}</a>
</section>""")

    # 3. Business
    bba_c = data["bba"]["count_str"]
    bba_i = f"<i>{bba_c}</i>" if bba_c else "<i></i>"
    bcom_c = data["bcom"]["count_str"]
    bcom_i = f"<i>{bcom_c}</i>" if bcom_c else "<i></i>"
    bcomh_c = data["bcom-hons"]["count_str"]
    bcomh_i = f"<i>{bcomh_c}</i>" if bcomh_c else "<i></i>"
    sections_html.append(f"""<section>
<h2>3. Business</h2>
<a class="r" href="/bba/"><b>BBA</b>{bba_i}</a>
<a class="r" href="/bcom/"><b>B.Com</b>{bcom_i}</a>
<a class="r" href="/bcom-hons/"><b>B.Com. (Honours)</b>{bcomh_i}</a>
</section>""")

    # 4. Arts
    ba_c = data["ba"]["count_str"]
    ba_i = f"<i>{ba_c}</i>" if ba_c else "<i></i>"
    sections_html.append(f"""<section>
<h2>4. Arts</h2>
<a class="r" href="/ba/"><b>B.A. &amp; English Honours</b>{ba_i}</a>
</section>""")

    # 5. Sciences
    science_slugs = [
        ("bsc-botany", "B.Sc. Botany"),
        ("bsc-zoology", "B.Sc. Zoology"),
        ("bsc-biotechnology", "B.Sc. Biotechnology"),
        ("bsc-biochemistry", "B.Sc. Biochemistry"),
        ("bsc-chemistry", "B.Sc. Chemistry"),
        ("bsc-mathematics", "B.Sc. Mathematics"),
        ("bsc-medical", "B.Sc. Medical"),
        ("bsc-non-medical", "B.Sc. Non-Medical"),
        ("bsc-physics", "B.Sc. Physics"),
    ]
    sci_links = []
    for s_slug, s_name in science_slugs:
        sc_c = data[s_slug]["count_str"]
        sc_i = f"<i>{sc_c}</i>" if sc_c else "<i></i>"
        sci_links.append(f'<a class="r" href="/{s_slug}/"><b>{s_name}</b>{sc_i}</a>')
    
    sections_html.append(f"""<section>
<h2>5. Sciences</h2>
{chr(10).join(sci_links)}
</section>""")

    about_section_html = """<section id="about">
<h2>About</h2>
<p>ExamStash has free past papers and syllabus for students of Islamia College of Science &amp; Commerce, Srinagar. A paper missing? Send it on <a href="https://t.me/sahilsleem">Telegram</a>.</p>
</section>"""

    home_body = f"""<body>
<main>
<p class="college">Islamia College of Science &amp; Commerce, Srinagar</p>
<h1>ExamStash</h1>
<input id="q" type="search" aria-label="Search programmes" placeholder="Search programme" autocomplete="off">
{chr(10).join(sections_html)}
{about_section_html}
{FOOTER_HTML}
</main>
<script>
var q=document.getElementById('q');
q.addEventListener('input',function(){{var v=q.value.toLowerCase().trim();
document.querySelectorAll('a.r').forEach(function(a){{a.hidden=!!v&&a.textContent.toLowerCase().indexOf(v)<0}});
document.querySelectorAll('section').forEach(function(s){{if(s.id==='about'){{s.hidden=!!v}}else{{s.hidden=!s.querySelector('a.r:not([hidden])')}}}})}});
</script>
</body>
</html>"""

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(home_head + "\n" + home_body)

    print("2. Generating Programme Pages...")
    for prog in PROGRAMMES:
        slug = prog["slug"]
        short_name = prog["short_name"]
        prog_path = os.path.join(slug, "index.html")
        
        prog_title = f"{short_name} Past Papers & Syllabus — Islamia College"
        prog_desc = f"Download free previous year question papers and syllabi for {short_name} at Islamia College of Science & Commerce, Srinagar."
        canonical_url = f"https://examstash.online/{slug}/"
        
        if os.path.exists(prog_path):
            with open(prog_path, "r", encoding="utf-8") as f:
                soup = BeautifulSoup(f.read(), "html.parser")
            if soup.title:
                prog_title = soup.title.string.strip()
            md = soup.find("meta", attrs={"name": "description"})
            if md and "content" in md.attrs:
                prog_desc = md["content"].strip()
                
        prog_head = build_head(
            title=prog_title,
            description=prog_desc,
            canonical_url=canonical_url,
            extra_meta='<script async crossorigin="anonymous" src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-1741354477413638"></script>\n'
        )
        
        sem_rows = []
        for sem in prog["semesters"]:
            sem_data = data[slug]["semesters"].get(sem, {"count_str": ""})
            c_str = sem_data["count_str"]
            c_i = f"<i>{c_str}</i>" if c_str else "<i></i>"
            sem_num = sem.replace("semester-", "")
            sem_rows.append(f'<a class="r" href="/{slug}/{sem}/"><b>Semester {sem_num}</b>{c_i}</a>')
            
        prog_body = f"""<body>
<main>
<p class="college">Islamia College of Science &amp; Commerce, Srinagar</p>
<p class="bc"><a href="/">Home</a> › {short_name}</p>
<h1>{short_name}</h1>
{chr(10).join(sem_rows)}
{FOOTER_HTML}
</main>
</body>
</html>"""

        with open(prog_path, "w", encoding="utf-8") as f:
            f.write(prog_head + "\n" + prog_body)

    print("3. Generating Semester Pages and Subject Pages...")
    for prog in PROGRAMMES:
        slug = prog["slug"]
        short_name = prog["short_name"]
        
        for sem in prog["semesters"]:
            sem_dir = os.path.join(slug, sem)
            if not os.path.exists(sem_dir):
                continue
            
            sem_num = sem.replace("semester-", "")
            sem_display = f"Semester {sem_num}"
            sem_index_path = os.path.join(sem_dir, "index.html")
            
            sem_title = f"{short_name} {sem_display} Past Papers & Syllabus — Islamia College"
            sem_desc = f"Download previous year question papers and syllabi for {short_name} {sem_display} at Islamia College of Science & Commerce, Srinagar."
            canonical_url = f"https://examstash.online/{slug}/{sem}/"
            
            if os.path.exists(sem_index_path):
                with open(sem_index_path, "r", encoding="utf-8") as f:
                    soup = BeautifulSoup(f.read(), "html.parser")
                if soup.title:
                    sem_title = soup.title.string.strip()
                md = soup.find("meta", attrs={"name": "description"})
                if md and "content" in md.attrs:
                    sem_desc = md["content"].strip()
                    
            sem_head = build_head(
                title=sem_title,
                description=sem_desc,
                canonical_url=canonical_url,
                extra_meta='<script async crossorigin="anonymous" src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-1741354477413638"></script>\n'
            )
            
            sem_data = data[slug]["semesters"].get(sem, {"papers": [], "syllabi": []})
            
            content_blocks = []
            if sem_data["papers"]:
                p_rows = [f'<a class="r" href="{p["url"]}"><b>{p["title"]}</b><i>View</i></a>' for p in sem_data["papers"]]
                content_blocks.append(f"""<h2>Question papers</h2>\n{chr(10).join(p_rows)}""")
                
            if sem_data["syllabi"]:
                s_rows = [f'<a class="r" href="{s["url"]}"><b>{s["title"]}</b><i>View</i></a>' for s in sem_data["syllabi"]]
                content_blocks.append(f"""<h2>Syllabus</h2>\n{chr(10).join(s_rows)}""")
                
            sem_body = f"""<body>
<main>
<p class="college">Islamia College of Science &amp; Commerce, Srinagar</p>
<p class="bc"><a href="/">Home</a> › <a href="/{slug}/">{short_name}</a> › {sem_display}</p>
<h1>{sem_display}</h1>
{chr(10).join(content_blocks)}
{FOOTER_HTML}
</main>
</body>
</html>"""

            with open(sem_index_path, "w", encoding="utf-8") as f:
                f.write(sem_head + "\n" + sem_body)

            # Subject / Paper pages
            all_subjects = sem_data["papers"] + sem_data["syllabi"]
            for sub in all_subjects:
                sub_path = os.path.join(sem_dir, sub["slug"], "index.html")
                sub_title = sub["page_title"]
                sub_desc = sub["page_desc"]
                sub_canonical = f"https://examstash.online/{slug}/{sem}/{sub['slug']}/"
                
                sub_head = build_head(
                    title=sub_title,
                    description=sub_desc,
                    canonical_url=sub_canonical,
                    extra_meta='<script async crossorigin="anonymous" src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-1741354477413638"></script>\n'
                )
                
                sub_body = f"""<body>
<main>
<p class="college">Islamia College of Science &amp; Commerce, Srinagar</p>
<p class="bc"><a href="/">Home</a> › <a href="/{slug}/">{short_name}</a> › <a href="/{slug}/{sem}/">{sem_display}</a> › {sub['title']}</p>
<h1>{sub['title']}</h1>
<a class="r" href="{sub['drive_link']}" target="_blank" rel="noopener"><b>Download PDF</b><i>View</i></a>
{FOOTER_HTML}
</main>
</body>
</html>"""

                with open(sub_path, "w", encoding="utf-8") as f:
                    f.write(sub_head + "\n" + sub_body)

    print("4. Generating Other Pages (about, contact, privacy, terms, dmca, 404)...")
    
    # About
    about_head = build_head(
        title="About ExamStash — Independent Academic Resource",
        description="ExamStash has free past papers and syllabus for students of Islamia College of Science & Commerce, Srinagar.",
        canonical_url="https://examstash.online/about/",
        extra_meta='<script async crossorigin="anonymous" src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-1741354477413638"></script>\n'
    )
    about_body = f"""<body>
<main>
<p class="college">Islamia College of Science &amp; Commerce, Srinagar</p>
<p class="bc"><a href="/">Home</a> › About</p>
<h1>About</h1>
<p>ExamStash has free past papers and syllabus for students of Islamia College of Science &amp; Commerce, Srinagar. A paper missing? Send it on <a href="https://t.me/sahilsleem">Telegram</a>.</p>
{FOOTER_HTML}
</main>
</body>
</html>"""
    with open("about/index.html", "w", encoding="utf-8") as f:
        f.write(about_head + "\n" + about_body)

    # Contact
    contact_head = build_head(
        title="Contact — ExamStash",
        description="Contact ExamStash for inquiries, paper submissions, or feedback.",
        canonical_url="https://examstash.online/contact/",
        extra_meta='<script async crossorigin="anonymous" src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-1741354477413638"></script>\n'
    )
    contact_body = f"""<body>
<main>
<p class="college">Islamia College of Science &amp; Commerce, Srinagar</p>
<p class="bc"><a href="/">Home</a> › Contact</p>
<h1>Contact</h1>
<p>Send a message on <a href="https://t.me/sahilsleem">Telegram</a> or email <a href="mailto:examstash1@gmail.com">examstash1@gmail.com</a>.</p>
{FOOTER_HTML}
</main>
</body>
</html>"""
    with open("contact/index.html", "w", encoding="utf-8") as f:
        f.write(contact_head + "\n" + contact_body)

    # Privacy
    privacy_head = build_head(
        title="Privacy Policy — ExamStash",
        description="Privacy policy and data disclosures for ExamStash.",
        canonical_url="https://examstash.online/privacy/",
        extra_meta='<script async crossorigin="anonymous" src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-1741354477413638"></script>\n'
    )
    privacy_body = f"""<body>
<main>
<p class="college">Islamia College of Science &amp; Commerce, Srinagar</p>
<p class="bc"><a href="/">Home</a> › Privacy</p>
<h1>Privacy Policy</h1>
<p>ExamStash does not collect personal data or require accounts. Google AdSense and Google Analytics may use cookies to serve ads and analyze anonymous traffic.</p>
{FOOTER_HTML}
</main>
</body>
</html>"""
    with open("privacy/index.html", "w", encoding="utf-8") as f:
        f.write(privacy_head + "\n" + privacy_body)

    # Terms
    terms_head = build_head(
        title="Terms &amp; Disclaimer — ExamStash",
        description="Terms of service and non-affiliation disclaimer for ExamStash.",
        canonical_url="https://examstash.online/terms/",
        extra_meta='<script async crossorigin="anonymous" src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-1741354477413638"></script>\n'
    )
    terms_body = f"""<body>
<main>
<p class="college">Islamia College of Science &amp; Commerce, Srinagar</p>
<p class="bc"><a href="/">Home</a> › Terms</p>
<h1>Terms</h1>
<p>ExamStash is an independent student resource and is not affiliated with Islamia College of Science &amp; Commerce. All study materials are for educational reference.</p>
{FOOTER_HTML}
</main>
</body>
</html>"""
    with open("terms/index.html", "w", encoding="utf-8") as f:
        f.write(terms_head + "\n" + terms_body)

    # DMCA
    dmca_head = build_head(
        title="DMCA — ExamStash",
        description="DMCA and copyright policy for ExamStash.",
        canonical_url="https://examstash.online/dmca/",
        extra_meta='<script async crossorigin="anonymous" src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-1741354477413638"></script>\n'
    )
    dmca_body = f"""<body>
<main>
<p class="college">Islamia College of Science &amp; Commerce, Srinagar</p>
<p class="bc"><a href="/">Home</a> › DMCA</p>
<h1>DMCA</h1>
<p>If you believe content infringes your copyright, email <a href="mailto:examstash1@gmail.com">examstash1@gmail.com</a> or message on <a href="https://t.me/sahilsleem">Telegram</a> for prompt removal.</p>
{FOOTER_HTML}
</main>
</body>
</html>"""
    with open("dmca/index.html", "w", encoding="utf-8") as f:
        f.write(dmca_head + "\n" + dmca_body)

    # 404.html
    notfound_head = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Page Not Found — ExamStash</title>
<meta name="description" content="Page not found on ExamStash.">
<link rel="manifest" href="/manifest.json">
<meta name="theme-color" content="#ffffff">
<link rel="icon" type="image/svg+xml" href="/assets/icons/icon.svg">
<link rel="apple-touch-icon" href="/assets/icons/icon.svg">
<link rel="stylesheet" href="/style.css">
<script defer src="/assets/js/analytics.js"></script>
</head>"""
    notfound_body = f"""<body>
<main>
<p class="college">Islamia College of Science &amp; Commerce, Srinagar</p>
<h1>404</h1>
<p>Page not found. <a href="/">Return to home</a>.</p>
{FOOTER_HTML}
</main>
</body>
</html>"""
    with open("404.html", "w", encoding="utf-8") as f:
        f.write(notfound_head + "\n" + notfound_body)

    print("5. Syncing to islamia-college mirror...")
    for prog in PROGRAMMES:
        slug = prog["slug"]
        src = slug
        dst = os.path.join("islamia-college", slug)
        if os.path.exists(dst):
            shutil.rmtree(dst)
        shutil.copytree(src, dst)

    ic_terms_dir = os.path.join("islamia-college", "terms")
    os.makedirs(ic_terms_dir, exist_ok=True)
    with open(os.path.join(ic_terms_dir, "index.html"), "w", encoding="utf-8") as f:
        f.write(terms_head + "\n" + terms_body)

    ic_index_head = build_head(
        title="Islamia College of Science and Commerce — Past Papers & Syllabus",
        description="Download free previous year question papers and syllabus for Islamia College of Science and Commerce (ICSC) Srinagar.",
        canonical_url="https://examstash.online/islamia-college/",
        extra_meta='<script async crossorigin="anonymous" src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-1741354477413638"></script>\n'
    )
    ic_index_body = f"""<body>
<main>
<p class="college">Islamia College of Science &amp; Commerce, Srinagar</p>
<p class="bc"><a href="/">Home</a> › Islamia College</p>
<h1>Islamia College of Science &amp; Commerce</h1>
<input id="q" type="search" aria-label="Search programmes" placeholder="Search programme" autocomplete="off">
{chr(10).join(sections_html)}
{about_section_html}
{FOOTER_HTML}
</main>
<script>
var q=document.getElementById('q');
q.addEventListener('input',function(){{var v=q.value.toLowerCase().trim();
document.querySelectorAll('a.r').forEach(function(a){{a.hidden=!!v&&a.textContent.toLowerCase().indexOf(v)<0}});
document.querySelectorAll('section').forEach(function(s){{if(s.id==='about'){{s.hidden=!!v}}else{{s.hidden=!s.querySelector('a.r:not([hidden])')}}}})}});
</script>
</body>
</html>"""
    with open(os.path.join("islamia-college", "index.html"), "w", encoding="utf-8") as f:
        f.write(ic_index_head + "\n" + ic_index_body)

    print("\nAll HTML pages generated successfully!")

if __name__ == "__main__":
    main()
