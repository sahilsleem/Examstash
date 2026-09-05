import os
import json
import re

def rebuild_search():
    index_entries = []
    
    # We want to scan all course directories and semester subdirectories
    courses = []
    with open('scratch/courses.txt', 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split('|')
            if len(parts) >= 3:
                courses.append((parts[0], parts[2]))
                
    for course_slug, course_name in courses:
        for sem in range(1, 7):
            sem_dir = os.path.join(course_slug, f"semester-{sem}")
            if not os.path.isdir(sem_dir):
                continue
                
            for entry in os.listdir(sem_dir):
                paper_dir = os.path.join(sem_dir, entry)
                if not os.path.isdir(paper_dir):
                    continue
                    
                idx_file = os.path.join(paper_dir, "index.html")
                if not os.path.exists(idx_file):
                    continue
                    
                with open(idx_file, "r", encoding="utf-8") as f:
                    content = f.read()
                    
                m_title = re.search(r'<div class="file-title">(.*?)</div>', content)
                m_desc = re.search(r'<meta name="description" content="(.*?)"', content)
                
                if m_title:
                    title = m_title.group(1).strip()
                    desc = m_desc.group(1).strip() if m_desc else ""
                    
                    keywords = f"{title} {course_slug} {course_name} semester {sem}".lower()
                    
                    # Original path
                    index_entries.append({
                        "title": title,
                        "url": f"/{course_slug}/semester-{sem}/{entry}/",
                        "category": course_name,
                        "description": desc,
                        "keywords": keywords
                    })
                    
                    # Mirror path
                    index_entries.append({
                        "title": title,
                        "url": f"/islamia-college/{course_slug}/semester-{sem}/{entry}/",
                        "category": course_name,
                        "description": desc,
                        "keywords": keywords + " islamia college"
                    })
                    
    # Generate JSON string
    json_str = json.dumps(index_entries, indent=2)
    
    js_content = f"// Islamia College Portal In-Memory Search Index\nwindow.EXAMSTASH_SEARCH_INDEX = {json_str};\n"
    
    with open("assets/js/search-index.js", "w", encoding="utf-8") as f:
        f.write(js_content)
        
    print(f"Search index rebuilt with {len(index_entries)} entries.")

if __name__ == "__main__":
    rebuild_search()
