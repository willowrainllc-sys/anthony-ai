# --- Owned by Anthony Christopher Maestas | Directed by ARES ---
# --- GLOBAL LINK REPAIR v5.0 (Absolute to Relative) ---
import os
from pathlib import Path

root = Path(r"C:\Users\willo\OneDrive\Desktop\Anthony_Ai")

# Mappings for Clean URLs to HTML Files
clean_url_mappings = {
    "/domains": "obsidian_domains.html",
    "/vps": "obsidian_vps_hosting.html",
    "/anthony_ai_supreme": "obsidian_anthony_ai_supreme_builder.html",
    "/llc": "obsidian_llc_formation.html",
    "/signin": "obsidian_signin.html",
    "/register": "obsidian_register.html",
    "/checkout": "obsidian_unified_checkout.html",
    "/dashboard": "obsidian_city_dashboard.html",
    "/profile": "obsidian_user_profile.html",
    "/help": "obsidian_help_center.html",
    "/developer": "developer.html",
    "/about": "obsidian_city_dashboard.html",
    "/terms": "terms.html",
    "/privacy": "privacy.html"
}

def repair_links():
    dirs = [root, root / "app" / "src" / "main" / "assets", root / "obsidian_edge_root"]

    for d in dirs:
        if not d.exists(): continue
        print(f"[*] Scanning for link repair in: {d}")
        for hf in d.rglob("*.html"):
            if ".git" in str(hf) or "venv" in str(hf) or "__pycache__" in str(hf): continue
            try:
                content = hf.read_text(encoding="utf-8", errors="ignore")
                original_content = content

                # 1. Fix Absolute Assets (e.g. href="/assets/...")
                content = content.replace('href="/assets/', 'href="assets/')
                content = content.replace('src="/assets/', 'src="assets/')

                # 2. Fix Clean URL routes
                for old, new in clean_url_mappings.items():
                    for q in ['"', "'"]:
                        # Match href="/path" or href="/path/"
                        targets = [f'href={q}{old}{q}', f'href={q}{old}/{q}']
                        replacement = f'href={q}{new}{q}'
                        for t in targets:
                            if t in content:
                                content = content.replace(t, replacement)

                # 3. Fix auth/callback specifically
                content = content.replace('href="/auth/callback', 'href="obsidian_auth_callback.html')

                if content != original_content:
                    hf.write_text(content, encoding="utf-8")
                    print(f"[+] Repaired: {hf.relative_to(root)}")
            except Exception as e:
                print(f"[-] Error in {hf}: {e}")

if __name__ == "__main__":
    repair_links()