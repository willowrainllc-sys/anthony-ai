# --- WILLOW RAIN COMPANY LLC: LONG-FORM DOCUMENTARY PRODUCTION ORCHESTRATOR v1.0 ---
import os
import sys
import json
import uuid
import time
import asyncio
from pathlib import Path
from colony_logger import colony_log
from colony_persistence import db
from longform_15min_director import longform_15m_director
from visual_director_v4 import visual_director_librarian
from pipeline import build_storyline_video
from production_qa_gate import qa_gate
from node_youtube import publish_to_youtube_api

# Mock StoryPlan classes to bridge 15-min chapters to the Visual Director
from pydantic import BaseModel
class MockShot(BaseModel):
    shot_id: str
    visual_prompt: str
    camera_motion: str = "slow cinematic movement"
    duration_seconds: float = 20.0 # 180s / 9 shots = 20s per shot

class MockScene(BaseModel):
    scene_id: str
    narration: str
    start_state: str = "Cinematic documentary environment"
    location_id: str = "cloud_data_center"
    shots: list

class MockStoryPlan(BaseModel):
    title: str
    scenes: list

class LongformProductionOrchestrator:
    """
    LONG-FORM PRODUCTION ORCHESTRATOR v1.0:
    Bridges the 15-Minute Deep Lore Director with the 4K Visual Director and Video Pipeline.
    1. Generates 3,000-word 5-chapter script.
    2. Resolves 45+ distinct 4K video shots.
    3. Renders a full 15-minute 1080p widescreen documentary.
    """
    async def execute_longform_burst(self, publish_live: bool = False) -> dict:
        colony_log("LONGFORM_BURST: Architecting 9-Minute Documentary...", node="LONGFORM_BURST")

        # 1. Generate 9-Min Story Plan
        plan = longform_15m_director.generate_random_15min_documentary()
        job_id = f"job_9m_{uuid.uuid4().hex[:6]}"

        # 2. Map Chapters to Visual Scenes
        mock_scenes = []
        for ch in plan.chapters:
            chapter_shots = []
            for i in range(ch.shots_count):
                chapter_shots.append({
                    "shot_id": f"ch{ch.chapter_number}_s{i+1}",
                    "visual_prompt": f"{ch.chapter_title}: {ch.narration_script[:60]}... cinematic 4k"
                })

            mock_scenes.append({
                "scene_id": f"chapter_{ch.chapter_number}",
                "narration": ch.narration_script,
                "shots": chapter_shots
            })

        # 3. Register FULL Job in Database
        with db._get_connection() as conn:
            full_manifest = {
                "title": plan.title,
                "description": " ".join([ch.narration_script for ch in plan.chapters]),
                "scenes": mock_scenes,
                "bibles": {
                    "global_style": "cinematic documentary 4k, National Geographic aesthetic",
                    "character": "human observers",
                    "environment": "atmospheric locations"
                },
                "niche": "History",
                "duration_tier": "mid", # 9 minutes is 'mid' tier
                "publish_live": publish_live
            }
            conn.execute("""
                INSERT INTO production_jobs (job_id, page_id, status, progress, current_stage, manifest)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (job_id, "WILLOW_RAIN_OFFICIAL", 'QUEUED', 10, 'PLAN_LOCKED', json.dumps(full_manifest)))
            conn.commit()

        colony_log(f" LONGFORM_BURST SUCCESS: 9-Minute Job [{job_id}] queued.", node="LONGFORM_BURST")
        return {"status": "QUEUED", "job_id": job_id, "title": plan.title}

longform_orchestrator = LongformProductionOrchestrator()

if __name__ == "__main__":
    # Test a partial render (headless)
    asyncio.run(longform_orchestrator.execute_longform_burst(publish_live=False))
