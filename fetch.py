import os
import re
import urllib.request
import json

base_url = "https://turminha-alfakids.online/"

with open("index.html", "r", encoding="utf-8") as f:
    html_content = f.read()

# Find URLs in src=, href=, url()
# Also find them in srcset (things like images/xxx.png#123 300w)
# For srcset, it's easier to just pick anything that starts with images/, js/, fonts/
urls = set()

# Regex to catch (js/...), (images/...), (fonts/...)
for match in re.findall(r'(images/[a-zA-Z0-9_\-\.\#]+)', html_content):
    urls.add(match)
for match in re.findall(r'(js/[a-zA-Z0-9_\-\.\#]+)', html_content):
    urls.add(match)
for match in re.findall(r'(fonts/[a-zA-Z0-9_\-\.\#]+)', html_content):
    urls.add(match)
# Also some links might be plain without #
for match in re.findall(r'(?:href|src)="([^"]+)"', html_content):
    if not match.startswith("http") and not match.startswith("data:") and not match.startswith("javascript:") and not match.startswith("#"):
        urls.add(match)

def download(url_path):
    # url_path might have # in it, we need to download from the base URL without #
    clean_path = url_path.split("#")[0]
    full_url = base_url + clean_path
    
    if not clean_path:
        return
        
    os.makedirs(os.path.dirname(clean_path), exist_ok=True)
    
    if os.path.exists(clean_path) and os.path.getsize(clean_path) > 0:
        return
        
    try:
        req = urllib.request.Request(full_url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response, open(clean_path, 'wb') as out_file:
            data = response.read()
            out_file.write(data)
            print(f"Downloaded {clean_path}")
    except Exception as e:
        print(f"Failed to download {clean_path}: {e}")

for u in urls:
    download(u)

print("Done downloading assets.")
