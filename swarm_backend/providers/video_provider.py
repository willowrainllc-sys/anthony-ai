# --- EMPIRE VIDEO PROVIDER: NARRATIVE SNIPER ADAPTER v1.1 (BIBLE-AWARE) ---
import os
import asyncio
from typing import Optional, Dict, Any
from .base_provider import VideoProvider
from social_harvest_node import SocialHarvestNode
from swarm_logger import swarm_log

class SniperVideoProvider(VideoProvider):
    """
    Adapter for the SocialHarvestNode Sniper.
    v1.1: Uses directorial bibles to guide visual selection/generation.
    """
    def __init__(self):
        self.sniper = SocialHarvestNode()

    async def generate_video(self, prompt: str, duration: int, bible: Dict[str, Any] = None) -> Optional[str]:
        swarm_log(f"VIDEO_PROVIDER: Generating cinematic visual for [{prompt[:30]}]", node="VIDEO_PROVIDER")

        # Prepare scene data for the sniper
        scene_data = {
            "visual_prompt": prompt,
            "duration": duration
        }

        # Inject bible into search context if provided
        # The sniper uses this for genre keyword extraction and LTX synthesis guidance.
        path = await self.sniper.get_best_match_for_scene(scene_data, 0, bible=bible)
        return path

video_provider = SniperVideoProvider()
