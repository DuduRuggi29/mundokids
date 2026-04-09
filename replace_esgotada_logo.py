import re

with open("esgotado.html", "r", encoding="utf-8") as f:
    html = f.read()

new_img_tag = '<img loading="eager" fetchpriority="high" decoding="async" style="width: 100%; height: auto; max-width: 600px;" src="images/logokids.png" alt="Mundo Kids Logo">'

html = re.sub(r'<img [^>]*src="[^"]*RBPgtQ5755033\.png[^"]*"[^>]*>', new_img_tag, html)

with open("esgotado.html", "w", encoding="utf-8") as f:
    f.write(html)

print("Esgotado logo replaced.")
