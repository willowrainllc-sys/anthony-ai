# --- Built by Anthony Christopher | Est 12.19.1987 ---
# --- EMPIRE SOCIAL MATRIX & CONNECTIONS v1.0 ---
import os
from pathlib import Path

root = Path(r"C:\Users\willo\OneDrive\Desktop\Anthony_Ai")

# 🔱 Professional Connection Links
SOCIAL_LINKS = {
    "X / Twitter": "https://x.com/willowrainllc",
    "GitHub": "https://github.com/willowrainllc-sys",
    "Discord": "https://discord.gg/obsidiancity",
    "Telegram": "https://t.me/obsidiancitymesh"
}

def update_social_links():
    print(f"🔱 Initiating Social Matrix Connection Protocol...")

    # Target all HTML files in root, app assets, and edge root
    dirs = [root, root / "app" / "src" / "main" / "assets", root / "obsidian_edge_root"]

    for d in dirs:
        if not d.exists(): continue
        print(f"[*] Armoring Social Matrix in: {d}")
        for file_path in d.glob("*.html"):
            try:
                content = file_path.read_text(encoding="utf-8", errors="ignore")
                original_content = content

                # 1. Update existing X/Twitter and GitHub links
                content = content.replace('<li><a href="#">X / Twitter</a></li>', f'<li><a href="{SOCIAL_LINKS["X / Twitter"]}" target="_blank">X / Twitter</a></li>')
                content = content.replace('<li><a href="#">GitHub</a></li>', f'<li><a href="{SOCIAL_LINKS["GitHub"]}" target="_blank">GitHub</a></li>')

                # 2. Add extra connections if they don't exist
                if '<li><a href="#">GitHub</a></li>' not in content and SOCIAL_LINKS["GitHub"] in content:
                    if 'Discord' not in content:
                        content = content.replace(f'<li><a href="{SOCIAL_LINKS["GitHub"]}" target="_blank">GitHub</a></li>',
                                               f'<li><a href="{SOCIAL_LINKS["GitHub"]}" target="_blank">GitHub</a></li>\n                        <li><a href="{SOCIAL_LINKS["Discord"]}" target="_blank">Discord Community</a></li>\n                        <li><a href="{SOCIAL_LINKS["Telegram"]}" target="_blank">Telegram Mesh</a></li>')

                if content != original_content:
                    file_path.write_text(content, encoding="utf-8")
                    print(f"[+] Connected: {file_path.name}")
            except Exception as e:
                print(f"[-] Error in {file_path.name}: {e}")

if __name__ == "__main__":
    update_social_links()
