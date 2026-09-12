import os
import re
from pathlib import Path

ROOT = Path(r"C:\Users\willo\OneDrive\Desktop\Anthony_Ai\willow_rain_global\wholesale_portal")

REPLACEMENTS = {
    "HANDSHAKE": "SECURE CONNECTION",
    "Handshake": "Secure Sync",
    "handshake": "sync",
    "NEGOTIATING": "PROCESSING",
    "Negotiating": "Reviewing",
    "INGRESS": "NETWORK",
    "Ingress": "Access",
    "ingress": "feed",
    "PROPOSAL_SENT": "SECURE_AUTHORIZED",
    "SETTLING": "CLEARING",
    "Settling": "Verifying",
    "SETTLED": "VERIFIED",
    "BACKEND": "SOVEREIGN CORE",
    "Backend": "Secure Core",
    "TITAN INGRESS": "TITAN NETWORK",
    "BLACK HOLE": "OBSIDIAN MEDIA",
    "Black Hole": "Obsidian Media",
    "black hole": "obsidian media"
}

def apply_aesthetic_fix():
    print("=== 🔱 AURA: APPLYING PROFESSIONAL AESTHETIC FIX ===\n")

    for f in ROOT.glob("*.html"):
        try:
            content = f.read_text(encoding='utf-8', errors='ignore')
            new_content = content

            for old, new in REPLACEMENTS.items():
                new_content = new_content.replace(old, new)

            if new_content != content:
                f.write_text(new_content, encoding='utf-8')
                print(f"  [✓] AURA HARDENED: {f.name}")
        except: pass

if __name__ == "__main__":
    apply_aesthetic_fix()
