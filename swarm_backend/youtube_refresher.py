import asyncio
import os
import httpx
import json
from pathlib import Path
from dotenv import load_dotenv
from swarm_logger import swarm_log
from swarm_tasks import TaskQueue
from cognitive_sentinel import sentinel

# Load environment
dotenv_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=dotenv_path)

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
CHANNEL_URL = "https://youtube.com/@willowrainco"

async def run_youtube_legacy_jitter():
    swarm_log("JITTER: Initiating YouTube Boost for Willow Rain Co / XIX...", node="YOUTUBE")

    # 1. We signal the Jitter to the Conglomerate
    # This instructs the other nodes (Threads/FB/IG) to 'Mention' or 'Link' to XIX content
    # creating cross-platform resonance.

    TaskQueue.push("ENGAGEMENT", {
        "channel_url": CHANNEL_URL,
        "name": "Willow Rain Co / XIX",
        "type": "LEGACY_YOUTUBE_BOOST"
    })

    # 2. Gaussian Jitter Pacing
    delay = sentinel.get_stealth_jitter(30)
    swarm_log(f"JITTER: Queued XIX support pulse. Pacing: {round(delay, 1)}s.", node="YOUTUBE")
    await asyncio.sleep(delay)

    swarm_log("SUCCESS: YouTube Legacy Jitter issued to the Swarm.", node="YOUTUBE")

if __name__ == "__main__":
    asyncio.run(run_youtube_legacy_jitter())
