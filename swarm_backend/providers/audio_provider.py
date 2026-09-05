# --- EMPIRE AUDIO PROVIDER: CINEMATIC VOICE & MUSIC v1.0 ---
import os
import asyncio
import uuid
import random
from pathlib import Path
from .base_provider import AudioProvider
from swarm_logger import swarm_log

import imageio_ffmpeg
FFMPEG_EXE = imageio_ffmpeg.get_ffmpeg_exe() or "ffmpeg"

class EdgeTTSProvider(AudioProvider):
    """
    Adapter for Microsoft Edge TTS and Local Music Assets.
    """
    def __init__(self):
        self.output_dir = Path(r"D:\AnthonyAi_Swarm\Renderings")
        self.output_dir.mkdir(exist_ok=True, parents=True)
        self.music_dir = Path(r"D:\AnthonyAi_Swarm\Secure_Assets\brand_music")

    async def generate_speech(self, text: str, voice: str) -> str:
        job_id = uuid.uuid4().hex[:8]
        path = self.output_dir / f"speech_{job_id}.mp3"

        try:
            import edge_tts
            comm = edge_tts.Communicate(text, voice)
            await comm.save(str(path))
            return str(path)
        except Exception as e:
            swarm_log(f"[-] AUDIO ERROR (TTS): {e}", node="AUDIO_PROVIDER")
            # Fallback to silent MP3 via FFmpeg
            cmd = [FFMPEG_EXE, "-y", "-f", "lavfi", "-i", "anullsrc=r=44100:cl=stereo", "-t", "5", "-c:a", "libmp3lame", str(path)]
            await (await asyncio.create_subprocess_exec(*cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)).communicate()
            return str(path)

    async def generate_music(self, mood: str, duration: int) -> str:
        """Pulls matched cinematic music from the local library."""
        music_files = list(self.music_dir.glob("*.mp3")) + list(self.music_dir.glob("*.wav"))
        if not music_files: return ""

        # In v1.0 we pick a random brand track. v1.1 will use mood-tag matching.
        return str(random.choice(music_files))

audio_provider = EdgeTTSProvider()
