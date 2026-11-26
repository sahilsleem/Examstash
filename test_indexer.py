import os
import re
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

def format_count(papers, syllabi):
    parts = []
    if papers > 0:
        parts.append(f"{papers} paper" if papers == 1 else f"{papers} papers")
    if syllabi > 0:
        parts.append(f"{syllabi} syllabus" if syllabi == 1 else f"{syllabi} syllabi")
    return " · ".join(parts)

data = {}
total_papers = 0
total_syllabi = 0

for prog in PROGRAMMES:
    slug = prog["slug"]
    prog_data = {"semesters": {}, "total_papers": 0, "total_syllabi": 0}
    
    for sem in prog["semesters"]:
        sem_path = os.path.join(slug, sem)
        sem_data = {"papers": [], "syllabi": []}
        
        if os.path.exists(sem_path):
            # Check existing semester index.html
            sem_index_file = os.path.join(sem_path, "index.html")
            
            # Subdirectories
            subdirs = sorted([d for d in os.listdir(sem_path) if os.path.isdir(os.path.join(sem_path, d))])
            for d in subdirs:
                sub_index = os.path.join(sem_path, d, "index.html")
                if os.path.exists(sub_index):
                    with open(sub_index, "r", encoding="utf-8") as f:
                        c = f.read()
                    
                    soup = BeautifulSoup(c, "html.parser")
                    h1_tag = soup.find("h1")
                    title = h1_tag.get_text().strip() if h1_tag else d.replace("-", " ").title()
                    
                    m_drive = re.search(r'href=[\x22\x27](https://drive\.google\.com/[^\x22\x27\s>]+)[\x22\x27]', c)
                    drive_link = m_drive.group(1) if m_drive else "#"
                    
                    is_syllabus = "syllabus" in d.lower()
                    
                    item = {
                        "slug": d,
                        "title": title,
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
    total_papers += prog_data["total_papers"]
    total_syllabi += prog_data["total_syllabi"]
    print(f"{slug}: {prog_data['total_papers']} papers, {prog_data['total_syllabi']} syllabi -> '{prog_data['count_str']}'")

print(f"\nTOTAL: {total_papers} papers, {total_syllabi} syllabi")
