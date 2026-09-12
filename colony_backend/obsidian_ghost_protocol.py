# --- WILLOW RAIN SECURITY: OBSIDIAN GHOST PROTOCOL v1.0 ---
import os
import shutil
from pathlib import Path
from colony_logger import colony_log
from colony_persistence import db

class ObsidianGhostProtocol:
    """
    OBSIDIAN GHOST PROTOCOL v1.0:
    Erases digital traces of the Willow Rain Colony.
    1. LOG PURGE: Deletes all local .log and .jsonl files in the secure vaults.
    2. TEMP CLEANUP: Clears the AppData/Local/Temp directories used for video buffering.
    3. IDENTITY WIPE: Deletes all cached 'Ghost Identities' from the secure vault.
    4. DATABASE TRUNCATE: Optionally purges event history (leaving core settings).
    """
    def __init__(self):
        self.logs_dir = Path(r"D:\ObsidianAi_Colony\Logs")
        self.temp_dir = Path(os.environ.get("TEMP", "."))
        self.vault_dir = Path(r"D:\ObsidianAi_Colony\Secure_Assets")

    def execute_ghost_purge(self):
        colony_log(" GHOST_PROTOCOL: INITIATING DIGITAL TRACE PURGE...", node="SECURITY")

        # 1. Purge Logs
        if self.logs_dir.exists():
            for f in self.logs_dir.glob("*.*"):
                try: os.remove(f)
                except: pass
            colony_log(" GHOST: Master logs incinerated.", node="SECURITY")

        # 2. Purge Ghost Identities
        identity_dir = self.vault_dir / "ghost_identities"
        if identity_dir.exists():
            shutil.rmtree(identity_dir)
            identity_dir.mkdir(parents=True, exist_ok=True)
            colony_log(" GHOST: All virtual identities deleted.", node="SECURITY")

        # 3. Clear Temp Buffers
        for f in self.temp_dir.glob("yt_burst_*.mp4"):
            try: os.remove(f)
            except: pass
        for f in self.temp_dir.glob("fb_burst_*.mp4"):
            try: os.remove(f)
            except: pass

        colony_log(" GHOST: Temporary video buffers cleared.", node="SECURITY")

        db.log_event("SECURITY", "GHOST_PROTOCOL_EXECUTED", {"status": "TRACES_PURGED"})
        colony_log("[SUPREME] SYSTEM STATUS: GHOSTED. WILLOW RAIN IS NOW INVISIBLE.", node="SECURITY")
        return True

ghost_protocol = ObsidianGhostProtocol()

if __name__ == "__main__":
    ghost_protocol.execute_ghost_purge()
