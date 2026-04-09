import os
import re
import urllib.request

base_url = "https://turminha-alfakids.online/"
esgotada_url = "https://turminhaalfakids.online/esgotada/"

try:
    req = urllib.request.Request(esgotada_url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req) as response:
        html = response.read().decode('utf-8', errors='ignore')
except Exception as e:
    print(f"Failed to fetch {esgotada_url}: {e}")
    html = ""

if html:
    # 1. Clean trackings
    html = re.sub(r'<script>window\.pixelId = ".*?";.*?document\.head\.appendChild\(a\);</script>', '', html, flags=re.DOTALL)
    html = re.sub(r'<script async="" defer="" src=".*?pixel\.js"></script>', '', html)
    html = re.sub(r'<script src=".*?latest\.js" data-utmify-[^>]+></script>', '', html)
    html = re.sub(r'<link rel="shortcut icon"[^>]*>', '', html)
    html = re.sub(r'href="https://pay\.kirvano\.com/[^"]+"', 'href="#"', html)

    # 2. Anonymize/Rebranding
    html = html.replace('Turminha Alfa Kids', 'Mundo Kids')
    html = html.replace('Kit Alfa Kids', 'Kit Mundo Kids')
    html = html.replace('Alfa Kids', 'Mundo Kids')
    html = html.replace('Turminha', 'Mundo')
    
    # Check if the page has a hero image that should be logokids.png
    # The esgotada page might also have the same logo
    # For a generic catch: we won't assume logo exists, but we can replace if needed.

    # 3. Find unique assets and download
    urls = set()
    for match in re.findall(r'(images/[a-zA-Z0-9_\-\.\#]+)', html):
        urls.add(match)
    for match in re.findall(r'(js/[a-zA-Z0-9_\-\.\#]+)', html):
        urls.add(match)
    for match in re.findall(r'(fonts/[a-zA-Z0-9_\-\.\#]+)', html):
        urls.add(match)
    def download(url_path):
        clean_path = url_path.split("#")[0].strip('/')
        full_url = base_url + clean_path
        if not clean_path.strip(): return
        os.makedirs(os.path.dirname(clean_path), exist_ok=True)
        if os.path.exists(clean_path) and os.path.getsize(clean_path) > 0: return
        try:
            req2 = urllib.request.Request(full_url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req2) as resp, open(clean_path, 'wb') as out_file:
                out_file.write(resp.read())
                print(f"Downloaded {clean_path}")
        except Exception as err:
            print(f"Failed to fetch {full_url}: {err}")

    for u in urls:
        download(u)

    # 4. Save cleaned HTML
    with open("esgotado.html", "w", encoding="utf-8") as f:
        f.write(html)
        
    print("Esgotada page cloned and cleaned successfully.")
