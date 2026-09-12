# --- Built by Anthony Christopher | Est 12.19.1987 ---
# --- OBSIDIAN CITY GLOBAL SEO ARMOR FIX v1.0 ---
import os
import re
import glob

def fix_seo(file_path):
    if not os.path.exists(file_path):
        return

    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    # 1. Determine New Title based on Filename
    fn = os.path.basename(file_path).lower()
    title = "Obsidian City | Sovereign Cloud & Identity"

    if "index.html" in fn:
        title = "OBSIDIAN.CITY | The World's Best Wholesale Domain Registrar"
    elif "domain" in fn:
        title = "Register Domain Names | Obsidian City Wholesale Registrar"
    elif "hosting" in fn or "vps" in fn or "node" in fn:
        title = "Cloud Hosting & Edge VPS | Obsidian City"
    elif "llc" in fn or "incorporator" in fn:
        title = "LLC Formation & Business Identity | Obsidian City"
    elif "leo" in fn or "airo" in fn:
        title = "Obsidian Leo™ AI | Prompt to App Builder"
    elif "signin" in fn or "login" in fn or "auth" in fn or "register" in fn:
        title = "Secure Access | Obsidian City Account Manager"
    elif "checkout" in fn or "pay" in fn or "settle" in fn:
        title = "Secure Checkout | Obsidian City Global"
    elif "dashboard" in fn:
        title = "Account Dashboard | Obsidian City Manager"
    elif "help" in fn or "support" in fn:
        title = "Support Desk & Help Center | Obsidian City"

    # 2. Define Description
    description = "Obsidian City is the premier wholesale domain registrar and cloud edge provider. Get .com domains at cost, $39 LLC formation, and AI-powered app building."

    # 3. Perform Replacements in <head>
    # Remove old junk titles
    content = re.sub(r'<title>.*?</title>', f'<title>{title}</title>', content, flags=re.IGNORECASE | re.DOTALL)

    # Remove old junk descriptions/meta
    content = re.sub(r'<meta name="description" content=".*?">', '', content, flags=re.IGNORECASE)
    content = re.sub(r'<meta content=".*?" name="description">', '', content, flags=re.IGNORECASE)

    # Inject New Description after title
    new_meta = f'\n    <meta name="description" content="{description}"/>'
    content = content.replace(f'</title>', f'</title>{new_meta}')

    # 4. Global Cleanup of Jargon in content
    # (Careful not to break functional code, just cleaning visible text/meta)
    jargon = [
        "ANTHONY AI — Secure Access Gate",
        "Mission Hub // Access Gate",
        "AUTHENTICATE GRID",
        "BY ANTHONY CHRISTOPHER MAESTAS",
        "BY ANTHONY CHRISTOPHER",
        "Anthony Christopher Maestas |"
    ]
    for j in jargon:
        content = re.sub(re.escape(j), "Obsidian City Global", content, flags=re.IGNORECASE)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"✓ SEO Fixed: {file_path}")

def run_fix():
    # Targets: Root, Assets, Edge
    root_dir = r"C:\Users\willo\OneDrive\Desktop\Anthony_Ai"
    dirs = [
        root_dir,
        os.path.join(root_dir, "app", "src", "main", "assets"),
        os.path.join(root_dir, "obsidian_edge_root")
    ]

    for d in dirs:
        if os.path.exists(d):
            html_files = glob.glob(os.path.join(d, "*.html"))
            for hf in html_files:
                fix_seo(hf)

if __name__ == "__main__":
    run_fix()
