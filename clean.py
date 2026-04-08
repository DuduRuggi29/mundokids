import re

with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

# 1. Remove pixel script
html = re.sub(r'<script>window\.pixelId = ".*?";.*?document\.head\.appendChild\(a\);</script>', '', html, flags=re.DOTALL)
html = re.sub(r'<script async="" defer="" src="js/pixel\.js"></script>', '', html)

# 2. Remove UTM / Latest
html = re.sub(r'<script src="js/latest\.js" data-utmify-[^>]+></script>', '', html)

# 3. Remove Facivon
html = re.sub(r'<link rel="shortcut icon" type="image/png" href="images/[^"]+\.png">', '', html)

# 4. Replace links to payment
html = re.sub(r'href="https://pay\.kirvano\.com/[^"]+"', 'href="#"', html)

# 5. Names
html = html.replace('Turminha Alfa Kids', 'Mundo Kids')
html = html.replace('Kit Alfa Kids', 'Kit Mundo Kids')
html = html.replace('Alfa Kids', 'Mundo Kids')
html = html.replace('Turminha', 'Mundo')

# 6. Offer funnel modification
# Find the button for "Oferta Básica" -> "Adquirir o Kit Básico"
# It currently has: <a href="javascript:void(0)" class="a-btn a-g-m-t a-b-b"><span>Adquirir o Kit Básico</span></a>
# Let's change its class to hook it: id="btn-basic-offer"
html = html.replace(
    'class="a-btn a-g-m-t a-b-b"><span>Adquirir o Kit Básico</span></a>',
    'class="a-btn a-g-m-t a-b-b" id="btn-basic-offer"><span>Adquirir o Kit Básico</span></a>'
)

# Modal HTML templates for our custom funnel
modals_html = """
<div id="modal-discount" class="atomicat-modal-overlay">
  <div class="atomicat-modal atomicat-modal-active" style="background: rgba(0,0,0,0.8); display: flex; justify-content: center; align-items: center;">
    <div style="background: white; padding: 30px; border-radius: 10px; max-width: 500px; text-align: center;">
      <h2 style="font-family: Poppins; color: #ec7124;">ESPERE! 🛑</h2>
      <p style="font-family: Poppins; font-size: 18px; margin: 20px 0;">Você tem certeza que quer apenas o pacote básico?</p>
      <p style="font-family: Poppins; font-size: 16px; margin: 20px 0;">Leve o <b>Pacote Completo</b> agora mesmo com um <b>Desconto Exclusivo</b>!</p>
      <div style="display: flex; gap: 10px; justify-content: center; flex-direction: column;">
        <a href="#" style="background: #337915; color: white; padding: 15px; border-radius: 5px; font-weight: bold; text-decoration: none; font-family: Poppins;">SIM! QUERO O PACOTE COMPLETO!</a>
        <a href="#" id="btn-decline-discount" style="background: #ccc; color: #333; padding: 15px; border-radius: 5px; font-weight: bold; text-decoration: none; font-family: Poppins;">Não, obrigado. Quero apenas o básico.</a>
      </div>
    </div>
  </div>
</div>

<div id="modal-sold-out" class="atomicat-modal-overlay">
  <div class="atomicat-modal atomicat-modal-active" style="background: rgba(0,0,0,0.8); display: flex; justify-content: center; align-items: center;">
    <div style="background: white; padding: 30px; border-radius: 10px; max-width: 500px; text-align: center;">
      <h2 style="font-family: Poppins; color: red;">ESGOTADO! 😔</h2>
      <p style="font-family: Poppins; font-size: 18px; margin: 20px 0;">Infelizmente, o Kit Básico acabou de <b>esgotar</b>.</p>
      <p style="font-family: Poppins; font-size: 16px; margin: 20px 0;">Nesse momento os nossos estoques/vagas promocionais da Oferta Básica terminaram. Mas você ainda pode levar o pacote completo.</p>
      <div style="display: flex; gap: 10px; justify-content: center;">
        <button id="btn-close-sold-out" style="background: #ec7124; color: white; padding: 15px; border-radius: 5px; font-weight: bold; width: 100%; font-family: Poppins;">VOLTAR E VER O PACOTE COMPLETO</button>
      </div>
    </div>
  </div>
</div>

<script>
document.addEventListener('DOMContentLoaded', () => {
    const btnBasic = document.getElementById('btn-basic-offer');
    const modalDiscount = document.getElementById('modal-discount');
    const btnDecline = document.getElementById('btn-decline-discount');
    const modalSoldOut = document.getElementById('modal-sold-out');
    const btnCloseSoldOut = document.getElementById('btn-close-sold-out');

    // Initially hide modals
    modalDiscount.style.display = 'none';
    modalDiscount.classList.remove('atomicat-modal-active');
    
    modalSoldOut.style.display = 'none';
    modalSoldOut.classList.remove('atomicat-modal-active');

    if (btnBasic) {
        btnBasic.addEventListener('click', (e) => {
            e.preventDefault();
            e.stopPropagation();
            modalDiscount.style.display = 'block';
            setTimeout(() => modalDiscount.classList.add('atomicat-modal-active'), 10);
        });
    }

    if (btnDecline) {
        btnDecline.addEventListener('click', (e) => {
            e.preventDefault();
            modalDiscount.classList.remove('atomicat-modal-active');
            setTimeout(() => {
                modalDiscount.style.display = 'none';
                modalSoldOut.style.display = 'block';
                setTimeout(() => modalSoldOut.classList.add('atomicat-modal-active'), 10);
            }, 300);
        });
    }

    if (btnCloseSoldOut) {
        btnCloseSoldOut.addEventListener('click', (e) => {
            e.preventDefault();
            modalSoldOut.classList.remove('atomicat-modal-active');
            setTimeout(() => {
                modalSoldOut.style.display = 'none';
            }, 300);
        });
    }
});
</script>
</body>
"""

html = html.replace("</body>", modals_html)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("Cleanup complete.")
