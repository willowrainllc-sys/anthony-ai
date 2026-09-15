# --- Owned by Anthony Christopher Maestas | Directed by ARES ---
# --- EMPIRE MONETIZATION ARMOURING v1.0 ---
import os
from pathlib import Path

root = Path(r"C:\Users\willo\OneDrive\Desktop\Anthony_Ai")

# Real AdSense Configuration
REAL_ADSENSE_ID = "pub-9539640812310468"
PLACEHOLDER_ID = "ca-pub-OBSIDIAN_GLOBAL_ADSENSE"

def armour_monetization():
    print(f"[+] Armouring Empire Monetization Grid...")

    # 1. Update AdSense IDs in all HTML files
    targets = [root, root / "app" / "src" / "main" / "assets", root / "obsidian_edge_root"]

    html_count = 0
    for d in targets:
        if not d.exists(): continue
        for hf in d.rglob("*.html"):
            if "venv" in str(hf) or ".git" in str(hf): continue
            try:
                content = hf.read_text(encoding="utf-8", errors="ignore")
                if PLACEHOLDER_ID in content or "ca-pub-OBSIDIAN_GLOBAL_ADSENSE" in content:
                    content = content.replace(PLACEHOLDER_ID, f"ca-{REAL_ADSENSE_ID}")
                    content = content.replace("ca-pub-OBSIDIAN_GLOBAL_ADSENSE", f"ca-{REAL_ADSENSE_ID}")
                    hf.write_text(content, encoding="utf-8")
                    html_count += 1
            except Exception as e:
                print(f"[-] Error in {hf.name}: {e}")

    print(f"[+] ADSENSE: Injected real publisher ID into {html_count} pages.")

    # 2. Sync ads.txt to deployment targets
    ads_txt_src = root / "ads.txt"
    if ads_txt_src.exists():
        for d in [root / "app" / "src" / "main" / "assets", root / "obsidian_edge_root"]:
            if d.exists():
                import shutil
                shutil.copy2(ads_txt_src, d / "ads.txt")
        print("[+] ADS.TXT: Synchronized to all targets.")

if __name__ == "__main__":
    armour_monetization()