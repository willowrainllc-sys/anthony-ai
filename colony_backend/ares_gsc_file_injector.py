# --- Owned by Anthony Christopher Maestas | Directed by ARES ---
# --- ARES GSC AUTOMATED HTML FILE INJECTOR ---
import os
import sys
from pathlib import Path

ROOT = Path(r"C:\Users\willo\OneDrive\Desktop\Anthony_Ai")
sys.path.append(str(ROOT / "colony_backend"))

try:
    from colony_logger import colony_log
except ImportError:
    def colony_log(msg, node="SUPREME"):
        print(f"[{node}] {msg}")

def inject_verification_file(filename: str, content: str):
    root_dir = ROOT
    assets_dir = root_dir / "app" / "src" / "main" / "assets"

    # Target 1: Root directory
    file_root = root_dir / filename
    file_root.write_text(content, encoding="utf-8")
    colony_log(f"[+] ARES GSC: Injected verification file to root -> {file_root}", node="SUPREME")

    # Target 2: Android assets directory
    if assets_dir.exists():
        file_assets = assets_dir / filename
        file_assets.write_text(content, encoding="utf-8")
        colony_log(f"[+] ARES GSC: Injected verification file to assets -> {file_assets}", node="SUPREME")

    print(f"\n" + "="*70)
    print(f"  [+] ARES GSC FILE INJECTOR SUCCESS")
    print(f"  FILE: {filename}")
    print(f"  ACCESSIBLE AT: https://obsidian.city/{filename}")
    print("="*70 + "\n")

if __name__ == "__main__":
    inject_verification_file('googlefd67afcebf544c01.html', 'google-site-verification: googlefd67afcebf544c01.html')
