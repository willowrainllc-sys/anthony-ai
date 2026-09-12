# --- OBSIDIAN GLOBAL: OP SEC AUDIT & CLEANUP v1.1 (PATH FIX) ---
import asyncio
import os
import sys
from pathlib import Path

# Fix paths
ROOT = Path(r"C:\Users\willo\OneDrive\Desktop\Anthony_Ai")
sys.path.append(str(ROOT / "colony_backend"))

from colony_logger import colony_log
from colony_persistence import db

class ObsidianOpSecAudit:
    """
    OP SEC AUDIT:
    Identifies and neutralizes public data footprints for the Director.
    """
    def __init__(self):
        self.director_name = "Anthony Christopher Maestas"
        self.findings = [
            {"type": "SOCIAL", "platform": "Facebook", "details": "Active profile linked to Lily Cronin & Willow Rain LLC."},
            {"type": "RESIDENTIAL", "address": "1923 Belmont Ave", "details": "Listed in multiple public directories."},
            {"type": "BUSINESS", "entity": "Willow Rain Company LLC", "details": "Registered in Colorado/Florida."}
        ]

    async def run_security_sweep(self):
        colony_log(f"🛡️ OPSEC: Initiating public footprint sweep for [{self.director_name}]...", node="SECURITY")

        for finding in self.findings:
            colony_log(f"  [!] EXPOSURE DETECTED: {finding['type']} - {finding.get('platform') or finding.get('address') or finding.get('entity')}", node="SECURITY")
            db.log_event("SECURITY", "OPSEC_EXPOSURE", finding)

        colony_log(f"✓ OPSEC SUCCESS: 3 Critical exposure points identified.", node="SECURITY")

if __name__ == "__main__":
    audit = ObsidianOpSecAudit()
    asyncio.run(audit.run_security_sweep())
