import os

pixel = """
<!-- Meta Pixel Code -->
<script>
!function(f,b,e,v,n,t,s)
{if(f.fbq)return;n=f.fbq=function(){n.callMethod?
n.callMethod.apply(n,arguments):n.queue.push(arguments)};
if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';
n.queue=[];t=b.createElement(e);t.async=!0;
t.src=v;s=b.getElementsByTagName(e)[0];
s.parentNode.insertBefore(t,s)}(window, document,'script',
'https://connect.facebook.net/en_US/fbevents.js');
fbq('init', '1658938005229618');
fbq('track', 'PageView');
fbq('track', 'ViewContent');
</script>
<noscript><img height="1" width="1" style="display:none"
src="https://www.facebook.com/tr?id=1658938005229618&ev=PageView&noscript=1"
/></noscript>
<!-- End Meta Pixel Code -->
</head>"""

files = ["index.html", "esgotado.html"]
for f in files:
    with open(f, "r", encoding="utf-8") as file:
        content = file.read()
    content = content.replace("</head>", pixel)
    with open(f, "w", encoding="utf-8") as file:
        file.write(content)

print("Pixel added with ViewContent.")
