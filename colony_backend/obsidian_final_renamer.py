import os
import re
from pathlib import Path

ROOT = Path(r"C:\Users\willo\OneDrive\Desktop\Anthony_Ai")

# 🔱 THE FINAL RENAMER: Handling both content and filenames
REPLACEMENTS = [
    (r"colony_backend", "colony_backend"),
    (r"colony_log", "colony_log"),
    (r"colony_logger", "colony_logger"),
    (r"colony_persistence", "colony_persistence"),
    (r"colony_tasks", "colony_tasks"),
    (r"colony_brain", "colony_brain"),
    (r"colony_hud", "colony_hud"),
    (r"colony_engagement", "colony_engagement"),
    (r"colonyBurst", "colonyBurst"),
    (r"igniteFullBurst", "igniteFullBurst"),
    (r"colonyFeed", "colonyFeed")
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
                    # print(f"✓ Renamed content in: {file_path.relative_to(ROOT)}")
            except Exception as e:
                pass

def rename_files():
    # Pass 1: Directories
    for root, dirs, files in os.walk(str(ROOT), topdown=False):
        if "venv" in root or ".git" in root: continue
        for d in dirs:
            if "swarm" in d or "strike" in d or "103" in d:
                new_d = d.replace("swarm", "colony").replace("strike", "burst").replace("103", "nest")
                old_path = os.path.join(root, d)
                new_path = os.path.join(root, new_d)
                try:
                    os.rename(old_path, new_path)
                    print(f"✓ Renamed Dir: {d} -> {new_d}")
                except: pass

    # Pass 2: Files
    for file_path in list(ROOT.rglob("*")):
        if "venv" in str(file_path) or ".git" in str(file_path): continue
        if file_path.is_dir(): continue

        name = file_path.name
        new_name = name.replace("swarm", "colony").replace("Swarm", "Colony").replace("strike", "burst").replace("Strike", "Burst")

        if name != new_name:
            new_path = file_path.with_name(new_name)
            try:
                os.rename(file_path, new_path)
                print(f"✓ Renamed File: {name} -> {new_name}")
            except: pass

if __name__ == "__main__":
    print("🔱 Executing Final Colony Renamer Strike... (Wait, BURST)")
    rename_content()
    rename_files()
    print("✓ Evolution Complete.")
