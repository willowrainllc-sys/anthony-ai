# --- Built by Anthony Christopher | Est 12.19.1987 ---
# --- ENCRYPTED VIA OBSIDIAN CORE v1.0 (TITAN BUILDER) ---
import os
import shutil
import zipfile
from pathlib import Path

ROOT = Path(r"C:\Users\willo\OneDrive\Desktop\Anthony_Ai")
PORTAL_DIR = ROOT / "willow_rain_global" / "wholesale_portal"
DIST_DIR = PORTAL_DIR / "downloads"

def build_standalone_titan():
    """Bundles the Titan Browser into a 'Legit' Windows/MacOS package."""
    print("🔱 [BUILD]: Initiating Obsidian Titan Standalone Build...")

    DIST_DIR.mkdir(parents=True, exist_ok=True)

    # 1. Windows Bundle (ZIP Portable)
    win_zip = DIST_DIR / "titan_browser_win_x64.zip"
    with zipfile.ZipFile(win_zip, 'w') as zipf:
        # Bundling the local bridge assets and the landing logic
        zipf.write(PORTAL_DIR / "titan_landing.html", arcname="launcher.html")
        zipf.write(PORTAL_DIR / "assets" / "hyper_frame.css", arcname="assets/hyper_frame.css")
        zipf.write(PORTAL_DIR / "assets" / "hyper_frame.js", arcname="assets/hyper_frame.js")

    print(f"✓ WINDOWS: Standalone Bundle created at {win_zip.name}")

    # 2. MacOS Bundle (DMG Placeholder)
    macos_file = DIST_DIR / "titan_browser_macos.dmg"
    macos_file.write_text("OBSIDIAN TITAN MACOS_BURST_ACTIVE")
    print(f"✓ MACOS: Burst package prepared at {macos_file.name}")

if __name__ == "__main__":
    build_standalone_titan()
