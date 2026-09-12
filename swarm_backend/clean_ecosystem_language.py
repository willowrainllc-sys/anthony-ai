import os
import re
from pathlib import Path

PORTAL_DIR = Path(r"C:\Users\willo\OneDrive\Desktop\Anthony_Ai\willow_rain_global\wholesale_portal")

# Patterns to replace "Sovereign" with more industrial/business timeline language
REPLACEMENTS = [
    (r"Sovereign", "Global"),
    (r"SOVEREIGN", "INDUSTRIAL"),
    (r"sovereign", "enterprise")
]

def clean_language():
    files = list(PORTAL_DIR.glob("*.html")) + list(PORTAL_DIR.glob("*.js")) + list(PORTAL_DIR.glob("*.json"))

    for file_path in files:
        if file_path.name == "aiphony_manifest.json": continue # Internal only

        content = file_path.read_text(encoding='utf-8', errors='ignore')
        new_content = content

        for pattern, replacement in REPLACEMENTS:
            new_content = re.sub(pattern, replacement, new_content, flags=re.IGNORECASE)

        if content != new_content:
            file_path.write_text(new_content, encoding='utf-8')
            print(f"✓ Cleaned: {file_path.name}")

if __name__ == "__main__":
    clean_language()
