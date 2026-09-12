import os
import re
from pathlib import Path

ROOT = Path(r"C:\Users\willo\OneDrive\Desktop\Anthony_Ai")
DIRS = [ROOT / "colony_backend", ROOT / "willow_rain_global", ROOT / "saturn_cloud" / "dashboard_ui"]

REPLACEMENTS = {
    "Negotiating (Awaiting Handshake)": "Negotiating (Awaiting Handshake)",
    "NEGOTIATING": "NEGOTIATING",
    "negotiating": "negotiating",
    "Negotiating": "Negotiating",
    "Awaiting Handshake": "Awaiting Handshake",
    "awaiting handshake": "awaiting handshake"
}

def apply_boss_lingo():
    print("=== 🔱 BOSS LINGO STRIKE: UPDATING EMPIRE VOCABULARY ===\n")
    update_count = 0

    for d in DIRS:
        if not d.exists(): continue
        for f in d.rglob("*"):
            if f.is_file() and f.suffix in [".py", ".html", ".js", ".json", ".kt"]:
                try:
                    content = f.read_text(encoding='utf-8', errors='ignore')
                    new_content = content

                    # We don't want to break internal status strings like 'NEGOTIATING' in DB
                    # unless we update the whole loop. We'll update the DISPLAY strings.
                    # Actually, the Director says 'negotiating' means 'already paid', so we update the logic too.

                    for old, new in REPLACEMENTS.items():
                        new_content = new_content.replace(old, new)

                    if new_content != content:
                        f.write_text(new_content, encoding='utf-8')
                        print(f"  [✓] BOSS LINGO: {f.name}")
                        update_count += 1
                except: pass

    print(f"\n🪐 LINGO UPDATE COMPLETE: {update_count} files aligned with Director vocabulary.")

if __name__ == "__main__":
    apply_boss_lingo()
