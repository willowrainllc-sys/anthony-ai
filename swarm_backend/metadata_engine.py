# --- EMPIRE METADATA ENGINE: CONVERSION OPTIMIZER v1.1 (PLATFORM-SPECIFIC) ---
import asyncio
import json
import re
from swarm_logger import swarm_log
from swarm_brain import brain_gate

class MetadataEngine:
    """
    BUSINESS NODE: CTR Architect.
    Optimizes for peak curiosity and specific platform requirements.
    """
    async def optimize_for_grid(self, script_body: str, niche: str, original_title: str):
        swarm_log(f"METADATA: Architecting multi-platform distribution for [{original_title[:20]}]", node="METADATA")

        # 1. GENERATE TITLE POOL & THUMBNAIL CONCEPT
        prompt = f"""
        NICHE: {niche}
        SCRIPT: {script_body[:1200]}
        TASK: Generate the ultimate metadata package.
        1. 10 curiosity-gap titles (The [X] Trap, Why [X] is vanishing).
        2. A THUMBNAIL CONCEPT: Visual description of a high-click image (The 'Hook' in still form).
        3. PLATFORM CAPTIONS: Unique atmospheric descriptions for TikTok, IG, and Facebook.
        Format: JSON only.
        """

        res = await brain_gate.generate_serialized(prompt, complexity="medium", format="json")
        try:
            package = json.loads(res)
            # Pick best title from pool
            best_title = await self._score_and_select_title(package.get('titles', [original_title]), niche)

            return {
                "title": best_title,
                "hashtags": package.get('hashtags', "#Sovereign #AI #Cinema"),
                "thumbnail_concept": package.get('thumbnail_concept', "Cinematic high-contrast shot of subject"),
                "platforms": package.get('platforms', {
                    "tiktok": {"hook": "Strong immediately", "body": "Fast-paced summary"},
                    "instagram": {"hook": "Visual-first", "body": "Rich storytelling"},
                    "facebook": {"hook": "Context-heavy", "body": "Full narrative arc"}
                })
            }
        except:
            return {"title": original_title, "hashtags": "#AI #Empire", "thumbnail_concept": "Cinematic visual", "platforms": {}}

    async def _score_and_select_title(self, titles: list, niche: str):
        prompt = f"""
        TASK: Select the highest CTR title for {niche} audience.
        TITLES: {titles}
        Return ONLY the chosen title text.
        """
        return await brain_gate.generate_serialized(prompt, format="text", complexity="medium")

metadata_engine = MetadataEngine()
