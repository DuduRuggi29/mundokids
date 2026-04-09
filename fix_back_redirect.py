import re

with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

# Replace the hidden back-redirect URL
html = html.replace("https://turminhaalfakids.online/esgotada/", "esgotado.html")

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("index.html updated successfully with local back-redirect.")
