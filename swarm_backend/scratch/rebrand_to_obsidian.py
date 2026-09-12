import os
from pathlib import Path

# Paths to process
DIRS = [
    Path(r"C:\Users\willo\OneDrive\Desktop\Obsidian_Ai\swarm_backend"),
    Path(r"C:\Users\willo\OneDrive\Desktop\Obsidian_Ai\willow_rain_global\ingress_api"),
    Path(r"C:\Users\willo\OneDrive\Desktop\Obsidian_Ai\willow_rain_global\cellular_stack"),
    Path(r"C:\Users\willo\OneDrive\Desktop\Obsidian_Ai\willow_rain_global\imperium_carrier_core"),
    Path(r"C:\Users\willo\OneDrive\Desktop\Obsidian_Ai\obsidian_cloud")
]

REPLACEMENTS = {
    "obsidian": "obsidian",
    "Obsidian": "Obsidian",
    "OBSIDIAN": "OBSIDIAN",
    "obsidian": "obsidian", # Merging the brain into the brand
    "Obsidian": "Obsidian"
}

def rebrand_to_obsidian():
    print("=== 💎 OBSIDIAN REBRANDING: INITIALIZING THE DARK STRIKE ===\n")
    rename_count = 0
    content_count = 0

    # 1. Filename Strike
    for d in DIRS:
        if not d.exists(): continue
        for f in d.iterdir():
            old_name = f.name
            new_name = old_name
            for old, new in REPLACEMENTS.items():
                if old in new_name:
                    new_name = new_name.replace(old, new)

            if new_name != old_name:
                new_path = f.parent / new_name
                try:
                    os.rename(f, new_path)
                    print(f"  [✓] RENAME: {old_name} -> {new_name}")
                    rename_count += 1
                    f = new_path
                except Exception as e:
                    print(f"  [-] FAIL RENAME {old_name}: {e}")

    # 2. Content Strike (DNA Recode)
    all_python_files = []
    for d in DIRS:
        if not d.exists(): continue
        all_python_files.extend(list(d.rglob("*.py")))
        all_python_files.extend(list(d.rglob("*.html")))
        all_python_files.extend(list(d.rglob("*.bat")))

    for f in all_python_files:
        try:
            content = f.read_text(encoding='utf-8', errors='ignore')
            new_content = content
            for old, new in REPLACEMENTS.items():
                new_content = new_content.replace(old, new)

            if new_content != content:
                f.write_text(new_content, encoding='utf-8')
                content_count += 1
        except: pass

    print(f"\n💎 OBSIDIAN COMPLETE: {rename_count} files renamed, {content_count} files recoded.")

if __name__ == "__main__":
    rebrand_to_obsidian()
