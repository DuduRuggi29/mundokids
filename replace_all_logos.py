import re

files = ["index.html", "esgotado.html"]

logo_tag = '<img loading="eager" fetchpriority="high" decoding="async" style="width: 100%; height: auto; max-width: 600px;" src="images/logokiki.png" alt="Mundo Kids Logo">'

for fname in files:
    with open(fname, "r", encoding="utf-8") as f:
        html = f.read()
        
    html = re.sub(r'<img [^>]*RBPgtQ5755033[^>]*>', logo_tag, html)
    html = re.sub(r'<img [^>]*logokids\.png[^>]*>', logo_tag, html)
    
    fav_tag = '<link rel="shortcut icon" type="image/png" href="images/logokiki.png">'
    if 'rel="shortcut icon"' in html:
        html = re.sub(r'<link rel="shortcut icon"[^>]*>', fav_tag, html)
    else:
        html = html.replace("</head>", fav_tag + "</head>")

    with open(fname, "w", encoding="utf-8") as f:
        f.write(html)
        
print("All instances replaced.")
