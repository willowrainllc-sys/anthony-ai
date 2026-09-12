# --- Built by Anthony Christopher | Est 12.19.1987 ---
# --- OBSIDIAN ADSENSE REMOVER v1.0 ---
from pathlib import Path
from colony_logger import colony_log

def remove_adsense_everywhere():
    colony_log("ADSENSE REMOVER: Stripping Google AdSense monetization banners from all HTML pages...", node="SUPREME")
    root = Path(__file__).resolve().parent.parent

    count = 0
    for html_file in root.rglob("*.html"):
        if "venv" in str(html_file) or ".git" in str(html_file):
            continue
        try:
            content = html_file.read_text(encoding="utf-8", errors="ignore")
            changed = False
            if "adsbygoogle.js" in content or "adsbygoogle" in content:
                # Remove adsense script tag
                lines = content.splitlines()
                new_lines = []
                skip = False
                for line in lines:
                    if "adsbygoogle" in line:
                        changed = True
                        continue
                    new_lines.append(line)
                content = "\n".join(new_lines)
                html_file.write_text(content, encoding="utf-8")
                count += 1
                print(f"Removed AdSense from: {html_file.name}")
        except Exception as e:
            pass

    colony_log(f"✓ ADSENSE REMOVER SUCCESS: Stripped ads across {count} HTML pages!", node="SUPREME")

if __name__ == "__main__":
    remove_adsense_everywhere()
