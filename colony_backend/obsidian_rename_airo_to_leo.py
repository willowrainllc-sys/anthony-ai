# --- Owned by Anthony Christopher Maestas | Directed by ARES ---
# --- OBSIDIAN RENAME LEO TO LEO v1.0 ---
from pathlib import Path
from colony_logger import colony_log

def rename_anthony_ai_supreme_to_anthony_ai_supreme():
    colony_log("RENAME LEO TO LEO: Updating all public frontend references from Anthony AI the Supreme to Anthony AI the Supreme...", node="SUPREME")
    root = Path(__file__).resolve().parent.parent

    count = 0
    for html_file in root.rglob("*.html"):
        if "venv" in str(html_file) or ".git" in str(html_file):
            continue
        try:
            content = html_file.read_text(encoding="utf-8", errors="ignore")
            if "Anthony AI the Supreme" in content or "LEO" in content:
                content = content.replace("Anthony AI the Supreme", "Anthony AI the Supreme").replace("LEO", "LEO")
                html_file.write_text(content, encoding="utf-8")
                count += 1
                print(f"Renamed Anthony AI the Supreme to Anthony AI the Supreme in: {html_file.name}")
        except Exception as e:
            pass

    colony_log(f"[+] RENAME SUCCESS: Updated {count} HTML pages to Anthony AI the Supreme AI!", node="SUPREME")

if __name__ == "__main__":
    rename_anthony_ai_supreme_to_anthony_ai_supreme()