# --- EMPIRE MASTER DOCUMENTARY CREATOR & MULTI-CHANNEL DISPATCHER v7.0 (SYNCHRONIZED STORYBOARDS) ---
import os
import sys
import asyncio
import json
import uuid
import random
import time
from pathlib import Path
import httpx

sys.path.append(os.path.dirname(__file__))

from swarm_logger import swarm_log
from swarm_persistence import db
from pipeline import build_storyline_video, generate_neural_narration
from faceless_niches_engine import generate_faceless_package, FACELESS_20_NICHES
from node_youtube import publish_to_youtube_api
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv(dotenv_path=Path(__file__).resolve().parent.parent / ".env")
supabase: Client = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))

async def create_and_dispatch_documentary(niche_key: str = None, duration_tier: str = "short") -> dict:
    """
    MASTER FACELESS DOCUMENTARY ENGINE v7.0:
    Builds 100% synchronized storyline videos where title, narration, tags,
    and B-roll visuals match 100% with zero disconnects.
    """
    faceless_pkg = generate_faceless_package(niche_key=niche_key)

    clean_title = faceless_pkg["title"]
    narration_text = faceless_pkg["narration"]
    visual_prompts = faceless_pkg["prompts"]
    description_text = faceless_pkg["description"]

    filename = f"faceless_{uuid.uuid4().hex[:6]}.mp4"
    swarm_log(f"MASTER ENGINE: Generating [{faceless_pkg['channel_name']}] doc [{clean_title}]...", node="MASTER")

    # 1. BUILD STUDIO-QUALITY MP4 WITH PIPELINE
    res_dict = await build_storyline_video(
        title=clean_title,
        script_narration=narration_text,
        scene_prompts=visual_prompts,
        output_filename=filename,
        duration_tier=duration_tier,
        category="mystery"
    )

    if not res_dict or not os.path.exists(res_dict.get("output_path", "")):
        swarm_log("[-] MASTER ENGINE FAIL: Video assembly failed.", node="MASTER")
        return {"status": "error", "reason": "Render failed"}

    output_path = res_dict["output_path"]

    # 2. UPLOAD TO SUPABASE STORAGE WITH VIDEO/MP4 MIME TYPE
    swarm_log(f"MASTER ENGINE: Uploading [{filename}] to Supabase Storage...", node="MASTER")
    storage_path = f"renders/master_{filename}"
    with open(output_path, "rb") as f:
        supabase.storage.from_("ai-videos").upload(
            storage_path,
            f,
            file_options={"content-type": "video/mp4", "upsert": "true"}
        )

    public_url = supabase.storage.from_("ai-videos").get_public_url(storage_path)

    # 3. REGISTER IN SUPABASE VIDEOS FEED (APP FEED)
    swarm_log("MASTER ENGINE: Registering in Supabase Videos feed...", node="MASTER")
    supabase.table("videos").insert({
        "title": clean_title,
        "description": description_text,
        "video_url": public_url,
        "creator": "Anthony AI",
        "posted": "Just Now"
    }).execute()

    # 4. DISPATCH LIVE STRICTLY TO YOUTUBE SHORTS (ONLY ACTIVE CHANNEL FOR TESTING)
    swarm_log("MASTER ENGINE: Dispatching strictly to YouTube Shorts for Quality Inspection...", node="MASTER")
    yt_url = await publish_to_youtube_api(
        task={"id": 101},
        video_url=public_url,
        title=clean_title,
        description=description_text
    )

    # 5. LOG SUCCESS EVENT TO VAULT
    db.log_event("MASTER", "STRIKE_SUCCESS", {
        "title": clean_title,
        "video_url": public_url,
        "youtube_url": yt_url,
        "reference_handle": faceless_pkg["reference_handle"]
    })

    swarm_log(f"🔱 MASTER STRIKE COMPLETE! YouTube Live: {yt_url}", node="MASTER")

    return {
        "status": "success",
        "title": clean_title,
        "public_url": public_url,
        "youtube_url": yt_url,
        "reference_handle": faceless_pkg["reference_handle"]
    }

if __name__ == "__main__":
    asyncio.run(create_and_dispatch_documentary(niche_key="thefourthencounter", duration_tier="short"))
