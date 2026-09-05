# --- ANTHONY HYPER-CHARGED PUBLISHER: GLOBAL CONTENT GRID v7.1 (LIVE-INJECT) ---
import os
import sys
import asyncio
import subprocess
import random
import time
import uuid
import json
import hashlib
from pathlib import Path
from swarm_logger import swarm_log
from swarm_persistence import db
from content_director import director

import imageio_ffmpeg
FFMPEG_EXE = imageio_ffmpeg.get_ffmpeg_exe() or "ffmpeg"

# Configuration Paths
OUTPUT_DIR = Path("D:/AnthonyAi_Swarm/Renderings")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# --- DIRECTORIAL SUBJECT POOL (EXPANDED DYNAMIC POOL) ---
SUBJECT_POOL = [
    "The lost civilization of the Gobi Desert",
    "Neural link breakthroughs in the year 2045",
    "The secret life of deep-sea colossal squids",
    "How AI agents are taking over global logistics",
    "The last stand of the Iron Samurai in Neo-Tokyo",
    "Exploring the diamond rain on Neptune",
    "The architecture of the first Martian colony",
    "Quantum computing and the end of encryption",
    "The mystery of the Wow! signal from deep space",
    "Inside the world's most secure digital vault",
    "The rise of holographic influencers in 2026",
    "Subterranean cities discovered beneath the Sahara",
    "The evolution of synthetic biology in the Amazon",
    "Autonomous drone swarms in the future of warfare",
    "The philosophy of sovereign AI in a post-human era"
]

class AutonomousDirectorAgent:
    """
    BUSINESS NODE: The Strategist.
    Identifies subjects and queues production jobs in the Vault.
    v7.1: Supports Live Injection from App/DB.
    """
    def __init__(self):
        # Fallback niche for manual strikes without payload
        self.niche_query = random.choice(SUBJECT_POOL)

    async def run_director_cycle(self, injected_subject: str = None):
        swarm_log("DIRECTOR: Planning next autonomous mission...", node="CORE")

        # 1. Get Plan (from injection or trend-autopilot)
        if injected_subject:
            from director_score_engine import director_engine
            # Direct hit for specific user request
            manifest = await director_engine.build_high_retention_mini_doc(injected_subject)
            manifest['page_id'] = "ANTHONY_AI_OFFICIAL" # Default for injection
            manifest['niche'] = "User Injected"
        else:
            manifest = await director.run_autopilot_cycle()

        if manifest and "scenes" in manifest:
            job_id = f"job_{uuid.uuid4().hex[:8]}"
            page_id = manifest.get('page_id', 'GLOBAL_NODE')

            # 2. Persist the Job in the Vault
            with db._get_connection() as conn:
                conn.execute("""
                    INSERT INTO production_jobs (job_id, page_id, status, manifest, current_stage)
                    VALUES (?, ?, ?, ?, ?)
                """, (job_id, page_id, 'QUEUED', json.dumps(manifest), 'IDEATION'))
                conn.commit()

            swarm_log(f"DIRECTOR: Mission [{manifest.get('title')}] queued. JOB_ID: {job_id}", node="CORE")
            return True
        return False

    async def fetch_production_assets(self, manifest, video_id):
        """Targeted Asset Sniping"""
        scenes = manifest.get("scenes", [])
        swarm_log(f"DIRECTOR: Scoping {len(scenes)} clips for narrative arc.", node="CORE")
        python_exe = sys.executable
        temp_clips = []

        for i, scene in enumerate(scenes):
            scene_path = OUTPUT_DIR / f"clip_{video_id}_{i}.mp4"
            search_query = f"{scene['visual_prompt']} cinematic 4k"

            try:
                duration = int(scene.get('duration', 15))
                cmd = [
                    python_exe, "-m", "yt_dlp",
                    "-f", "bestvideo[ext=mp4][height<=1080]+bestaudio[ext=m4a]/best[ext=mp4]/best",
                    "--ffmpeg-location", FFMPEG_EXE,
                    "--max-downloads", "1",
                    "--match-filter", "duration < 600",
                    "--download-sections", f"*0-{duration + 5}",
                    "-o", str(scene_path),
                    "--quiet", "--no-warnings",
                    f"ytsearch1:{search_query}"
                ]
                proc = await asyncio.create_subprocess_exec(*cmd)
                await asyncio.wait_for(proc.wait(), timeout=120.0)

                final_clip = None
                if scene_path.exists():
                    final_clip = str(scene_path)
                else:
                    for f in OUTPUT_DIR.glob(f"clip_{video_id}_{i}*.mp4"):
                        if f.stat().st_size > 500000:
                            final_clip = str(f)
                            break

                if final_clip:
                    scene["path"] = final_clip
                    temp_clips.append(final_clip)
                else:
                    swarm_log(f"[-] Scene {i+1} fail. Sniping fallback...", node="CORE")
                    from social_harvest_node import SocialHarvestNode
                    sniper = SocialHarvestNode()
                    v_path = await sniper.fetch_youtube_cinematic(scene['visual_prompt'])
                    if v_path:
                        scene["path"] = v_path
                        temp_clips.append(v_path)
            except Exception as e:
                swarm_log(f"[-] Clip fetch error: {e}", node="CORE")

        return len(temp_clips) >= 2

async def run_autopilot_loop():
    swarm_log("🔱 ANTHONY DIRECTOR ENGINE: v7.1 Submitter active.", node="CORE")
    agent = AutonomousDirectorAgent()
    while True:
        try:
            with db._get_connection() as conn:
                # 1. Check for Injected Subjects
                injected = conn.execute("SELECT id, subject FROM injected_prompts WHERE status='PENDING' ORDER BY priority DESC LIMIT 1").fetchone()

                # 2. Check active jobs
                active_jobs = conn.execute("SELECT COUNT(*) FROM production_jobs WHERE status IN ('QUEUED', 'GENERATING', 'EDITING')").fetchone()[0]

            if injected:
                prompt_id, subject = injected
                swarm_log(f"🔥 LIVE INJECTION: [{subject}]", node="CORE")
                success = await agent.run_director_cycle(injected_subject=subject)
                if success:
                    with db._get_connection() as conn:
                        conn.execute("UPDATE injected_prompts SET status='EXECUTED' WHERE id=?", (prompt_id,))
                        conn.commit()

            elif active_jobs < 2:
                await agent.run_director_cycle()

            await asyncio.sleep(300)
        except Exception as e:
            swarm_log(f"[-] DIRECTOR ERROR: {e}", node="CORE")
            await asyncio.sleep(60)

if __name__ == "__main__":
    asyncio.run(run_autopilot_loop())
