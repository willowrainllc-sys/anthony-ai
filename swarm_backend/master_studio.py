# --- EMPIRE MASTER STUDIO: A-ROLL & B-ROLL DUAL-LAYER CINEMATIC STUDIO v14.0 ---
import os
import sys
import asyncio
import json
import uuid
import random
import re
from pathlib import Path

sys.path.append(os.path.dirname(__file__))

from swarm_logger import swarm_log
from swarm_persistence import db
from media_studio_brain import studio_brain, ContentContext
from series_director import HashtagValidator
from pipeline import generate_neural_narration, build_storyline_video
from science_randomizer import science_randomizer
from aroll_presenter_engine import aroll_engine
from node_youtube import publish_to_youtube_api
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv(dotenv_path=Path(__file__).resolve().parent.parent / ".env")
supabase: Client = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))

class MasterStudioFactory:
    """
    A-ROLL & B-ROLL DUAL-LAYER CINEMATIC STUDIO v14.0:
    Interleaves primary A-Roll presenter host footage with supporting 4K B-roll visuals,
    voiceover narration, floating captions, and background instrumentals.
    """
    def _is_duplicate_upload(self, title: str) -> bool:
        try:
            with db._get_connection() as conn:
                row = conn.execute("SELECT id FROM empire_events WHERE metadata LIKE ? LIMIT 1", (f"%{title[:30]}%",)).fetchone()
                return row is not None
        except:
            return False

    async def produce_and_dispatch_episode(
        self,
        channel_id: str = "ANTHONY_AI_OFFICIAL",
        category: str = "exoplanetary_anomalies",
        ep_num: int = 1,
        target_min: int = 1,
        content_type: str = "SHORT_FORM",
        text_only: bool = False,
        voice_type: str = "expressive_female"
    ) -> dict:
        swarm_log(f"STUDIO: Initiating A-Roll + B-Roll Production [{category.upper()} | {target_min} MIN]...", node="STUDIO")

        # 1. PULL REAL SCIENCE / STORY CONTEXT
        science_payload = science_randomizer.generate_script_structure(category_key=category, target_format="dual")
        doc_data = science_payload["short_form_3min"] if target_min <= 3 else science_payload["long_form_20min"]

        title = doc_data["title"]
        full_script = doc_data["script"] if "script" in doc_data else doc_data.get("full_script", "")
        broll_prompts = doc_data["prompts"]

        if self._is_duplicate_upload(title):
            swarm_log(f"STUDIO: Title [{title}] already published. Pulling fresh topic...", node="STUDIO")
            science_payload = science_randomizer.generate_script_structure(target_format="dual")
            doc_data = science_payload["short_form_3min"] if target_min <= 3 else science_payload["long_form_20min"]
            title = doc_data["title"]
            full_script = doc_data["script"] if "script" in doc_data else doc_data.get("full_script", "")
            broll_prompts = doc_data["prompts"]

        # Clean script text
        full_script = re.sub(r'Season \d+|Episode \d+|Key evidence:|In this video|Today we are going to', '', full_script).strip()

        # 2. SNIPE PRIMARY A-ROLL PRESENTER FOOTAGE
        aroll_host_clip = await aroll_engine.get_aroll_presenter_clip(category=category)

        # 3. INTERLEAVE A-ROLL PRESENTER WITH B-ROLL VISUALS
        scene_prompts = []
        if aroll_host_clip:
            scene_prompts.append(aroll_host_clip) # Scene 1: A-Roll Host Anchor
        scene_prompts.extend(broll_prompts)       # Scene 2-4: B-Roll Supporting Visuals

        # 4. GENERATE SYNCHRONIZED METADATA & HASHTAGS
        raw_hashtags = doc_data["tags"] + ["#ARoll", "#Presenter", "#Science", "#WillowRainCompany"]
        ctx_mock = ContentContext(
            channel_id=channel_id, series_id=f"science_{category}", season_id="season_01", episode_id=f"ep_{ep_num:02d}",
            category=category, content_mode="DOCUMENTARY", text_only=text_only, audience_profile="Science lovers",
            emotional_trigger="Awe", series_title="Real Science & Astronomical Anomalies", series_theme="Cosmology",
            season_theme="Exoplanet Discoveries", episode_number=ep_num, episode_title=title, episode_topic=title,
            primary_subject=title, secondary_subjects=["Cosmology", "Astronomy"], entities=["NASA", "JWST"],
            locations=["Deep Space"], keywords=["science", "astronomy", "aroll"], story_summary=full_script[:150],
            hook=full_script[:100], body_evidence=full_script[100:250], climax_payoff=full_script[250:],
            unresolved_questions="What lies beyond?", target_duration_sec=target_min * 60, content_type=content_type,
            visual_style="A-Roll Host + B-Roll 8K", narration_style=voice_type
        )
        validated_hashtags = HashtagValidator.validate_and_filter_hashtags(raw_hashtags, ctx_mock)

        description = f"{full_script[:150]}...\n\nReal Science & Astronomical Anomalies (A-Roll + B-Roll Feature) - Episode {ep_num}\n\n{' '.join(validated_hashtags)}"

        filename = f"studio_aroll_{category}_{uuid.uuid4().hex[:4]}.mp4"
        duration_tier = "short" if target_min <= 3 else "mid"

        # 5. RENDER FULL A-ROLL + B-ROLL VIDEO
        res_dict = await build_storyline_video(
            title=title,
            script_narration=full_script,
            scene_prompts=scene_prompts,
            output_filename=filename,
            duration_tier=duration_tier,
            category="inspirational",
            text_only=text_only
        )

        if not res_dict or not os.path.exists(res_dict.get("output_path", "")):
            return {"status": "error", "reason": "Render failed"}

        output_path = res_dict["output_path"]

        public_url = output_path
        # 6. UPLOAD TO SUPABASE STORAGE WITH VIDEO/MP4 MIME TYPE
        try:
            storage_path = f"renders/studio_{filename}"
            with open(output_path, "rb") as f:
                supabase.storage.from_("ai-videos").upload(
                    storage_path,
                    f,
                    file_options={"content-type": "video/mp4", "upsert": "true"}
                )
            public_url = supabase.storage.from_("ai-videos").get_public_url(storage_path)

            # REGISTER IN SUPABASE VIDEOS FEED
            supabase.table("videos").insert({
                "title": title,
                "description": description,
                "video_url": public_url,
                "creator": "Anthony AI",
                "posted": "Just Now"
            }).execute()
        except Exception as e:
            swarm_log(f"STUDIO Supabase Sync Note: {e}", node="STUDIO")

        # 7. DISPATCH LIVE STRICTLY TO YOUTUBE SHORTS
        yt_url = await publish_to_youtube_api(
            task={"id": 3001},
            video_url=public_url,
            title=title,
            description=description
        )

        db.log_event("STUDIO", "STRIKE_SUCCESS", {
            "series_id": f"science_{category}",
            "episode_id": f"ep_{ep_num:02d}",
            "title": title,
            "video_url": public_url,
            "youtube_url": yt_url
        })

        swarm_log(f"🔱 A-ROLL + B-ROLL PRODUCTION COMPLETE! YouTube Live: {yt_url}", node="STUDIO")

        return {
            "status": "success",
            "title": title,
            "public_url": public_url,
            "youtube_url": yt_url,
            "aroll_host": aroll_host_clip
        }

master_factory = MasterStudioFactory()

if __name__ == "__main__":
    asyncio.run(master_factory.produce_and_dispatch_episode("ANTHONY_AI_OFFICIAL", "exoplanetary_anomalies", ep_num=1, target_min=1, text_only=False))
