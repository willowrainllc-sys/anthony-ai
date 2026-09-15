# --- Owned by Anthony Christopher Maestas | Directed by ARES ---
from pathlib import Path

root = Path(r'C:\Users\willo\OneDrive\Desktop\Anthony_Ai')
mappings = {
    'href="/domains"': 'href="obsidian_domains.html"',
    'href="/vps"': 'href="obsidian_vps_hosting.html"',
    'href="/anthony_ai_supreme"': 'href="obsidian_anthony_ai_supreme_builder.html"',
    'href="/llc"': 'href="obsidian_llc_formation.html"',
    'href="/signin"': 'href="obsidian_signin.html"',
    'href="/checkout"': 'href="obsidian_unified_checkout.html"',
    'href="checkout?"': 'href="obsidian_unified_checkout.html?"',
    'href="/register"': 'href="obsidian_register.html"',
    'href="/dashboard"': 'href="obsidian_city_dashboard.html"',
    'href="/profile"': 'href="obsidian_user_profile.html"',
    'href="/help"': 'href="obsidian_help_center.html"',
    'href="/developer"': 'href="developer.html"',
    'href="/about"': 'href="obsidian_city_dashboard.html"',
    'href="/terms"': 'href="terms.html"',
    'href="/privacy"': 'href="privacy.html"'
}

def sync_links():
    for path in root.rglob('*.html'):
        if '.git' in str(path) or 'venv' in str(path): continue
        try:
            content = path.read_text(encoding='utf-8', errors='ignore')
            modified = False
            for old, new in mappings.items():
                if old in content:
                    content = content.replace(old, new)
                    modified = True

            if modified:
                path.write_text(content, encoding='utf-8')
                print(f"[+] Fixed links: {path.relative_to(root)}")
        except Exception as e:
            print(f"[-] Error in {path}: {e}")

if __name__ == "__main__":
    sync_links()