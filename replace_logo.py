import re

with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

# The hero image has src="images/RBPgtQ5755033.png#365487"
# We match the <img ...> tag with this src and replace it
new_img_tag = '<img loading="eager" fetchpriority="high" decoding="async" style="width: 100%; height: auto; max-width: 600px;" src="images/logokids.png" alt="Mundo Kids Logo">'

html = re.sub(r'<img [^>]*src="images/RBPgtQ5755033\.png[^>]*>', new_img_tag, html)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("Logo replaced.")
