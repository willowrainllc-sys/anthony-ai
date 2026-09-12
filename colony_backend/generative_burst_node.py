# --- EMPIRE GENERATIVE BURST: OBSIDIAN LOCAL PIPELINE v2.0 ---
import os
import sys
import httpx
import asyncio
import uuid
import random
import json
import urllib.parse
from pathlib import Path
from colony_logger import colony_log
from dotenv import load_dotenv

# Use absolute path for local import
sys.path.append(os.path.dirname(__file__))

load_dotenv(dotenv_path=Path(__file__).resolve().parent.parent / ".env")

TOGETHER_KEY = os.getenv("TOGETHER_AI_API_KEY")
RUNWARE_KEY = os.getenv("RUNWARE_API_KEY") # User's key might be Runware
VIDEOS_DIR = Path(__file__).resolve().parent.parent / "secure_assets" / "source_videos"
PHOTOS_DIR = Path(__file__).resolve().parent.parent / "secure_assets" / "source_photos"

class GenerativeBurstNode:
    """
    ELITE OBSIDIAN PIPELINE:
    1. Local FLUX (Diffusers) - Absolute Authority
    2. Pollinations.ai - High Speed / Zero Cost
    3. Stock Sniper Fallback
    """
    def __init__(self):
        VIDEOS_DIR.mkdir(parents=True, exist_ok=True)
        PHOTOS_DIR.mkdir(parents=True, exist_ok=True)
        self.local_pipe = None

    def _init_local_flux(self):
        """Lazy loads local FLUX.1-schnell if hardware permits."""
        if self.local_pipe is not None: return True

        try:
            import torch
            from diffusers import FluxPipeline

            colony_log("GEN_BURST: Initializing Local FLUX.1-schnell Authority...", node="GENERATOR")

            # Using bfloat16 for speed/VRAM efficiency
            self.local_pipe = FluxPipeline.from_pretrained(
                "black-forest-labs/FLUX.1-schnell",
                torch_dtype=torch.bfloat16
            )

            if torch.cuda.is_available():
                self.local_pipe.to("cuda")
                self.local_pipe.enable_model_cpu_offload() # Save VRAM
            elif hasattr(torch, 'xpu') and torch.xpu.is_available():
                self.local_pipe.to("xpu")

            return True
        except Exception as e:
            colony_log(f"[-] Local FLUX Load Fail: {e}", node="GENERATOR")
            return False

    async def trigger_alpha_video(self, prompt_text: str, visual_cue: str = ""):
        colony_log(f"GEN_BURST: Launching high-fidelity Alpha render: [{visual_cue[:30]}]", node="GENERATOR")

        # 1. OPTION: LOCAL LTX (DISABLED - CAUSING 28GB HANGS)
        # colony_log("GEN_BURST: Local LTX Bypass active to prevent system stall.", node="GENERATOR")

        # 2. PRIMARY: POLLINATIONS (Fast / Free)
        # We convert the generated image to a dynamic video clip to meet the "VIDEO" requirement.
        try:
            from social_harvest_node import SocialHarvestNode
            harvester = SocialHarvestNode()
            img_path = await harvester.generate_matching_image(visual_cue, 0)
            if img_path:
                colony_log("GEN_BURST: Converting Alpha image to dynamic video clip...", node="GENERATOR")
                video_path = await harvester.convert_image_to_dynamic_video(img_path)
                if video_path: return video_path
        except Exception as e:
            colony_log(f"[-] Pollinations to Video failed: {e}", node="GENERATOR")

        return None

generator = GenerativeBurstNode()
