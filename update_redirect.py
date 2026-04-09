import re

with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

old_js = """    if (btnDecline) {
        btnDecline.addEventListener('click', (e) => {
            e.preventDefault();
            modalDiscount.classList.remove('atomicat-modal-active');
            setTimeout(() => {
                modalDiscount.style.display = 'none';
                modalSoldOut.style.display = 'block';
                setTimeout(() => modalSoldOut.classList.add('atomicat-modal-active'), 10);
            }, 300);
        });
    }"""

new_js = """    if (btnDecline) {
        btnDecline.addEventListener('click', (e) => {
            e.preventDefault();
            window.location.href = 'esgotado.html';
        });
    }"""

html = html.replace(old_js, new_js)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("index.html updated successfully with redirect.")
