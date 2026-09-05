# --- EMPIRE MASTER STUDIO: GENERAL-PURPOSE FACELESS AI MEDIA STUDIO v2.0 ---
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
from media_studio_framework import media_studio, ContentContext
from series_director import HashtagValidator
from pipeline import generate_neural_narration, build_storyline_video
from node_youtube import publish_to_youtube_api
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv(dotenv_path=Path(__file__).resolve().parent.parent / ".env")
supabase: Client = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))

class ContentQualityControl:
    """Automated Content QA Gatekeeper."""
    @staticmethod
    def verify_content_readiness(ctx: ContentContext, video_path: str, actual_duration_sec: float) -> tuple:
        if not os.path.exists(video_path) or os.path.getsize(video_path) < 500000:
            return False, "File missing or corrupted"

        if ctx.content_type == "SHORT_FORM" and actual_duration_sec < 60:
            return False, f"Short duration ({actual_duration_sec:.1f}s) below 60s minimum requirement"

        if ctx.content_type == "LONG_FORM" and actual_duration_sec < 600: # 10 mins
            return False, f"Long-form duration ({actual_duration_sec:.1f}s) below 10 min minimum requirement"

        return True, "Passed Content QA"

class MasterStudioFactory:
    """
    CANONICAL GENERAL-PURPOSE AI MEDIA STUDIO:
    Supports all 2026 faceless niches (fantasy, anime, scifi, history, finance, horror, etc.)
    governed strictly by the canonical ContentContext (SINGLE SOURCE OF TRUTH).
    """
    async def produce_and_dispatch_episode(self, channel_id: str = "ANTHONY_AI_OFFICIAL", niche: str = "fantasy", ep_num: int = 1, target_min: int = 12, content_type: str = "LONG_FORM") -> dict:
        swarm_log(f"STUDIO: Initiating General-Purpose Studio production for Ep {ep_num} [{niche.upper()}]...", node="STUDIO")

        # 1. GENERATE CANONICAL CONTENT CONTEXT
        ctx = await media_studio.get_canonical_context(channel_id, niche, ep_num, target_min, content_type)

        # 2. GENERATE EPISODE SCRIPT (140 words per min target)
        target_words = target_min * 140
        full_script = f"{ctx.hook} {ctx.story_summary} Key evidence and developments: {ctx.evidence_or_climax}. {ctx.unresolved_questions} {ctx.next_episode_tease}"

        # Expand script narrative for full duration target
        narrative_expansion = [
            f"As events unfolded in the {ctx.niche} domain, researchers and observers documented unprecedented changes.",
            f"The primary focus, {ctx.primary_subject}, presented challenges that traditional models could not explain.",
            f"Key findings in {ctx.locations[0]} confirmed that the underlying mechanism was far more complex than initially thought.",
            f"Looking ahead to the next episode, the consequences of {ctx.primary_subject} continue to reshape the landscape."
        ]
        while len(full_script.split()) < target_words and target_min > 3:
            full_script += " " + random.choice(narrative_expansion)

        # 3. GENERATE SYNCHRONIZED METADATA & HASHTAGS FROM CONTEXT
        raw_hashtags = [f"#{kw.replace(' ', '')}" for kw in ctx.keywords] + [f"#{ctx.niche.capitalize()}", "#Documentary", "#Series"]
        validated_hashtags = HashtagValidator.validate_and_filter_hashtags(raw_hashtags, ctx)

        title = f"{ctx.episode_title}: {ctx.primary_subject}"
        description = f"{ctx.hook}\n\n{ctx.story_summary}\n\nSeries: {ctx.series_title} - Season 1 Episode {ctx.episode_number}\n\n{' '.join(validated_hashtags)}"

        # 4. RENDER EPISODE MP4 WITH DYNAMIC VISUAL PROMPTS
        filename = f"studio_{ctx.series_id}_{ctx.episode_id}.mp4"
        scene_prompts = [
            f"{ctx.primary_subject}, {ctx.visual_style}",
            f"{ctx.locations[0]}, {ctx.visual_style}",
            f"{ctx.niche} exploration scene, {ctx.visual_style}"
        ]

        duration_tier = "short" if target_min <= 3 else "mid"
        res_dict = await build_storyline_video(
            title=title,
            script_narration=full_script[:1200], # Pass main narrative section
            scene_prompts=scene_prompts,
            output_filename=filename,
            duration_tier=duration_tier,
            category="mystery"
        )

        if not res_dict or not os.path.exists(res_dict.get("output_path", "")):
            return {"status": "error", "reason": "Render failed"}

        output_path = res_dict["output_path"]

        # 5. UPLOAD TO SUPABASE STORAGE WITH VIDEO/MP4 MIME TYPE
        storage_path = f"renders/studio_{filename}"
        with open(output_path, "rb") as f:
            supabase.storage.from_("ai-videos").upload(
                storage_path,
                f,
                file_options={"content-type": "video/mp4", "upsert": "true"}
            )

        public_url = supabase.storage.from_("ai-videos").get_public_url(storage_path)

        # 6. REGISTER IN SUPABASE VIDEOS FEED (APP FEED)
        supabase.table("videos").insert({
            "title": title,
            "description": description,
            "video_url": public_url,
            "creator": "Anthony AI",
            "posted": "Just Now"
        }).execute()

        # 7. DISPATCH LIVE STRICTLY TO YOUTUBE SHORTS (ONLY ACTIVE CHANNEL FOR TESTING)
        yt_url = await publish_to_youtube_api(
            task={"id": 301},
            video_url=public_url,
            title=title,
            description=description
        )

        db.log_event("STUDIO", "STRIKE_SUCCESS", {
            "series_id": ctx.series_id,
            "episode_id": ctx.episode_id,
            "title": title,
            "video_url": public_url,
            "youtube_url": yt_url
        })

        swarm_log(f"🔱 STUDIO PRODUCTION COMPLETE! YouTube Live: {yt_url}", node="STUDIO")

        return {
            "status": "success",
            "title": title,
            "public_url": public_url,
            "youtube_url": yt_url,
            "content_context": ctx
        }

master_factory = MasterStudioFactory()

if __name__ == "__main__":
    asyncio.run(master_factory.produce_and_dispatch_episode("ANTHONY_AI_OFFICIAL", "fantasy", ep_num=1, target_min=1))
