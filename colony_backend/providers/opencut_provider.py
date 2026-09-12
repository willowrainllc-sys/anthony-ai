# --- EMPIRE OPENCUT EDITOR: CINEMATIC ASSEMBLY WORKER v1.8 (FINAL COMPAT) ---
import os
import asyncio
from typing import Dict, Any, List
from pathlib import Path
from .base_provider import VideoEditorProvider
from colony_logger import colony_log

# MoviePy v2.x Robust Import Matrix
try:
    # Try MoviePy 2.x primary paths
    from moviepy import VideoFileClip, AudioFileClip, CompositeVideoClip, concatenate_videoclips, CompositeAudioClip
    try:
        from moviepy import vfx
    except ImportError:
        import moviepy.video.fx as vfx
    MOVIEPY_AVAILABLE = True
except Exception:
    try:
        # Fallback to MoviePy 1.x / .editor
        from moviepy.editor import VideoFileClip, AudioFileClip, CompositeVideoClip, concatenate_videoclips, CompositeAudioClip, vfx
        MOVIEPY_AVAILABLE = True
    except Exception as e2:
        colony_log(f"[-] MOVIEPY IMPORT FAIL: {e2}", node="OPENCUT")
        MOVIEPY_AVAILABLE = False

class OpenCutEditor(VideoEditorProvider):
    """
    BUSINESS NODE: Adaptive Cinematic Editor.
    v1.8: Hardened for MoviePy 2.1.2.
    Corrected 'cropped' params to x_center/y_center and used subclipped/subclip safely.
    """
    def __init__(self):
        self.render_dir = Path(r"D:\ObsidianAi_Swarm\Renderings")

    async def assemble_video(self, manifest: Dict[str, Any], output_path: str) -> bool:
        if not MOVIEPY_AVAILABLE:
            colony_log("[-] OPENCUT: Core engine missing. Aborting.", node="OPENCUT")
            return False

        try:
            return await asyncio.to_thread(self._sync_assemble, manifest, output_path)
        except Exception as e:
            colony_log(f"[-] OPENCUT FATAL: {e}", node="OPENCUT")
            return False

    def _sync_assemble(self, manifest: Dict[str, Any], output_path: str):
        format_type = manifest.get('bible', {}).get('aspect_ratio', '9:16')

        clips = []
        audio_tracks = []

        for scene in manifest.get('scenes', []):
            path = scene.get('path')
            if not path or not os.path.exists(path):
                continue

            try:
                duration = float(scene.get('duration', 15))
                clip = VideoFileClip(path)

                # 1. TIME TRIM
                if clip.duration > duration:
                    if hasattr(clip, 'subclipped'):
                        clip = clip.subclipped(0, duration)
                    else:
                        clip = clip.subclip(0, duration)

                # 2. VISUAL ADAPTATION
                w, h = clip.size
                if format_type == '9:16':
                    scale = 1280 / h
                    new_w, new_h = int(w * scale), 1280
                    # Ensure width is even for x264
                    if new_w % 2 != 0: new_w += 1

                    if hasattr(clip, 'resized'):
                        clip = clip.resized(width=new_w, height=new_h)
                        clip = clip.cropped(x_center=clip.w/2, y_center=clip.h/2, width=720, height=1280)
                    else:
                        from moviepy.video.fx.all import resize, crop
                        clip = clip.fx(resize, height=1280)
                        clip = clip.fx(crop, x_center=clip.w/2, width=720)
                else:
                    scale = 1280 / w
                    new_w, new_h = 1280, int(h * scale)
                    # Ensure height is even
                    if new_h % 2 != 0: new_h += 1

                    if hasattr(clip, 'resized'):
                        clip = clip.resized(width=new_w, height=new_h)
                        clip = clip.cropped(x_center=clip.w/2, y_center=clip.h/2, width=1280, height=720)
                    else:
                        from moviepy.video.fx.all import resize, crop
                        clip = clip.fx(resize, width=1280)
                        clip = clip.fx(crop, y_center=clip.h/2, height=720)

                clips.append(clip)
                if clip.audio:
                    audio_tracks.append(clip.audio)

            except Exception as e:
                colony_log(f"[-] OPENCUT: Scene Fail [{path}]: {e}", node="OPENCUT")

        if not clips: return False

        try:
            # 3. ASSEMBLY WITH TRANSITIONS
            # Using 1-second cross-fade between clips
            final_video = concatenate_videoclips(clips, method="compose", padding=-1)

            # 4. AUDIO OVERLAY & DUCKING
            vocal_path = manifest.get('vocal_path')
            if vocal_path and os.path.exists(vocal_path):
                vocal = AudioFileClip(vocal_path)
                # Ensure vocal fits video duration
                if vocal.duration > final_video.duration:
                    vocal = vocal.subclip(0, final_video.duration)

                # Boost vocal for clarity
                if hasattr(vocal, 'with_volume_scaled'):
                    vocal = vocal.with_volume_scaled(1.8)
                else:
                    vocal = vocal.volumex(1.8)
                audio_tracks.append(vocal)

                music_path = manifest.get('music_path')
                if music_path and os.path.exists(music_path):
                    music = AudioFileClip(music_path)

                    # DUCKING: Lower music volume when vocal is active
                    if hasattr(music, 'with_volume_scaled'):
                        music = music.with_volume_scaled(0.15)
                    else:
                        music = music.volumex(0.15)

                    if hasattr(vfx, 'Loop'):
                        music = music.with_effects([vfx.Loop(duration=final_video.duration)])
                    elif hasattr(vfx, 'loop'):
                        music = vfx.loop(music, duration=final_video.duration)
                    audio_tracks.append(music)

            if audio_tracks:
                final_audio = CompositeAudioClip(audio_tracks)
                if hasattr(final_video, 'with_audio'):
                    final_video = final_video.with_audio(final_audio)
                else:
                    final_video = final_video.set_audio(final_audio)

            # 5. RENDER
            final_video.write_videofile(
                output_path,
                fps=30,
                codec="libx264",
                audio_codec="aac",
                logger=None,
                threads=4,
                preset="ultrafast"
            )

            final_video.close()
            for c in clips: c.close()
            return True
        except Exception as e:
            colony_log(f"[-] OPENCUT: Final assembly crash: {e}", node="OPENCUT")
            return False

import uuid
opencut_editor = OpenCutEditor()
