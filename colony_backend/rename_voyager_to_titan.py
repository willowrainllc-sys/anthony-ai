import os
import re
from pathlib import Path

PORTAL_DIR = Path(r"C:\Users\willo\OneDrive\Desktop\Anthony_Ai\willow_rain_global\wholesale_portal")
APP_DIR = Path(r"C:\Users\willo\OneDrive\Desktop\Anthony_Ai\app\src\main\java\com\obsidian\global\ui")

# 🔱 The Pivot: Obsidian Titan -> Obsidian Titan (Unique and Trend-Setting)
REPLACEMENTS = [
    (r"OBSIDIAN_TITAN", "OBSIDIAN_TITAN"),
    (r"Obsidian Titan", "Obsidian Titan"),
    (r"titan-browser.io", "titan-browser.io"),
    (r"titan_landing.html", "titan_landing.html")
]

def rename_entities():
    # 1. Update File Contents
    files = list(PORTAL_DIR.glob("*.html")) + list(PORTAL_DIR.glob("*.js")) + list(Path(r"C:\Users\willo\OneDrive\Desktop\Anthony_Ai\colony_backend").glob("*.py"))
    files.append(APP_DIR / "Obsidian TitanBrowserScreen.kt")
    files.append(Path(r"C:\Users\willo\OneDrive\Desktop\Anthony_Ai\app\src\main\java\com\obsidian\global\MainViewModel.kt"))

    for file_path in files:
        if not file_path.exists(): continue
        content = file_path.read_text(encoding='utf-8', errors='ignore')
        new_content = content
        for pattern, replacement in REPLACEMENTS:
            new_content = re.sub(pattern, replacement, new_content)

        if content != new_content:
            file_path.write_text(new_content, encoding='utf-8')
            print(f"✓ Renamed in: {file_path.name}")

    # 2. Rename the actual file
    old_file = PORTAL_DIR / "titan_landing.html"
    new_file = PORTAL_DIR / "titan_landing.html"
    if old_file.exists():
        os.rename(old_file, new_file)
        print(f"✓ Renamed File: {old_file.name} -> {new_file.name}")

if __name__ == "__main__":
    rename_entities()
