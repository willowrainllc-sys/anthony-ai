# --- Built by Anthony Christopher | Est 12.19.1987 ---
# --- GLOBAL LINK REPAIR v2.0 ---
import os
from pathlib import Path

root = Path(r"C:\Users\willo\OneDrive\Desktop\Anthony_Ai")
mappings = {
    "/domains": "obsidian_domains.html",
    "/vps": "obsidian_vps_hosting.html",
    "/leo": "obsidian_leo_builder.html",
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

def fix_html_files():
    # Process Root, app/src/main/assets, and obsidian_edge_root
    dirs = [root, root / "app" / "src" / "main" / "assets", root / "obsidian_edge_root"]

    for d in dirs:
        if not d.exists(): continue
        print(f"[*] Scanning: {d}")
        for hf in d.glob("*.html"):
            try:
                content = hf.read_text(encoding="utf-8", errors="ignore")
                modified = False
                for old, new in mappings.items():
                    # Handle double and single quotes
                    for q in ['"', "'"]:
                        target = f'href={q}{old}{q}'
                        replacement = f'href={q}{new}{q}'
                        if target in content:
                            content = content.replace(target, replacement)
                            modified = True

                if modified:
                    hf.write_text(content, encoding="utf-8")
                    print(f"✓ Fixed links in {hf.relative_to(root)}")
            except Exception as e:
                print(f"[-] Error fixing {hf}: {e}")

if __name__ == "__main__":
    fix_html_files()
