# --- Built by Anthony Christopher | Est 12.19.1987 ---
# --- OBSIDIAN RENAME AIRO TO LEO v1.0 ---
from pathlib import Path
from colony_logger import colony_log

def rename_airo_to_leo():
    colony_log("RENAME AIRO TO LEO: Updating all public frontend references from Airo to Leo...", node="SUPREME")
    root = Path(__file__).resolve().parent.parent

    count = 0
    for html_file in root.rglob("*.html"):
        if "venv" in str(html_file) or ".git" in str(html_file):
            continue
        try:
            content = html_file.read_text(encoding="utf-8", errors="ignore")
            if "Airo" in content or "AIRO" in content:
                content = content.replace("Airo", "Leo").replace("AIRO", "LEO")
                html_file.write_text(content, encoding="utf-8")
                count += 1
                print(f"Renamed Airo to Leo in: {html_file.name}")
        except Exception as e:
            pass

    colony_log(f"✓ RENAME SUCCESS: Updated {count} HTML pages to Obsidian Leo™ AI!", node="SUPREME")

if __name__ == "__main__":
    rename_airo_to_leo()
