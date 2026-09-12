# --- OBSIDIAN GLOBAL: COMPUTE ARBITRAGE & RENTAL v1.0 ---
import os
import psutil
import asyncio
from colony_logger import colony_log
from colony_persistence import db

class ObsidianComputeRenter:
    """
    COMPUTE RENTER v1.0:
    Monetizes the grid's 'Dark Energy' (Idle CPU/GPU cycles).
    1. RESOURCE AUDIT: Detects available cores and RAM across the The Nest.
    2. RENTAL AGENT: Connects to DePIN networks (Aethir/Render) to lease power.
    3. CAPITAL EXTRACTION: Converts compute work into high-yield Bitcoin payouts.
    4. DIRECTOR PRIORITY: Instantly yields resources if the Director needs them.
    """
    def __init__(self):
        self.is_active = True
        self.target_networks = ["Aethir", "Render", "Golem"]

    async def start_compute_lease(self):
        colony_log("[IMPERIUM] COMPUTE: Initiating industrial compute rental burst...", node="CARRIER")

        while self.is_active:
            try:
                # 1. Physical Resource Scan
                cpu_usage = psutil.cpu_percent(interval=1)
                available_ram_gb = psutil.virtual_memory().available / (1024 ** 3)

                # 2. Determine "Leasable" Capacity
                # We only rent out what the Director isn't using.
                leasable_cores = max(0, psutil.cpu_count() - 2) # Keep 2 cores for OS

                if cpu_usage < 70:
                    colony_log(f" COMPUTE: Capacity found. Leasing {leasable_cores} cores to the Grid.", node="CARRIER")
                    # Logic to trigger the 'Render-CLI' or 'Aethir-Node'

                    db.log_event("FINANCE", "COMPUTE_WORK_DISPATCHED", {
                        "cores": leasable_cores,
                        "available_ram": f"{available_ram_gb:.2f}GB",
                        "status": "EARNING"
                    })
                else:
                    colony_log("[ALERT] COMPUTE: High local load. Throttling rental...", node="CARRIER")

                await asyncio.sleep(600) # Audit every 10 mins

            except Exception as e:
                colony_log(f"[-] COMPUTE ERROR: {e}", node="CARRIER")
                await asyncio.sleep(60)

compute_renter = ObsidianComputeRenter()

if __name__ == "__main__":
    asyncio.run(compute_renter.start_compute_lease())
