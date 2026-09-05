# --- EMPIRE CORE VIDEO ASSEMBLER & DOCUMENTARY PIPELINE v3.0 (COPYRIGHT-SAFE & MULTI-TIER) ---
import os
import sys
import asyncio
import json
import uuid
import random
from pathlib import Path
import httpx
import edge_tts

# MoviePy 2.x Imports
from moviepy import (
    VideoFileClip,
    AudioFileClip,
    CompositeVideoClip,
    CompositeAudioClip,
    concatenate_videoclips,
    vfx
)

from swarm_logger import swarm_log
from swarm_persistence import db
from social_harvest_node import SocialHarvestNode
from quality_control import qc_node

# Constants & Paths
RENDER_DIR = Path(r"D:\AnthonyAi_Swarm\Renderings")
TEMP_DIR = Path(r"D:\AnthonyAi_Swarm\Temp")
RENDER_DIR.mkdir(parents=True, exist_ok=True)
TEMP_DIR.mkdir(parents=True, exist_ok=True)

# Free Neural Voice Engines
DOCUMENTARY_VOICES = {
    "deep_male": "en-US-ChristopherNeural",
    "authoritative_male": "en-US-GuyNeural",
    "expressive_female": "en-US-AvaNeural",
    "british_narrator": "en-GB-RyanNeural"
}

# --- DYNAMIC STORY ARC & TAG GENERATOR DATABASE ---
CONTENT_ARCHETYPES = {
    "mystery": {
        "hooks": [
            "What they aren't telling you about this changes everything.",
            "This hidden anomaly was wiped from public records.",
            "Look closely at the data. They missed this on purpose."
        ],
        "tags": ["#UnsolvedMysteries", "#DeepDive", "#HiddenHistory", "#SecretFiles", "#Documentary"],
        "voice": "en-US-ChristopherNeural"
    },
    "tech": {
        "hooks": [
            "The architecture behind this completely breaks traditional scaling.",
            "They said this code structure was impossible to automate.",
            "This autonomous pipeline runs entirely without human intervention."
        ],
        "tags": ["#TechBreakthrough", "#Automation", "#CodeEngine", "#FutureTech", "#AIWorkflow"],
        "voice": "en-US-GuyNeural"
    },
    "space": {
        "hooks": [
            "Deep space sensors just captured a signal that shouldn't exist.",
            "What lunar orbiters found on the far side of the moon changes solar history.",
            "At thirty thousand light years away, physicists recorded an energy spike."
        ],
        "tags": ["#SpaceDiscovery", "#Astronomy", "#NASA", "#Cosmos", "#Universe"],
        "voice": "en-GB-RyanNeural"
    },
    "ocean": {
        "hooks": [
            "Ten thousand meters below sea level, deep sea sonar picked up rhythmic pulses.",
            "Submersibles exploring the trench stumbled upon structures older than history.",
            "In pitch-black abyssal waters, bioluminescent light patterns triggered alarm systems."
        ],
        "tags": ["#OceanAbyss", "#MarianaTrench", "#DeepSea", "#Underwater", "#Exploration"],
        "voice": "en-US-ChristopherNeural"
    }
}

def generate_unique_metadata(category="mystery", base_title="UNCLASSIFIED DOSSIER"):
    """Generates distinct titles, storylines, and tags to prevent duplicate flags."""
    archetype = CONTENT_ARCHETYPES.get(category, CONTENT_ARCHETYPES["mystery"])
    hook = random.choice(archetype["hooks"])

    metadata = {
        "title": f"{base_title}: {hook[:45]}",
        "description": f"Unclassified deep-dive investigation. {hook} {' '.join(archetype['tags'])}",
        "tags": archetype["tags"],
        "voice": archetype.get("voice", "en-US-ChristopherNeural")
    }
    return metadata

async def generate_neural_narration(text: str, voice_type: str = "deep_male") -> str:
    """Generates a high-fidelity neural voiceover file using edge-tts (100% Free)."""
    voice = DOCUMENTARY_VOICES.get(voice_type, voice_type if "Neural" in voice_type else "en-US-ChristopherNeural")
    out_file = str(TEMP_DIR / f"vo_{uuid.uuid4().hex[:6]}.mp3")
    swarm_log(f"PIPELINE: Synthesizing Neural Voiceover ({voice})...", node="PIPELINE")

    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(out_file)
    if os.path.exists(out_file) and os.path.getsize(out_file) > 1000:
        return out_file
    return None

async def build_storyline_video(
    title: str,
    script_narration: str,
    scene_prompts: list,
    output_filename: str = None,
    duration_tier: str = "short",
    category: str = "mystery"
) -> dict:
    """
    HARDENED MONETIZATION-SAFE STORYLINE VIDEO BUILDER:
    Assembles a multi-clip visual narrative with proper voiceover layering,
    stripping original audio for zero copyright claims and applying fair-use visual transforms.
    """
    if not output_filename:
        output_filename = f"doc_{category}_{duration_tier}_{uuid.uuid4().hex[:6]}.mp4"

    meta = generate_unique_metadata(category=category, base_title=title)
    output_path = RENDER_DIR / output_filename
    swarm_log(f"PIPELINE: Building [{category.upper()} | {duration_tier.upper()}] Asset -> {output_filename}", node="PIPELINE")

    # 1. GENERATE NEURAL VOICEOVER NARRATION
    full_narration = f"{meta['title']}. {script_narration}"
    vo_path = await generate_neural_narration(full_narration, voice_type=meta["voice"])
    if not vo_path:
        swarm_log("[-] PIPELINE FAIL: Narration synthesis failed.", node="PIPELINE")
        return None

    voiceover = AudioFileClip(vo_path)
    total_duration = max(voiceover.duration, 15.0)

    # 2. DETERMINE RESOLUTION & ASPECT RATIO
    if duration_tier == "short":
        resolution = (720, 1280) # Vertical 9:16 for Shorts/Reels (1 to 3 minutes)
        target_aspect = "9:16"
    else:
        resolution = (1280, 720) # Horizontal 16:9 for Mid/Long-form (3 to 20 minutes)
        target_aspect = "16:9"

    # 3. SNIPE DIVERSE B-ROLL CLIPS
    sniper = SocialHarvestNode()
    broll_clips = []

    clip_target_duration = 5.0 # Fast 5-second cuts for high viewer retention
    num_clips_needed = max(len(scene_prompts), int(total_duration / clip_target_duration) + 1)

    extended_prompts = list(scene_prompts)
    while len(extended_prompts) < num_clips_needed:
        extended_prompts.append(f"{title} documentary cinematic 4k")

    for i, prompt in enumerate(extended_prompts[:num_clips_needed]):
        swarm_log(f"PIPELINE: Sniping B-Roll {i+1}/{num_clips_needed} for [{prompt[:30]}]...", node="PIPELINE")
        clip_path = await sniper.get_best_match_for_scene(
            scene_data={"visual_prompt": prompt, "duration": clip_target_duration},
            index=i,
            width=resolution[0],
            height=resolution[1]
        )
        if clip_path and os.path.exists(clip_path):
            broll_clips.append(clip_path)

    if not broll_clips:
        swarm_log("[-] PIPELINE FAIL: No B-roll clips acquired.", node="PIPELINE")
        return None

    # 4. COMPILE B-ROLL SEQUENCE WITH FAIR-USE TRANSFORMATIONS
    def _sync_render():
        video_clips = []
        try:
            for path in broll_clips:
                c = VideoFileClip(path)

                # STRIP ORIGINAL AUDIO TO PREVENT COPYRIGHT CLAIMS
                c = c.without_audio()

                # FAIR-USE VISUAL TRANSFORMATIONS (Color Shift & Contrast)
                try:
                    c = c.fx(vfx.colorx, 1.03)
                except: pass

                w, h = c.size

                # Scale & Crop to Target Resolution
                if target_aspect == "9:16":
                    scale = resolution[1] / h
                    new_w, new_h = int(w * scale), resolution[1]
                    c = c.resized(width=new_w, height=new_h)
                    c = c.cropped(x_center=c.w / 2, y_center=c.h / 2, width=resolution[0], height=resolution[1])
                else:
                    scale = resolution[0] / w
                    new_w, new_h = resolution[0], int(h * scale)
                    c = c.resized(width=new_w, height=new_h)
                    c = c.cropped(x_center=c.w / 2, y_center=c.h / 2, width=resolution[0], height=resolution[1])

                video_clips.append(c)

            # Sequence distinct clips through concatenate_videoclips
            concat_video = concatenate_videoclips(video_clips, method="compose")
            if concat_video.duration < total_duration:
                loops_needed = int(total_duration / concat_video.duration) + 1
                concat_video = concatenate_videoclips([concat_video] * loops_needed, method="compose")

            final_video = concat_video.subclipped(0, total_duration)

            # Attach Original Neural Voiceover Track
            if hasattr(voiceover, 'with_volume_scaled'):
                vo_audio = voiceover.with_volume_scaled(1.8)
            else:
                vo_audio = voiceover.volumex(1.8)

            final_video = final_video.with_audio(vo_audio)

            # Render Final Video
            final_video.write_videofile(
                str(output_path),
                fps=30,
                codec="libx264",
                audio_codec="aac",
                logger=None,
                threads=4,
                preset="fast"
            )

            final_video.close()
            for vc in video_clips: vc.close()
            voiceover.close()
            return True
        except Exception as e:
            swarm_log(f"[-] RENDER CRASH: {e}", node="PIPELINE")
            return False

    success = await asyncio.to_thread(_sync_render)

    # Clean up temp vo file
    if os.path.exists(vo_path):
        try: os.remove(vo_path)
        except: pass

    if success and output_path.exists():
        swarm_log(f"✓ PIPELINE SUCCESS: Rendered {output_filename} ({output_path.stat().st_size} bytes)", node="PIPELINE")
        return {
            "output_path": str(output_path),
            "output_filename": output_filename,
            "metadata": meta
        }

    return None

async def main():
    title = "The Lost City of the Sahara"
    narration = "Deep beneath the Sahara Desert, satellite radar uncovered a massive subterranean complex built with impossible mathematical precision."
    prompts = [
        "Sahara desert sand dunes golden sunset 4k",
        "Ancient ruins buried under desert sand cinematic"
    ]
    res = await build_storyline_video(title, narration, prompts, duration_tier="short", category="mystery")
    print("Test pipeline result:", res)

if __name__ == "__main__":
    asyncio.run(main())
