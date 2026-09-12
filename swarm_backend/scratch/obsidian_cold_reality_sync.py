# --- Built by Anthony Christopher | Est 12.19.1987 ---
# --- ENCRYPTED VIA OBSIDIAN CORE v7.5 (COLD REALITY SYNC) ---
import os
import re
from pathlib import Path

ROOT = Path(r"C:\Users\willo\OneDrive\Desktop\Anthony_Ai")

FILES_TO_CLEAN = [
    ROOT / "saturn_cloud" / "dashboard_ui" / "obsidian_supreme_universe.html",
    ROOT / "saturn_cloud" / "dashboard_ui" / "virtual_call_center.html",
    ROOT / "swarm_backend" / "obsidian_voyager_shell.py",
    ROOT / "swarm_backend" / "scratch" / "obsidian_wealth_sync.py",
    ROOT / "willow_rain_global" / "obsidian_intelligence" / "credit_optimization_kernel.py",
    ROOT / "willow_rain_global" / "wholesale_portal" / "obsidian_master_hub.html",
    ROOT / "willow_rain_global" / "wholesale_portal" / "sovereign_payout_gate.html",
    ROOT / "app" / "src" / "main" / "java" / "com" / "obsidian" / "global" / "MainViewModel.kt"
]

def execute_reality_sync():
    print("=== 🔱 AURA: SYNCING EMPIRE TO COLD REALITY ($0.00) ===\n")

    replacements = {
        r"\$22,102\.50": "$0.00",
        r"22102\.50": "0.00",
        r"\$8,044\.95": "$0.00",
        r"8044\.95": "0.00"
    }

    for f in FILES_TO_CLEAN:
        if not f.exists():
            print(f"  [!] NOT FOUND: {f.name}")
            continue

        try:
            content = f.read_text(encoding='utf-8', errors='ignore')
            new_content = content

            for old, new in replacements.items():
                new_content = re.sub(old, new, new_content)

            if new_content != content:
                f.write_text(new_content, encoding='utf-8')
                print(f"  [✓] CLEANED: {f.name}")
            else:
                print(f"  [-] NO TRACES: {f.name}")
        except Exception as e:
            print(f"  [❌] ERROR {f.name}: {e}")

    print("\n🪐 REALITY SYNC COMPLETE: The board is reset to $0.00. Time to get real money.")

if __name__ == "__main__":
    execute_reality_sync()
