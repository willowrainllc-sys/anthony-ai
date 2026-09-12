import os
from pathlib import Path

# Paths to process
DIRS = [
    Path(r"C:\Users\willo\OneDrive\Desktop\Obsidian_Ai\colony_backend"),
    Path(r"C:\Users\willo\OneDrive\Desktop\Obsidian_Ai\willow_rain_global\ingress_api"),
    Path(r"C:\Users\willo\OneDrive\Desktop\Obsidian_Ai\willow_rain_global\cellular_stack"),
    Path(r"C:\Users\willo\OneDrive\Desktop\Obsidian_Ai\willow_rain_global\imperium_carrier_core")
]

TARGETS = ["sovereign_", "supreme_"]
REPLACEMENT = "obsidian_"

def rebrand_files():
    print("=== 🪐 OBSIDIAN REBRANDING: INITIALIZING FILENAME STRIKE ===\n")
    rename_count = 0

    for d in DIRS:
        if not d.exists(): continue
        print(f"[*] Processing Directory: {d}")
        for f in d.iterdir():
            if f.is_file():
                new_name = f.name
                for target in TARGETS:
                    if new_name.lower().startswith(target):
                        new_name = new_name.replace(target, REPLACEMENT)

                if new_name != f.name:
                    new_path = f.parent / new_name
                    try:
                        os.rename(f, new_path)
                        print(f"  [✓] RENAME: {f.name} -> {new_name}")
                        rename_count += 1
                    except Exception as e:
                        print(f"  [-] FAIL: {f.name} -> {e}")

    print(f"\n🪐 REBRAND COMPLETE: {rename_count} files renamed to OBSIDIAN.")

if __name__ == "__main__":
    rebrand_files()
