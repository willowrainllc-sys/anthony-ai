# --- EMPIRE AUTONOMOUS DAEMON WORKER v2.0 (GENERAL-PURPOSE AI MEDIA STUDIO) ---
import time
import random
import asyncio
import sys
import os
from datetime import datetime
from pathlib import Path

sys.path.append(os.path.dirname(__file__))

from swarm_logger import swarm_log
from master_studio import master_factory

STUDIO_NICHES = [
    "fantasy", "anime_scifi", "horror", "mythology",
    "scifi", "mystery", "finance", "psychology", "history", "motivation"
]

async def run_autonomous_cycle():
    swarm_log("DAEMON: Initializing 24/7 Autonomous General-Purpose AI Media Studio Engine...", node="DAEMON")

    while True:
        try:
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            selected_niche = random.choice(STUDIO_NICHES)
            selected_ep_num = random.randint(1, 10)

            swarm_log(f"[{current_time}] DAEMON: Starting Series-First production cycle -> Niche: [{selected_niche.upper()}] | Episode: [{selected_ep_num}]", node="DAEMON")

            # Produce and dispatch Season 1 episode using Master Studio Factory
            res = await master_factory.produce_and_dispatch_episode(
                channel_id="ANTHONY_AI_OFFICIAL",
                niche=selected_niche,
                ep_num=selected_ep_num,
                target_min=1, # 1 min test target for background worker
                content_type="SHORT_FORM"
            )

            if res and res.get("status") == "success":
                yt_link = res.get("youtube_url", "N/A")
                swarm_log(f"✓ DAEMON CYCLE SUCCESS! YouTube Live Link: {yt_link}", node="DAEMON")
            else:
                swarm_log(f"[-] DAEMON CYCLE WARNING: {res}", node="DAEMON")

            # Human-like organic jitter delay (2 to 4 hours between cycles in background)
            sleep_duration = random.randint(7200, 14400)
            sleep_mins = sleep_duration // 60
            swarm_log(f"DAEMON: Cycle complete. Entering organic jitter sleep state for {sleep_mins} minutes...", node="DAEMON")
            await asyncio.sleep(sleep_duration)

        except Exception as e:
            swarm_log(f"[-] DAEMON ERROR: {e}", node="DAEMON")
            await asyncio.sleep(600) # 10 min recovery delay

if __name__ == "__main__":
    asyncio.run(run_autonomous_cycle())
