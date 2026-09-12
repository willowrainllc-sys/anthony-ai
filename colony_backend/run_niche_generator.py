# --- EMPIRE AUTONOMOUS NICHE VIDEO GENERATION PIPELINE v2.0 (RUN_NICHE_GENERATOR.PY) ---
import os
import sys
import json
import uuid
import time
import asyncio
from pathlib import Path

sys.path.append(os.path.dirname(__file__))

from colony_logger import colony_log
from colony_persistence import db
from story_director_v2 import story_director_v2
from story_director_v3 import story_director_v3
from visual_director_v4 import visual_director_librarian
from pipeline import build_storyline_video
from production_qa_gate import qa_gate, ProductionJobState
from node_youtube import publish_to_youtube_api
from dotenv import load_dotenv

load_dotenv(dotenv_path=Path(__file__).resolve().parent.parent / ".env")

PUBLISH_LIVE_ENV = os.getenv("PUBLISH_LIVE", "false").lower() == "true"

async def build_random_niche_masterpiece():
    """
    AUTONOMOUS NICHE VIDEO GENERATION PIPELINE v2.0:
    Executes 3-Minute (180s) 6-Beat "Director Cut" documentary production:
    1. Story Director V3 Random Topic Engine -> Production Blueprint (180s Duration)
    2. Visual Director V4.2 -> Resolved Production Timeline
    3. Pipeline Video & Neural Audio Generation -> Render Output (niche_director_cut_live.mp4)
    4. Production QA Gate Audit
    5. Environment-Gated YouTube Publishing
    """
    job_id = f"job_niche_{uuid.uuid4().hex[:8]}"
    colony_log(f"1. STARTING AUTONOMOUS NICHE PIPELINE [{job_id}]...", node="NICHE_GEN")

    # Step 1: Generate 3-Minute Production Story Plan
    blueprint = story_director_v3.generate_director_blueprint()
    colony_log(f"   [] Topic: {blueprint.topic}", node="NICHE_GEN")
    colony_log(f"   [] Title: {blueprint.title}", node="NICHE_GEN")

    # Map to StoryPlan for Visual Director v4.2 resolution
    story_plan = story_director_v2.generate_production_story_plan(blueprint.topic)

    # Step 2: Resolve Structured Production Timeline
    colony_log(f"2. RESOLVING VISUAL TIMELINE VIA VISUAL DIRECTOR V4.2...", node="NICHE_GEN")
    production_timeline = await visual_director_librarian.resolve_production_timeline(story_plan)

    # Step 3: Render 3-Minute Cinematic Video (niche_director_cut_live.mp4)
    colony_log(f"3. RENDERING 3-MINUTE CINEMATIC VIDEO (niche_director_cut_live.mp4)...", node="NICHE_GEN")
    res = await build_storyline_video(
        production_timeline=production_timeline,
        output_filename="niche_director_cut_live.mp4",
        duration_tier="mid",
        category="mystery",
        text_only=False
    )

    if not res or not res.get("output_path"):
        colony_log("[-] NICHE PIPELINE FAIL: Video rendering returned no output.", node="NICHE_GEN")
        return {"status": "error", "message": "Render failed"}

    v_path = res["output_path"]
    full_script = " ".join([s.narration_text for s in production_timeline.shots])

    # Step 4: Environment-Gated Live YouTube Publishing
    if PUBLISH_LIVE_ENV:
        colony_log("4. PUBLISHING LIVE TO YOUTUBE...", node="NICHE_GEN")
        desc = f"{full_script}\n\n#AnomalyDeepDive #WillowRain #Documentary #History #Science #CGI #ObsidianMedia"
        yt_url = await publish_to_youtube_api(task={"id": 6001}, video_url=v_path, title=blueprint.title, description=desc)
        colony_log(f"=== LIVE YOUTUBE 3-MIN NICHE RESULT: {yt_url} ===", node="NICHE_GEN")
        return {"status": "published", "title": blueprint.title, "youtube_url": yt_url, "video_path": v_path}
    else:
        colony_log(f" TEST MODE (PUBLISH_LIVE=false): Video rendered locally at {v_path}", node="NICHE_GEN")
        return {"status": "rendered_local", "title": blueprint.title, "video_path": v_path}

if __name__ == "__main__":
    result = asyncio.run(build_random_niche_masterpiece())
    print("\nAUTONOMOUS NICHE GENERATOR RESULT:")
    print(json.dumps(result, indent=2))
