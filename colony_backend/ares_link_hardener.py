# --- Owned by Anthony Christopher Maestas | Directed by ARES ---
# --- ARES LINK HARDENER: GLOBAL DIRECTIVE WIRING v1.4 ---
import os
import re
from pathlib import Path

def harden_links(path):
    if not path.exists(): return
    content = path.read_text(encoding='utf-8', errors='ignore')
    old_content = content

    # 🔱 1. Map all legacy payment/checkout variants
    # Use word boundaries to prevent multi-nested replacement
    content = re.sub(r'\bGlobal_payout_gate\.html\b', 'obsidian_unified_checkout.html', content, flags=re.IGNORECASE)
    content = re.sub(r'\bsovereign_payout_gate\.html\b', 'obsidian_unified_checkout.html', content, flags=re.IGNORECASE)
    content = re.sub(r'\bcheckout\.html\b', 'obsidian_unified_checkout.html', content, flags=re.IGNORECASE)

    # 🔱 2. EXTREME CLEANUP: Fix multi-nested dashboard/checkout strings
    # This regex recursively collapses sequences like obsidian_unified_obsidian_unified_checkout.html
    # into a single obsidian_unified_checkout.html
    content = re.sub(r'(obsidian_unified_)+checkout\.html', 'obsidian_unified_checkout.html', content)
    content = re.sub(r'(obsidian_city_)+dashboard\.html', 'obsidian_city_dashboard.html', content)

    # 🔱 3. Fix partial hrefs (e.g. href="checkout?...")
    content = re.sub(r'href=["\'](?!obsidian_unified_checkout\.html)checkout\?', 'href="obsidian_unified_checkout.html?', content, flags=re.IGNORECASE)
    content = re.sub(r'href=["\'](?!obsidian_city_dashboard\.html)dashboard\?', 'href="obsidian_city_dashboard.html?', content, flags=re.IGNORECASE)

    # 🔱 4. Map legacy variants
    content = content.replace('dashboard.html', 'obsidian_city_dashboard.html')
    content = content.replace('pay_landing.html', 'obsidian_pay_hub.html')

    # 🔱 5. Rebrand 'Blackhole' data points to 'Obsidian Deep'
    content = content.replace('blackhole', 'obsidian_deep')
    content = content.replace('Black Hole', 'Obsidian Deep Access')

    if content != old_content:
        path.write_text(content, encoding='utf-8')
        print(f"[+] Hardened: {path}")

if __name__ == "__main__":
    root = Path(r"C:\Users\willo\OneDrive\Desktop\Anthony_Ai")
    targets = list(root.glob("*.html")) + \
              list((root / "obsidian_edge_root").glob("*.html")) + \
              list((root / "app/src/main/assets").glob("*.html"))

    for t in targets:
        harden_links(t)

    print("\n🔱 GLOBAL LINK HARDENING COMPLETE. ALL DIRECTIVES ARMORED.")
