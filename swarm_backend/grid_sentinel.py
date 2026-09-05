# --- EMPIRE GRID SENTINEL: DISK & RAM DEFENSE v1.0 ---
import os
import shutil
import time
import asyncio
import psutil
from swarm_logger import swarm_log

class GridSentinel:
    """
    BUSINESS NODE: Infrastructure Defense.
    Auto-cleans disk space and monitors RAM to prevent grid crashes.
    """
    def __init__(self):
        self.render_dir = r"C:\AnthonyAi_Swarm\Renderings"
        self.hf_cache = r"C:\Users\willo\huggingface_cache"

    async def run_defense_loop(self):
        swarm_log("🔱 GRID SENTINEL: Disk & RAM Defense ACTIVE.", node="SENTINEL")

        while True:
            try:
                # 1. DISK DEFENSE (Trigger at < 5GB Free)
                usage = shutil.disk_usage("C:")
                free_gb = usage.free / (1024**3)

                if free_gb < 5.0:
                    swarm_log(f"SENTINEL: Low Disk Space ({round(free_gb, 1)}GB). Purging debris...", node="SENTINEL")
                    self.purge_debris()

                # 2. RAM DEFENSE
                ram = psutil.virtual_memory()
                if ram.percent > 90:
                    swarm_log(f"SENTINEL: CRITICAL RAM PRESSURE ({ram.percent}%). Recommending grid slowdown.", node="SENTINEL")

                await asyncio.sleep(300) # Check every 5 mins
            except Exception as e:
                swarm_log(f"[-] SENTINEL ERROR: {e}", node="SENTINEL")
                await asyncio.sleep(60)

    def purge_debris(self):
        """Clears temporary renders and locks."""
        # Clear old renders (> 1 day)
        now = time.time()
        for f in os.listdir(self.render_dir):
            path = os.path.join(self.render_dir, f)
            if os.stat(path).st_mtime < now - 86400:
                try: os.remove(path)
                except: pass

        # Clear HF locks
        lock_dir = os.path.join(self.hf_cache, "hub", ".locks")
        if os.path.exists(lock_dir):
            shutil.rmtree(lock_dir, ignore_errors=True)
            os.makedirs(lock_dir, exist_ok=True)

if __name__ == "__main__":
    sentinel = GridSentinel()
    asyncio.run(sentinel.run_defense_loop())
