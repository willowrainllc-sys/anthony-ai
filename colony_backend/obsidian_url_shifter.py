# --- Built by Anthony Christopher | Est 12.19.1987 ---
# --- OBSIDIAN URL SHIFTER & TRAFFIC REDIRECTOR v1.0 ---
import os
from pathlib import Path
from colony_logger import colony_log

def shift_empire_urls_to_obsidian_city():
    colony_log("URL SHIFTER: Shifting all empire traffic, scrapers, and monetization endpoints to https://obsidian.city...", node="SUPREME")

    root_dir = Path(__file__).resolve().parent.parent
    old_urls = ["https://obsidian.city", "https://obsidian.city"]
    new_url = "https://obsidian.city"

    updated_count = 0
    for path in root_dir.rglob("*.py"):
        if "venv" in str(path) or ".git" in str(path):
            continue
        try:
            content = path.read_text(encoding="utf-8")
            changed = False
            for old in old_urls:
                if old in content:
                    content = content.replace(old, new_url)
                    changed = True
            if changed:
                path.write_text(content, encoding="utf-8")
                updated_count += 1
                print(f"Shifted URL in: {path.relative_to(root_dir)}")
        except Exception as e:
            pass

    colony_log(f"✓ URL SHIFTER SUCCESS: Shifted empire traffic and scrapers across {updated_count} files to https://obsidian.city!", node="SUPREME")

if __name__ == "__main__":
    shift_empire_urls_to_obsidian_city()
