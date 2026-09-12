# --- Built by Anthony Christopher | Est 12.19.1987 ---
# --- OBSIDIAN PURGE OBSIDIAN CITY & LEO v1.0 ---
from pathlib import Path
from colony_logger import colony_log

def purge_legacy_references():
    colony_log("PURGE: Stripping all remaining Obsidian City and Leo references across the empire...", node="SUPREME")
    root = Path(__file__).resolve().parent.parent

    file_count = 0
    for path in root.rglob("*.*"):
        if "venv" in str(path) or ".git" in str(path) or ".gradle" in str(path) or ".idea" in str(path):
            continue
        if path.suffix.lower() not in [".html", ".js", ".py", ".md", ".json", ".kt", ".kts"]:
            continue
        try:
            content = path.read_text(encoding="utf-8", errors="ignore")
            changed = False

            # Replace Obsidian City variants
            if "Obsidian City" in content or "obsidian city" in content or "OBSIDIAN CITY" in content:
                content = content.replace("Obsidian City", "Obsidian City").replace("obsidian city", "obsidian city").replace("OBSIDIAN CITY", "OBSIDIAN CITY")
                changed = True

            # Replace Leo variants (if any linger outside backend)
            if "Leo" in content or "LEO" in content or "leo" in content:
                content = content.replace("Leo", "Leo").replace("LEO", "LEO").replace("leo", "leo")
                changed = True

            if changed:
                path.write_text(content, encoding="utf-8")
                file_count += 1
                print(f"Purged legacy refs in: {path.relative_to(root)}")
        except Exception as e:
            pass

    colony_log(f"✓ PURGE SUCCESS: Cleaned legacy references across {file_count} files!", node="SUPREME")

if __name__ == "__main__":
    purge_legacy_references()
