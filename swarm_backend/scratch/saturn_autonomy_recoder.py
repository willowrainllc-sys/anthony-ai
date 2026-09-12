import os
import re
from pathlib import Path

ROOT = Path(r"C:\Users\willo\OneDrive\Desktop\Obsidian_Ai")
DIRS = [ROOT / "swarm_backend", ROOT / "willow_rain_global", ROOT / "app"]

REPLACEMENTS = {
    # 1. Major Services
    "obsidian_ingress": "obsidian_ingress",
    "Obsidian Ingress": "Obsidian Ingress",
    "OBSIDIAN_INGRESS": "OBSIDIAN_INGRESS",

    "obsidian_bridge": "obsidian_bridge",
    "Obsidian Bridge": "Obsidian Bridge",
    "OBSIDIAN_BRIDGE": "OBSIDIAN_BRIDGE",

    "obsidian_ai": "obsidian_ai",
    "Obsidian AI": "Obsidian AI",

    "obsidian_global": "obsidian_global",
    "Obsidian Global": "Obsidian Global",

    "obsidian_grid": "obsidian_grid",
    "Obsidian Grid": "Obsidian Grid",

    # 2. Rewards
    "obsidian_rewards": "obsidian_rewards",
    "obsidian_rewards": "obsidian_rewards",
    "obsidian_rewards": "obsidian_rewards",

    # 3. Comms
    "obsidian_comm": "obsidian_comm",
    "obsidian_comm": "obsidian_comm",

    # 4. Identity
    "obsidian": "obsidian",
    "obsidian.global.holdings": "obsidian.global.holdings"
}

def recode_everything():
    print("=== 🪐 OBSIDIAN AUTONOMY RECODER: INITIATING FULL-STACK REBIRTH ===\n")
    rename_count = 0
    content_count = 0

    # Pass 1: Content Update
    for d in DIRS:
        if not d.exists(): continue
        for f in d.rglob("*"):
            if f.is_file() and f.suffix in [".py", ".kt", ".xml", ".html", ".js", ".json", ".bat", ".sh", ".gradle", ".kts", ".properties"]:
                try:
                    content = f.read_text(encoding='utf-8', errors='ignore')
                    new_content = content
                    for old, new in REPLACEMENTS.items():
                        new_content = new_content.replace(old, new)

                    if new_content != content:
                        f.write_text(new_content, encoding='utf-8')
                        content_count += 1
                        print(f"  [RECODED] {f.name}")
                except Exception as e:
                    print(f"  [-] ERROR content {f.name}: {e}")

    # Pass 2: Filename Update
    for d in DIRS:
        if not d.exists(): continue
        # We walk top-down to handle folders correctly
        for root, dirs, files in os.walk(d, topdown=False):
            for name in files + dirs:
                new_name = name
                for old, new in REPLACEMENTS.items():
                    # Handle lowercase filenames primarily
                    if old.lower() in new_name.lower():
                        new_name = new_name.replace(old.lower(), new.lower())

                if new_name != name:
                    old_path = Path(root) / name
                    new_path = Path(root) / new_name
                    try:
                        os.rename(old_path, new_path)
                        rename_count += 1
                        print(f"  [RENAMED] {name} -> {new_name}")
                    except Exception as e:
                        print(f"  [-] ERROR rename {name}: {e}")

    print(f"\n🪐 REBIRTH COMPLETE: {content_count} files recoded, {rename_count} files/folders renamed.")
    print("✓ Your system is now independent. No middlemen traces remain.")

if __name__ == "__main__":
    recode_everything()
