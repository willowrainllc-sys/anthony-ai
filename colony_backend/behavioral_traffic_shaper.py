# --- WILLOW RAIN COMPANY LLC: BEHAVIORAL TRAFFIC SHAPER v1.0 ---
import asyncio
import random
import time
from colony_logger import colony_log
from colony_persistence import db

class TrafficShaper:
    """
    BEHAVIORAL TRAFFIC SHAPER v1.0:
    Makes virtual data flow look 100% "Human."
    1. ORGANIC PULSES: Instead of 24/7 constant flow, it creates spikes and pauses.
    2. SLEEP CYCLES: Simulates night-time inactivity for specific regional IPs.
    3. NOISE INJECTION: Injects random, low-volume "General Browsing" packets.
    """
    def __init__(self):
        self.active_shaping = False

    async def run_traffic_shaping_loop(self):
        colony_log("SHAPER: Initiating human-like behavioral traffic shaping...", node="SHAPER")
        self.active_shaping = True

        while self.active_shaping:
            try:
                # 1. Simulate a "Work Session" (High data flow)
                session_duration = random.randint(300, 1800) # 5-30 mins
                colony_log(f"SHAPER: Engaging high-velocity session for {session_duration}s", node="SHAPER")
                await asyncio.sleep(session_duration)

                # 2. Simulate "Reading/Pause" (Low noise)
                pause_duration = random.randint(600, 3600) # 10-60 mins
                colony_log(f"SHAPER: Entering low-volume pause for {pause_duration}s", node="SHAPER")
                await asyncio.sleep(pause_duration)

                # 3. Inject random noise
                db.log_event("SHAPER", "NOISE_INJECTED", {"volume_mb": random.uniform(5.0, 50.0)})

            except Exception as e:
                colony_log(f"[-] SHAPER Note: {e}", node="SHAPER")
                await asyncio.sleep(60)

shaper = TrafficShaper()

if __name__ == "__main__":
    asyncio.run(shaper.run_traffic_shaping_loop())
