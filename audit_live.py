import urllib.request
import time

urls = [
    'https://examstash.online/',
    'https://examstash.online/bsc-physics/',
    'https://examstash.online/common-courses/'
]

for url in urls:
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        start = time.time()
        with urllib.request.urlopen(req, timeout=10) as response:
            html = response.read().decode('utf-8')
            status = response.status
        duration = time.time() - start
        
        print(f'\n--- {url} (Status: {status}, Time: {duration:.2f}s) ---')
        
        if url == 'https://examstash.online/':
            print('Has icon.svg?', 'icon.svg' in html)
            print('Has bsc-physics link?', 'href="/bsc-physics/"' in html)
            
        elif url == 'https://examstash.online/common-courses/':
            print('Has semester-1?', 'href="/common-courses/semester-1/"' in html)
            print('Has semester-4?', 'href="/common-courses/semester-4/"' in html)
            
    except Exception as e:
        print(f'Error fetching {url}: {e}')
