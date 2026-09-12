import os
import re
from pathlib import Path

ROOT = Path(r"C:\Users\willo\OneDrive\Desktop\Anthony_Ai")
DIRS = [ROOT / "colony_backend", ROOT / "willow_rain_global", ROOT / "saturn_cloud" / "dashboard_ui"]

REPLACEMENTS = {
    "PROPOSAL_SENT": "PROPOSAL_SENT",
    "Proposal Sent": "Proposal Sent",
    "proposal sent": "proposal sent",
    "AWAITING_HANDSHAKE": "AWAITING_HANDSHAKE",
    "Awaiting Handshake": "Awaiting Handshake",
    "awaiting handshake": "awaiting handshake",
    "NEGOTIATING": "NEGOTIATING",
    "Negotiating": "Negotiating",
    "negotiating": "negotiating"
}

def apply_proposal_lingo():
    print("=== 🔱 PROPOSAL SYNC: ALIGNING EMPIRE LINGO WITH REALITY ===\n")
    update_count = 0

    for d in DIRS:
        if not d.exists(): continue
        for f in d.rglob("*"):
            if f.is_file() and f.suffix in [".py", ".html", ".js", ".json", ".kt"]:
                try:
                    content = f.read_text(encoding='utf-8', errors='ignore')
                    new_content = content

                    for old, new in REPLACEMENTS.items():
                        new_content = new_content.replace(old, new)

                    if new_content != content:
                        f.write_text(new_content, encoding='utf-8')
                        print(f"  [✓] PROPOSAL LOGIC: {f.name}")
                        update_count += 1
                except: pass

    print(f"\n🪐 LINGO UPDATE COMPLETE: {update_count} files transitioned to PROPOSAL status.")

if __name__ == "__main__":
    apply_proposal_lingo()
