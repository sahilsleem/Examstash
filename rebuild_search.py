import os
import json
import re

def rebuild_search():
    index_entries = []
    
    # Exclude system and static folders
    excluded_dirs = {".git", "assets", "scratch", "islamia-college", "about", "contact", "privacy", "terms", "dmca"}
    
    # Discover courses from directories
    course_dirs = sorted([d for d in os.listdir(".") if os.path.isdir(d) and d not in excluded_dirs])
    
    for course_slug in course_dirs:
        course_index = os.path.join(course_slug, "index.html")
        course_name = course_slug.replace("-", " ").title()
        if os.path.exists(course_index):
            try:
                with open(course_index, "r", encoding="utf-8") as cf:
                    c_content = cf.read()
                    m_cname = re.search(r'<title>(.*?)—', c_content)
                    if m_cname:
                        course_name = m_cname.group(1).replace("Past Papers & Syllabus", "").replace("Past Papers &amp; Syllabus", "").strip()
            except Exception:
                pass
                
        for sem in range(1, 7):
            sem_dir = os.path.join(course_slug, f"semester-{sem}")
            if not os.path.isdir(sem_dir):
                continue
                
            for entry in sorted(os.listdir(sem_dir)):
                paper_dir = os.path.join(sem_dir, entry)
                if not os.path.isdir(paper_dir):
                    continue
                    
                idx_file = os.path.join(paper_dir, "index.html")
                if not os.path.exists(idx_file):
                    continue
                    
                with open(idx_file, "r", encoding="utf-8") as f:
                    content = f.read()
                    
                m_title = re.search(r'<div class="file-title">(.*?)</div>', content) or re.search(r'<h1[^>]*>(.*?)</h1>', content)
                m_desc = re.search(r'<meta\s+name=["\']description["\']\s+content=["\'](.*?)["\']', content) or re.search(r'<meta\s+content=["\'](.*?)["\']\s+name=["\']description["\']', content)
                
                if m_title:
                    title = m_title.group(1).strip()
                    desc = m_desc.group(1).strip() if m_desc else ""
                    
                    keywords = f"{title} {course_slug} {course_name} semester {sem} {entry}".lower()
                    
                    # Primary path only (107 unique resources)
                    index_entries.append({
                        "title": title,
                        "url": f"/{course_slug}/semester-{sem}/{entry}/",
                        "category": course_name,
                        "description": desc,
                        "keywords": keywords
                    })
                    
    # Generate JSON string
    json_str = json.dumps(index_entries, indent=2)
    
    js_content = f"// ExamStash In-Memory Search Index\nwindow.EXAMSTASH_SEARCH_INDEX = {json_str};\n"
    
    with open("assets/js/search-index.js", "w", encoding="utf-8") as f:
        f.write(js_content)
        
    print(f"Search index rebuilt with {len(index_entries)} primary entries.")

if __name__ == "__main__":
    rebuild_search()

