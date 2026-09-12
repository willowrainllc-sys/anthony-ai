# --- EMPIRE CORE VIDEO ASSEMBLER & TIMELINE EDITOR v16.0 (STRUCTURED PRODUCTION TIMELINE) ---
import os
import sys
import asyncio
import json
import uuid
import random
import subprocess
from pathlib import Path
import httpx
import edge_tts
from PIL import Image, ImageDraw, ImageFont

# MoviePy 2.x Imports
from moviepy import (
    VideoFileClip,
    AudioFileClip,
    ImageClip,
    CompositeVideoClip,
    CompositeAudioClip,
    concatenate_videoclips,
    vfx
)

from colony_logger import colony_log
from colony_persistence import db
from openmontage_engine import openmontage
from quality_control import qc_node

import imageio_ffmpeg
FFMPEG_EXE = imageio_ffmpeg.get_ffmpeg_exe() or "ffmpeg"

RENDER_DIR = Path(r"D:\ObsidianAi_Colony\Renderings")
TEMP_DIR = Path(r"D:\ObsidianAi_Colony\Temp")
BRAND_MUSIC_DIR = Path(r"D:\ObsidianAi_Colony\Secure_Assets\brand_music")
RENDER_DIR.mkdir(parents=True, exist_ok=True)
TEMP_DIR.mkdir(parents=True, exist_ok=True)
BRAND_MUSIC_DIR.mkdir(parents=True, exist_ok=True)

DOCUMENTARY_VOICES = {
    "deep_male": "en-US-ChristopherNeural",
    "authoritative_male": "en-US-GuyNeural",
    "expressive_female": "en-US-AvaNeural",
    "british_narrator": "en-GB-RyanNeural"
}

CONTENT_ARCHETYPES = {
    "mystery": {
        "tags": ["#StorytellerV2", "#Mystery", "#WillowRainCompany", "#Documentary", "#DidYouKnow"],
        "voice": "en-US-ChristopherNeural"
    },
    "inspirational": {
        "tags": ["#Inspiration", "#Mindset", "#Wisdom", "#Quotes", "#WillowRainCompany"],
        "voice": "en-US-ChristopherNeural"
    }
}

EMOJIS = ["", "", "", "", "", "", "[BURST]", "", ""]

def create_brand_watermark_png(width: int = 1080, height: int = 1920) -> str:
    """Renders Willow Rain Company top-corner watermark logo PNG."""
    img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    try:
        font_brand = ImageFont.truetype("arial.ttf", 28)
    except:
        font_brand = ImageFont.load_default()

    brand_text = "WILLOW RAIN COMPANY "
    draw.rounded_rectangle([30, 40, 420, 95], radius=12, fill=(12, 16, 24, 180), outline=(0, 255, 136, 180), width=2)
    draw.text((50, 52), brand_text, font=font_brand, fill=(0, 255, 136, 240))

    out_png = str(TEMP_DIR / f"watermark_obsidian.png")
    img.save(out_png)
    return out_png

def create_floating_text_png(text_phrase: str, width: int = 1080, height: int = 1920) -> str:
    """Renders glowing white letters with heavy multi-directional drop shadows."""
    img = Image.new("RGBA", (width, 320), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    emoji = random.choice(EMOJIS)
    styled_text = f"{text_phrase} {emoji}"

    words = styled_text.split()
    lines = []
    curr = []
    for w in words:
        curr.append(w)
        if len(" ".join(curr)) > 22:
            lines.append(" ".join(curr[:-1]))
            curr = [w]
    if curr: lines.append(" ".join(curr))

    text_content = "\n".join(lines)

    try:
        font = ImageFont.truetype("arial.ttf", 42)
    except:
        font = ImageFont.load_default()

    center_x = width // 2
    center_y = 160

    shadow_color = (0, 0, 0, 255)
    for dx in [-4, -3, -2, -1, 0, 1, 2, 3, 4]:
        for dy in [-4, -3, -2, -1, 0, 1, 2, 3, 4]:
            if dx != 0 or dy != 0:
                draw.multiline_text((center_x + dx, center_y + dy), text_content, font=font, fill=shadow_color, anchor="mm", align="center")

    draw.multiline_text((center_x, center_y), text_content, font=font, fill=(255, 255, 255, 255), anchor="mm", align="center")

    out_png = str(TEMP_DIR / f"quote_letters_{uuid.uuid4().hex[:6]}.png")
    img.save(out_png)
    return out_png

async def generate_neural_narration(text: str, voice_type: str = "deep_male") -> str:
    """Generates a high-fidelity neural voiceover file using edge-tts (100% Free)."""
    voice = DOCUMENTARY_VOICES.get(voice_type, voice_type if "Neural" in voice_type else "en-US-ChristopherNeural")
    out_file = str(TEMP_DIR / f"vo_{uuid.uuid4().hex[:6]}.mp3")

    clean_text = text.replace("Season 1 Episode", "").replace("Key evidence:", "").strip()
    colony_log(f"PIPELINE: Synthesizing Pure Story Voiceover ({voice})...", node="PIPELINE")

    communicate = edge_tts.Communicate(clean_text, voice)
    await communicate.save(out_file)
    if os.path.exists(out_file) and os.path.getsize(out_file) > 1000:
        return out_file
    return None

async def build_storyline_video(
    title: str = None,
    production_timeline = None,
    script_narration: str = None,
    scene_prompts: list = None,
    output_filename: str = None,
    duration_tier: str = "short",
    category: str = "mystery",
    text_only: bool = False
) -> dict:
    """
    TIMELINE EDITOR PIPELINE v16.0:
    Accepts structured ProductionTimeline objects preserving exact shot-narration-asset mappings.
    """
    if not output_filename:
        output_filename = f"doc_{category}_{duration_tier}_{uuid.uuid4().hex[:6]}.mp4"

    archetype = CONTENT_ARCHETYPES.get(category, CONTENT_ARCHETYPES["mystery"])
    output_path = RENDER_DIR / output_filename
    colony_log(f"PIPELINE: Building Production Timeline Video -> {output_filename}", node="PIPELINE")

    # Extract narration and asset paths from structured production_timeline
    if production_timeline:
        title = production_timeline.title
        script_narration = " ".join(list(dict.fromkeys([s.narration_text for s in production_timeline.shots])))
        asset_filepaths = [s.selected_asset_path for s in production_timeline.shots if os.path.exists(s.selected_asset_path)]
    else:
        asset_filepaths = [p for p in (scene_prompts or []) if os.path.exists(p)]

    if not script_narration or not asset_filepaths:
        colony_log("[-] PIPELINE FAIL: Missing script narration or valid asset filepaths.", node="PIPELINE")
        return None

    vo_path = None
    voiceover = None

    if not text_only:
        vo_path = await generate_neural_narration(script_narration, voice_type=archetype["voice"])
        if vo_path:
            voiceover = AudioFileClip(vo_path)
            total_duration = voiceover.duration + 0.1 # Exact millisecond audio-video sync!
        else:
            total_duration = 60.0
    else:
        total_duration = 60.0

    resolution = (1080, 1920) if duration_tier == "short" else (1920, 1080)

    # COMPILE STRUCTURED PRODUCTION TIMELINE
    def _sync_render():
        try:
            processed_clips = openmontage.create_montage_sequence(
                asset_filepaths,
                target_duration=total_duration,
                clip_cut_sec=3.5,
                target_resolution=resolution
            )

            if not processed_clips:
                return False

            concat_video = concatenate_videoclips(processed_clips, method="compose")
            if concat_video.duration < total_duration:
                loops_needed = int(total_duration / concat_video.duration) + 1
                concat_video = concatenate_videoclips([concat_video] * loops_needed, method="compose")

            base_video = concat_video.subclipped(0, total_duration)

            # TOP-CORNER WATERMARK
            overlay_layers = [base_video]
            watermark_png = create_brand_watermark_png(width=resolution[0], height=resolution[1])
            if os.path.exists(watermark_png):
                wm_clip = ImageClip(watermark_png).with_duration(total_duration)
                wm_clip = wm_clip.with_position((0, 0))
                overlay_layers.append(wm_clip)

            # FLOATING KINETIC CAPTIONS
            if text_only:
                words = script_narration.split()
                phrases = []
                chunk_size = 6
                for k in range(0, len(words), chunk_size):
                    phrases.append(" ".join(words[k:k+chunk_size]))

                phrase_duration = total_duration / max(len(phrases), 1)

                for idx, phrase in enumerate(phrases):
                    png_path = create_floating_text_png(phrase, width=resolution[0], height=resolution[1])
                    if os.path.exists(png_path):
                        txt_clip = ImageClip(png_path).with_duration(phrase_duration).with_start(idx * phrase_duration)
                        txt_clip = txt_clip.with_position("center")
                        overlay_layers.append(txt_clip)

            # ENSURE EVEN DIMENSIONS FOR LIBX264 (AND FORCE RESOLUTION FOR COMPOSITE)
            final_video = CompositeVideoClip(overlay_layers, size=resolution)

            # AUDIO COMPOSITION
            audio_layers = []
            if final_video.audio:
                try:
                    native_audio = final_video.audio
                    if hasattr(native_audio, 'with_volume_scaled'):
                        native_audio = native_audio.with_volume_scaled(0.6)
                    else:
                        native_audio = native_audio.volumex(0.6)
                    audio_layers.append(native_audio)
                except: pass

            if voiceover:
                if hasattr(voiceover, 'with_volume_scaled'):
                    vo_audio = voiceover.with_volume_scaled(1.8)
                else:
                    vo_audio = voiceover.volumex(1.8)
                audio_layers.append(vo_audio)

            # Smooth Real Instrumental Music
            music_files = list(BRAND_MUSIC_DIR.glob("*.mp3")) + list(BRAND_MUSIC_DIR.glob("*.wav"))
            if music_files:
                try:
                    music_path = str(random.choice(music_files))
                    bg_music = AudioFileClip(music_path)
                    vol = 0.35 if text_only else 0.12
                    if hasattr(bg_music, 'with_volume_scaled'):
                        bg_music = bg_music.with_volume_scaled(vol)
                    else:
                        bg_music = bg_music.volumex(vol)

                    if hasattr(vfx, 'Loop'):
                        bg_music = bg_music.with_effects([vfx.Loop(duration=total_duration)])
                    elif hasattr(vfx, 'loop'):
                        bg_music = vfx.loop(bg_music, duration=total_duration)

                    audio_layers.append(bg_music)
                except: pass

            if audio_layers:
                final_audio = CompositeAudioClip(audio_layers)
                final_video = final_video.with_audio(final_audio)

            # ENSURE EVEN DIMENSIONS FOR LIBX264
            w, h = final_video.size
            if w % 2 != 0 or h % 2 != 0:
                colony_log(f"PIPELINE: Normalizing odd dimensions ({w}x{h}) to even for FFMPEG...", node="PIPELINE")
                final_video = final_video.resized(width=w + (w % 2), height=h + (h % 2))

            # RENDER FINAL VIDEO WITH YUV420P PIXEL FORMAT
            final_video.write_videofile(
                str(output_path),
                fps=24,
                codec="libx264",
                audio_codec="aac",
                ffmpeg_params=["-pix_fmt", "yuv420p"],
                logger=None,
                threads=4,
                preset="ultrafast"
            )

            final_video.close()
            for vc in processed_clips: vc.close()
            if voiceover: voiceover.close()
            return True
        except Exception as e:
            import traceback
            colony_log(f"[-] RENDER CRASH: {e}\n{traceback.format_exc()}", node="PIPELINE")
            return False

    success = await asyncio.to_thread(_sync_render)

    if vo_path and os.path.exists(vo_path):
        try: os.remove(vo_path)
        except: pass

    if success and output_path.exists():
        colony_log(f" PIPELINE SUCCESS: Rendered {output_filename} ({output_path.stat().st_size} bytes)", node="PIPELINE")
        return {
            "output_path": str(output_path),
            "output_filename": output_filename,
            "metadata": {"title": title, "tags": archetype["tags"]}
        }

    return None

if __name__ == "__main__":
    print("Timeline Editor Pipeline v16.0 Initialized.")
