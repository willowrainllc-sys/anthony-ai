import os
from pathlib import Path

# Paths to process
DIRS = [
    Path(r"C:\Users\willo\OneDrive\Desktop\Obsidian_Ai\colony_backend"),
    Path(r"C:\Users\willo\OneDrive\Desktop\Obsidian_Ai\willow_rain_global\ingress_api"),
    Path(r"C:\Users\willo\OneDrive\Desktop\Obsidian_Ai\willow_rain_global\cellular_stack"),
    Path(r"C:\Users\willo\OneDrive\Desktop\Obsidian_Ai\willow_rain_global\imperium_carrier_core")
]

REPLACEMENTS = {
    "sovereign": "obsidian",
    "Sovereign": "Obsidian",
    "SOVEREIGN": "OBSIDIAN",
    "imperium": "obsidian",
    "Imperium": "Obsidian",
    "IMPERIUM": "OBSIDIAN"
}

def final_purge():
    print("=== 🪐 FINAL OBSIDIAN PURGE: INCINERATING LEGACY TERMS ===\n")
    rename_count = 0
    content_count = 0

    for d in DIRS:
        if not d.exists(): continue
        for f in d.iterdir():
            # 1. Rename the file if it contains legacy terms
            old_name = f.name
            new_name = old_name
            for old, new in REPLACEMENTS.items():
                if old.lower() in new_name.lower():
                    # Handle prefix replacements specifically for filenames
                    if new_name.lower().startswith(old.lower() + "_"):
                        new_name = new + new_name[len(old):]
                    else:
                        new_name = new_name.replace(old, new).replace(old.lower(), new.lower()).replace(old.upper(), new.upper())

            if new_name != old_name:
                new_path = f.parent / new_name
                try:
                    os.rename(f, new_path)
                    print(f"  [✓] RENAME: {old_name} -> {new_name}")
                    rename_count += 1
                    f = new_path # Update reference for content check
                except: pass

            # 2. Update File Content
            if f.is_file() and f.suffix == ".py":
                try:
                    content = f.read_text(encoding='utf-8', errors='ignore')
                    new_content = content
                    for old, new in REPLACEMENTS.items():
                        new_content = new_content.replace(old, new)

                    if new_content != content:
                        f.write_text(new_content, encoding='utf-8')
                        content_count += 1
                except: pass

    print(f"\n🪐 PURGE COMPLETE: {rename_count} files renamed, {content_count} files recoded.")

if __name__ == "__main__":
    final_purge()
