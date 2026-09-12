import os
import re
from pathlib import Path

ROOT = Path(r"C:\Users\willo\OneDrive\Desktop\Anthony_Ai")

# 🔱 THE EVOLUTION: Colony -> Colony | Burst -> Burst | The Nest -> The Nest
REPLACEMENTS = [
    (r"Colony", "Colony"),
    (r"colony", "colony"),
    (r"COLONY", "COLONY"),
    (r"Burst", "Burst"),
    (r"burst", "burst"),
    (r"BURST", "BURST"),
    (r"The Nest", "The Nest"),
    (r"The Nest", "The Nest"),
    (r"Nest-node", "Nest-node"),
    (r"The Nest", "The Nest"),
    (r"The Nest", "The Nest"),
    (r"The Nest", "The Nest")
]

def rename_content():
    # Target all text-based files
    extensions = [".html", ".py", ".kt", ".json", ".xml", ".bat", ".ps1", ".txt", ".md", ".gradle", ".kts"]

    for file_path in ROOT.rglob("*"):
        if file_path.suffix in extensions and "venv" not in str(file_path) and ".git" not in str(file_path):
            try:
                content = file_path.read_text(encoding='utf-8', errors='ignore')
                new_content = content
                for pattern, replacement in REPLACEMENTS:
                    new_content = re.sub(pattern, replacement, new_content)

                if content != new_content:
                    file_path.write_text(new_content, encoding='utf-8')
                    print(f"✓ Renamed content in: {file_path.relative_to(ROOT)}")
            except Exception as e:
                print(f"[-] Error processing {file_path}: {e}")

def rename_files():
    # Rename files that have 'colony' or 'burst' in their names
    # (Note: We do this after content to avoid path resolution errors during content rename)
    for file_path in list(ROOT.rglob("*")):
        if "venv" in str(file_path) or ".git" in str(file_path): continue

        name = file_path.name
        new_name = name

        # Replace in filename
        new_name = new_name.replace("colony", "colony")
        new_name = new_name.replace("Colony", "Colony")
        new_name = new_name.replace("burst", "burst")
        new_name = new_name.replace("Burst", "Burst")

        if name != new_name:
            new_path = file_path.with_name(new_name)
            try:
                os.rename(file_path, new_path)
                print(f"✓ Renamed File: {file_path.name} -> {new_name}")
            except Exception as e:
                print(f"[-] Error renaming {file_path}: {e}")

if __name__ == "__main__":
    print("🔱 Initiating Colony Evolution Burst... (Wait, it's a BURST now)")
    rename_content()
    rename_files()
    print("✓ Evolution Complete. The Colony is here.")
