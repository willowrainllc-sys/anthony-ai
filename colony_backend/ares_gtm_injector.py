# --- Owned by Anthony Christopher Maestas | Directed by ARES ---
# --- ARES GTM CONTAINER INJECTOR v1.0 ---
import os
from pathlib import Path

GTM_ID = "GTM-MHCNLC5"

HEAD_SNIPPET = f"""<!-- Google Tag Manager -->
<script>(function(w,d,s,l,i){{w[l]=w[l]||[];w[l].push({{'gtm.start':
new Date().getTime(),event:'gtm.js'}});var f=d.getElementsByTagName(s)[0],
j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
}})(window,document,'script','dataLayer','{GTM_ID}');</script>
<!-- End Google Tag Manager -->"""

BODY_SNIPPET = f"""<!-- Google Tag Manager (noscript) -->
<noscript><iframe src="https://www.googletagmanager.com/ns.html?id={GTM_ID}"
height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>
<!-- End Google Tag Manager (noscript) -->"""

def inject_gtm():
    root = Path(r"C:\Users\willo\OneDrive\Desktop\Anthony_Ai")
    count = 0
    for html_file in root.rglob("*.html"):
        if "venv" in str(html_file) or ".git" in str(html_file):
            continue
        try:
            content = html_file.read_text(encoding="utf-8", errors="ignore")
            if GTM_ID in content:
                continue

            modified = False
            # Inject in <head>
            if "<head>" in content and HEAD_SNIPPET not in content:
                content = content.replace("<head>", f"<head>\n{HEAD_SNIPPET}", 1)
                modified = True

            # Inject after <body>
            if "<body>" in content and BODY_SNIPPET not in content:
                content = content.replace("<body>", f"<body>\n{BODY_SNIPPET}", 1)
                modified = True

            if modified:
                html_file.write_text(content, encoding="utf-8")
                count += 1
        except Exception as e:
            pass

    print(f"[+] ARES GTM INJECTOR: Successfully injected {GTM_ID} into {count} HTML files.")

if __name__ == "__main__":
    inject_gtm()
