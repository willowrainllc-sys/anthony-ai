import shutil
import os
from pathlib import Path

# Paths
ROOT = Path(r"C:\Users\willo\OneDrive\Desktop\Anthony_Ai")
PORTAL_DIR = ROOT / "willow_rain_global" / "wholesale_portal"
TEMP_BUNDLE = ROOT / "secure_assets" / "ai_studio_bundle"
ZIP_DEST = ROOT / "willow_rain_global" / "wholesale_portal" / "obsidian_ai_studio_v1.zip"

def create_bundle():
    if TEMP_BUNDLE.exists():
        shutil.rmtree(TEMP_BUNDLE)
    TEMP_BUNDLE.mkdir(parents=True)

    # 1. Copy essential IDE files
    essential_files = [
        "obsidian_ai_studio.html",
        "titan_landing.html",
        "index.html",
        "assets/hyper_frame.css",
        "assets/hyper_frame.js"
    ]

    for f in essential_files:
        src = PORTAL_DIR / f
        dest = TEMP_BUNDLE / f
        dest.parent.mkdir(parents=True, exist_ok=True)
        if src.exists():
            shutil.copy2(src, dest)
            print(f"✓ Bundled: {f}")

    # 2. Create the ZIP
    shutil.make_archive(str(ZIP_DEST).replace(".zip", ""), 'zip', TEMP_BUNDLE)
    print(f"✓ SUCCESS: Industrial IDE Bundle created at {ZIP_DEST.name}")

if __name__ == "__main__":
    create_bundle()
