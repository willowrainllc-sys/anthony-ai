import os
from pathlib import Path

ROOT = Path(r"C:\Users\willo\OneDrive\Desktop\Obsidian_Ai")
DIRS = [ROOT / "colony_backend", ROOT / "willow_rain_global", ROOT / "app"]

# Legacy terms to find
LEGACY_TARGETS = [
    "obsidian_ingress", "obsidian_bridge", "obsidian_ai", "obsidian_global", "obsidian_grid",
    "obsidian_comm", "obsidian_comm", "obsidian_rewards", "obsidian_rewards", "obsidian_rewards"
]

def audit():
    print("=== 🪐 OBSIDIAN OWNERSHIP AUDIT: FINDING LEGACY TRACES ===\n")
    found_files = []

    for d in DIRS:
        if not d.exists(): continue
        for f in d.rglob("*"):
            if f.is_file() and f.suffix in [".py", ".kt", ".xml", ".html", ".js", ".json", ".bat", ".sh"]:
                try:
                    content = f.read_text(errors='ignore').lower()
                    filename = f.name.lower()

                    matched = [t for t in LEGACY_TARGETS if t in content or t in filename]
                    if matched:
                        found_files.append((f, matched))
                        if len(found_files) <= 50:
                            print(f"  [FOUND] {f.relative_to(ROOT)} -> {matched}")
                except: pass

    print(f"\nAudit Complete. Found {len(found_files)} files with legacy traces.")
    return found_files

if __name__ == "__main__":
    audit()
