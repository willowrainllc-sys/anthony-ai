# --- EMPIRE MASTER DOCUMENTARY CREATOR & MULTI-CHANNEL DISPATCHER v7.0 (SYNCHRONIZED STORYBOARDS) ---
import os
import sys
import asyncio
import json
import uuid
import random
import time
import shutil
from pathlib import Path
import httpx

sys.path.append(os.path.dirname(__file__))

from colony_logger import colony_log
from colony_persistence import db
from pipeline import build_storyline_video, generate_neural_narration
from faceless_niches_engine import generate_faceless_package, FACELESS_20_NICHES
from node_youtube import publish_to_youtube_api
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
    colony_log(f"MASTER ENGINE: Generating [{faceless_pkg['channel_name']}] doc [{clean_title}]...", node="MASTER")

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
        colony_log("[-] MASTER ENGINE FAIL: Video assembly failed.", node="MASTER")
        return {"status": "error", "reason": "Render failed"}

    output_path = res_dict["output_path"]

    # 2. VAULT TO LOCAL SOVEREIGN STORAGE
    colony_log(f"MASTER ENGINE: Vaulting [{filename}] to Sovereign Storage...", node="MASTER")
    vault_dir = Path(r"C:\Users\willo\OneDrive\Desktop\Anthony_Ai\willow_rain_global\wholesale_portal\renders")
    vault_dir.mkdir(parents=True, exist_ok=True)

    vault_path = vault_dir / filename
    shutil.copy2(output_path, vault_path)

    # Generate the public URL pointing to our native web server
    public_url = f"http://obsidian-global.io/ui/renders/{filename}"

    # 3. REGISTER IN NATIVE SQLITE VIDEOS FEED
    colony_log("MASTER ENGINE: Registering in Native SQLite Videos feed...", node="MASTER")
    with db._get_connection() as conn:
        conn.execute("""
            INSERT INTO ai_videos (id, title, description, video_url, thumbnail_url, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (uuid.uuid4().hex[:8], clean_title, description_text, public_url, "", time.time()))
        conn.commit()

    # 4. DISPATCH LIVE STRICTLY TO YOUTUBE SHORTS (ONLY ACTIVE CHANNEL FOR TESTING)
    colony_log("MASTER ENGINE: Dispatching strictly to YouTube Shorts for Quality Inspection...", node="MASTER")
    yt_url = await publish_to_youtube_api(
        task={"id": 101},
        video_url=public_url,
        title=clean_title,
        description=description_text
    )

    # 5. LOG SUCCESS EVENT TO VAULT
    db.log_event("MASTER", "BURST_SUCCESS", {
        "title": clean_title,
        "video_url": public_url,
        "youtube_url": yt_url,
        "reference_handle": faceless_pkg["reference_handle"]
    })

    colony_log(f"[SUPREME] MASTER BURST COMPLETE! YouTube Live: {yt_url}", node="MASTER")

    return {
        "status": "success",
        "title": clean_title,
        "public_url": public_url,
        "youtube_url": yt_url,
        "reference_handle": faceless_pkg["reference_handle"]
    }

if __name__ == "__main__":
    asyncio.run(create_and_dispatch_documentary(niche_key="thefourthencounter", duration_tier="short"))
