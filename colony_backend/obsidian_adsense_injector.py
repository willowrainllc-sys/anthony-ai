# --- Built by Anthony Christopher | Est 12.19.1987 ---
# --- OBSIDIAN ADSENSE GLOBAL INJECTOR v1.0 ---
from pathlib import Path
from colony_logger import colony_log

def inject_adsense_everywhere():
    colony_log("ADSENSE INJECTOR: Injecting Google AdSense monetization across all HTML pages...", node="SUPREME")
    root = Path(__file__).resolve().parent.parent
    adsense_tag = '<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-OBSIDIAN_GLOBAL_ADSENSE" crossorigin="anonymous"></script>'

    count = 0
    for html_file in root.rglob("*.html"):
        if "venv" in str(html_file) or ".git" in str(html_file):
            continue
        try:
            content = html_file.read_text(encoding="utf-8", errors="ignore")
            if "adsbygoogle.js" not in content:
                if "<head>" in content:
                    content = content.replace("<head>", f"<head>\n    {adsense_tag}")
                    html_file.write_text(content, encoding="utf-8")
                    count += 1
                    print(f"Injected AdSense into: {html_file.name}")
        except Exception as e:
            pass

    colony_log(f"✓ ADSENSE INJECTOR SUCCESS: Injected ad monetization across {count} HTML pages!", node="SUPREME")

if __name__ == "__main__":
    inject_adsense_everywhere()
