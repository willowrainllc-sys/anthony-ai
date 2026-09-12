# --- OPENMONTAGE: OPEN-SOURCE PYTHON VIDEO MONTAGE ENGINE v3.0 (PNG & MP4 SUPPORT) ---
import os
import sys
import json
import uuid
import time
import random
import asyncio
from pathlib import Path

# MoviePy 2.x Imports for OpenMontage Sequence Generation
from moviepy import (
    VideoFileClip,
    ImageClip,
    AudioFileClip,
    CompositeVideoClip,
    concatenate_videoclips,
    vfx
)

from swarm_logger import swarm_log
from swarm_persistence import db

SECURE_DIR = Path(r"D:\ObsidianAi_Swarm\Secure_Assets")
TEMP_DIR = Path(r"D:\ObsidianAi_Swarm\Temp")
RENDER_DIR = Path(r"D:\ObsidianAi_Swarm\Renderings")

class OpenMontageEngine:
    """
    OPENMONTAGE ENGINE v3.0:
    Open-source Python video montage framework supporting both PNG image plates and MP4 video clips.
    """
    def create_montage_sequence(
        self,
        clip_paths: list,
        target_duration: float = 60.0,
        clip_cut_sec: float = 3.5,
        target_resolution: tuple = (1080, 1920)
    ) -> list:
        swarm_log(f"OPENMONTAGE: Assembling open-source Python video montage across {len(clip_paths)} source assets...", node="OPENMONTAGE")

        processed_montage_clips = []
        try:
            for i, path in enumerate(clip_paths):
                if not os.path.exists(path): continue

                # Check file extension (PNG image plate vs MP4 video)
                if path.lower().endswith((".png", ".jpg", ".jpeg")):
                    c = ImageClip(path).with_duration(clip_cut_sec)
                else:
                    c = VideoFileClip(path)
                    safe_end = max(0.5, min(clip_cut_sec, c.duration - 0.2))
                    c = c.subclipped(0, safe_end)

                try:
                    c = c.fx(vfx.colorx, 1.05)
                except: pass

                w, h = c.size

                # 1080x1920 9:16 Scale & Crop
                scale = target_resolution[1] / h
                new_w, new_h = int(w * scale), target_resolution[1]
                if new_w < target_resolution[0]:
                    scale = target_resolution[0] / w
                    new_w, new_h = target_resolution[0], int(h * scale)

                c = c.resized(width=new_w, height=new_h)
                c = c.cropped(x_center=c.w / 2, y_center=c.h / 2, width=target_resolution[0], height=target_resolution[1])

                processed_montage_clips.append(c)

            swarm_log(f" OPENMONTAGE SUCCESS: Compiled {len(processed_montage_clips)} smooth montage sequence clips!", node="OPENMONTAGE")
            return processed_montage_clips

        except Exception as e:
            import traceback
            swarm_log(f"[-] OpenMontage Error: {e}\n{traceback.format_exc()}", node="OPENMONTAGE")
            return []

openmontage = OpenMontageEngine()

if __name__ == "__main__":
    print("OpenMontage Engine v3.0 Initialized.")
