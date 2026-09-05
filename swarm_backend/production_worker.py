# --- EMPIRE PRODUCTION WORKER: ASYNC TASK RUNNER v1.4 (RESILIENT SCENES) ---
import asyncio
import os
import json
import uuid
import time
import hashlib
from pathlib import Path
from swarm_logger import swarm_log
from swarm_persistence import db
from swarm_brain import brain_gate
from quality_control import qc_node
from metadata_engine import metadata_engine

# Universal Providers
from providers.audio_provider import audio_provider
from providers.video_provider import video_provider
from providers.opencut_provider import opencut_editor

class ProductionWorker:
    """
    BUSINESS NODE: The Executioner.
    v1.4: Implements Asset Registry check to prevent redundant generations.
    """
    async def run_worker_loop(self):
        swarm_log("WORKER: Autonomous Production Swarm active.", node="WORKER")
        self._reset_stalled_jobs()
        while True:
            try:
                job = await self._fetch_next_job()
                if job:
                    await self._execute_production_plan(job)
                else:
                    await asyncio.sleep(20)
            except Exception as e:
                swarm_log(f"[-] WORKER ERROR: {e}", node="WORKER")
                await asyncio.sleep(60)

    async def _fetch_next_job(self):
        with db._get_connection() as conn:
            row = conn.execute("""
                SELECT job_id, page_id, manifest, status FROM production_jobs
                WHERE status='QUEUED' ORDER BY created_at ASC LIMIT 1
            """).fetchone()
            if row:
                conn.execute("UPDATE production_jobs SET status='GENERATING', updated_at=? WHERE job_id=?", (time.time(), row[0]))
                conn.commit()
                return {"id": row[0], "page_id": row[1], "manifest": json.loads(row[2])}
        return None

    async def _execute_production_plan(self, job: dict):
        job_id = job['id']
        manifest = job['manifest']
        swarm_log(f"WORKER: Launching Production for Job [{job_id}]", node="WORKER")

        try:
            # 1. OPTIMIZE METADATA
            self._update_job_status(job_id, "GENERATING", stage="METADATA_OPT", progress=10)
            niche = manifest.get('niche', 'General AI')
            optimized_meta = await metadata_engine.optimize_for_grid(
                script_body=manifest.get('description', ''),
                niche=niche,
                original_title=manifest.get('title')
            )

            # 2. GENERATE ASSETS IN PARALLEL
            self._update_job_status(job_id, "GENERATING", stage="PARALLEL_ASSETS", progress=20)

            # A. Audio Tasks (Skip if already in Registry)
            full_script = " ... ".join([s.get('narration', '') for s in manifest.get('scenes', [])])
            vocal_id = hashlib.md5(f"vo_{full_script}".encode()).hexdigest()
            vocal_path = self._check_registry(vocal_id)

            if not vocal_path:
                vocal_path = await audio_provider.generate_speech(full_script, "en-US-AvaNeural")
                self._register_asset(vocal_id, job_id, "AUDIO_VO", vocal_path)

            manifest['vocal_path'] = vocal_path

            music_path = await audio_provider.generate_music("Cinematic", 120)
            manifest['music_path'] = music_path

            # B. Visual Tasks with Scene-Level Resilience
            visual_tasks = []
            bible = manifest.get('bibles', {})
            scenes = manifest.get('scenes', [])

            for i, scene in enumerate(scenes):
                # Check Registry for this specific scene prompt
                scene_prompt = scene.get('visual_prompt', '')
                scene_key = hashlib.md5(f"{scene_prompt}_{scene.get('duration')}".encode()).hexdigest()

                existing_path = self._check_registry(scene_key)
                if existing_path and os.path.exists(existing_path):
                    swarm_log(f"WORKER: Scene {i+1} found in registry. Skipping generation.", node="WORKER")
                    scene['path'] = existing_path
                else:
                    visual_tasks.append(self._generate_scene_and_register(scene, bible, scene_key, job_id, i+1))

            if visual_tasks:
                await asyncio.gather(*visual_tasks)

            # 3. OPENCUT ASSEMBLY
            self._update_job_status(job_id, "EDITING", progress=80)
            final_path = str(Path(r"D:\AnthonyAi_Swarm\Renderings") / f"final_{job_id}.mp4")
            success = await opencut_editor.assemble_video(manifest, final_path)

            if success and os.path.exists(final_path):
                # 4. QUALITY CONTROL
                self._update_job_status(job_id, "QC", progress=90)
                is_valid, q_msg = await qc_node.verify_strike_readiness(final_path, manifest)

                if is_valid:
                    self._update_job_status(job_id, "READY", final_path, progress=100)

                    # 5. DISPATCH
                    platforms = ["YOUTUBE", "FACEBOOK", "INSTA_THREADS", "TIKTOK", "ANTHONY_AI_APP"]
                    platform_meta = optimized_meta.get('platforms', {})

                    for hub in platforms:
                        hub_key = hub.lower().replace("_threads", "")
                        hub_data = platform_meta.get(hub_key, {})

                        payload = {
                            "title": optimized_meta['title'],
                            "description": hub_data.get('body', manifest.get('description')),
                            "video_url": final_path,
                            "job_id": job_id,
                            "bible": manifest.get('bibles'),
                            "thumbnail_concept": optimized_meta.get('thumbnail_concept')
                        }
                        db.push_task(hub, payload, priority=10)

                    swarm_log(f"WORKER: Mission [{optimized_meta['title']}] SUCCESS.", node="WORKER")
                else:
                    self._update_job_status(job_id, f"QC_FAILED: {q_msg}")
            else:
                self._update_job_status(job_id, "RENDER_FAILED")

        except Exception as e:
            swarm_log(f"[-] WORKER CRITICAL: {e}", node="WORKER")
            self._update_job_status(job_id, f"ERROR: {str(e)}")

    async def _generate_scene_and_register(self, scene, bible, key, job_id, index):
        prompt = scene.get('visual_prompt', 'cinematic high fidelity')
        duration = scene.get('duration', 15)
        path = await video_provider.generate_video(prompt, duration, bible=bible)
        if path:
            scene['path'] = path
            self._register_asset(key, job_id, f"SCENE_{index}", path)
        return path

    def _check_registry(self, asset_id):
        with db._get_connection() as conn:
            row = conn.execute("SELECT path FROM asset_registry WHERE asset_id=? AND status='SUCCESS'", (asset_id,)).fetchone()
            return row[0] if row else None

    def _register_asset(self, asset_id, job_id, type_str, path):
        with db._get_connection() as conn:
            conn.execute("""
                INSERT OR REPLACE INTO asset_registry (asset_id, job_id, type, path, status)
                VALUES (?, ?, ?, ?, 'SUCCESS')
            """, (asset_id, job_id, type_str, path))
            conn.commit()

    def _update_job_status(self, job_id, status, path="", stage=None, progress=None):
        with db._get_connection() as conn:
            query = "UPDATE production_jobs SET status=?, final_video_path=?, updated_at=?"
            params = [status, path, time.time()]
            if stage:
                query += ", current_stage=?"
                params.append(stage)
            if progress is not None:
                query += ", progress=?"
                params.append(progress)
            query += " WHERE job_id=?"
            params.append(job_id)
            conn.execute(query, params)
            conn.commit()

    def _reset_stalled_jobs(self):
        with db._get_connection() as conn:
            conn.execute("UPDATE production_jobs SET status='QUEUED' WHERE status IN ('GENERATING', 'EDITING')")
            conn.commit()
            swarm_log("WORKER: Stalled jobs reset to QUEUED.", node="WORKER")

if __name__ == "__main__":
    asyncio.run(ProductionWorker().run_worker_loop())
