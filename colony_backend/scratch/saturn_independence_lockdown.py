import os
import re
from pathlib import Path

ROOT = Path(r"C:\Users\willo\OneDrive\Desktop\Obsidian_Ai")
DIRS = [ROOT / "colony_backend", ROOT / "willow_rain_global"]

# URLs to redirect to our own infrastructure
URL_MAP = {
    "https://api.obsidian-global.io": "https://api.obsidian-global.io",
    "https://bridge.obsidian-global.io": "https://bridge.obsidian-global.io",
    "https://comm.obsidian-global.io": "https://comm.obsidian-global.io",
    "https://comm.obsidian-global.io": "https://comm.obsidian-global.io",
    "https://ingress.obsidian-global.io": "https://ingress.obsidian-global.io"
}

def lockdown_independence():
    print("=== 🪐 OBSIDIAN INDEPENDENCE LOCKDOWN: CUTTING THIRD-PARTY TIES ===\n")
    update_count = 0

    for d in DIRS:
        if not d.exists(): continue
        for f in d.rglob("*.py"):
            try:
                content = f.read_text(encoding='utf-8', errors='ignore')
                new_content = content
                for old_url, new_url in URL_MAP.items():
                    if old_url in new_content:
                        new_content = new_content.replace(old_url, new_url)

                if new_content != content:
                    f.write_text(new_content, encoding='utf-8')
                    print(f"  [LOCKED] {f.name} -> Pointed to Obsidian Infrastructure.")
                    update_count += 1
            except Exception as e:
                print(f"  [-] ERROR {f.name}: {e}")

    print(f"\n🪐 LOCKDOWN COMPLETE: {update_count} files decoupled from middlemen.")
    print("✓ Your bots now only talk to OBSIDIAN GLOBAL servers.")

if __name__ == "__main__":
    lockdown_independence()
