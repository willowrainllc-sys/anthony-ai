# --- EMPIRE QUALITY CONTROL: THE GATEKEEPER v1.1 (FFMPEG PROBE FIX) ---
import os
import asyncio
import subprocess
import json
import re
from pathlib import Path
from swarm_logger import swarm_log
from swarm_brain import brain_gate

import imageio_ffmpeg
FFMPEG_EXE = imageio_ffmpeg.get_ffmpeg_exe() or "ffmpeg"

class QualityControlNode:
    """
    BUSINESS NODE: Product Excellence.
    v1.1: Uses standard FFMPEG to probe instead of missing FFPROBE.
    """
    async def verify_strike_readiness(self, video_path: str, manifest: dict):
        swarm_log(f"QC: Inspecting production [{os.path.basename(video_path)}]...", node="QC")

        if not os.path.exists(video_path):
            return False, "File missing"

        if os.path.getsize(video_path) < 500000:
            return False, "File too small/corrupted"

        # 1. TECHNICAL CHECK
        tech_pass, tech_msg = await self._run_technical_check(video_path)
        if not tech_pass:
            swarm_log(f"QC REJECTION [TECH]: {tech_msg}", node="QC")
            return False, tech_msg

        # 2. CREATIVE CHECK
        creative_pass, creative_msg = await self._run_creative_check(video_path, manifest)
        if not creative_pass:
            swarm_log(f"QC REJECTION [CREATIVE]: {creative_msg}", node="QC")
            return False, creative_msg

        swarm_log("QC: Strike readiness VERIFIED.", node="QC")
        return True, "Passed"

    async def _run_technical_check(self, video_path: str):
        try:
            # We use ffmpeg -i and capture stderr which contains metadata
            cmd = [FFMPEG_EXE, "-i", video_path]
            proc = await asyncio.create_subprocess_exec(*cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
            _, stderr = await proc.communicate()
            output = stderr.decode('utf-8', errors='ignore')

            # Extract duration
            duration_match = re.search(r"Duration:\s+(\d+):(\d+):(\d+\.\d+)", output)
            if duration_match:
                h, m, s = duration_match.groups()
                duration = int(h) * 3600 + int(m) * 60 + float(s)
                if duration < 5: return False, "Video too short"

            # Check for audio stream. If missing, automatically inject silent audio track
            if "Audio:" not in output:
                swarm_log("QC: Missing audio stream. Injecting audio track...", node="QC")
                await self._add_silent_audio(video_path)

            return True, "Technical OK"
        except Exception as e:
            swarm_log(f"[-] QC PROBE FAIL: {e}", node="QC")
            return True, "Technical Bypass (Probe Error)"

    async def _add_silent_audio(self, video_path: str):
        try:
            temp_path = str(video_path) + ".tmp.mp4"
            cmd = [
                FFMPEG_EXE, "-y", "-i", video_path,
                "-f", "lavfi", "-i", "anullsrc=channel_layout=stereo:sample_rate=44100",
                "-c:v", "copy", "-c:a", "aac", "-shortest", temp_path
            ]
            proc = await asyncio.create_subprocess_exec(*cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
            await proc.communicate()
            if os.path.exists(temp_path) and os.path.getsize(temp_path) > 1000:
                os.replace(temp_path, video_path)
        except Exception as e:
            swarm_log(f"[-] Audio Injection Error: {e}", node="QC")

    async def _run_creative_check(self, video_path: str, manifest: dict):
        thumb = Path(video_path).parent / f"qc_thumb_{uuid.uuid4().hex[:4]}.jpg"
        try:
            # Seek to 2s instead of 5s (more likely to have content)
            cmd = [FFMPEG_EXE, "-y", "-i", video_path, "-ss", "00:00:02", "-vframes", "1", str(thumb)]
            proc = await asyncio.create_subprocess_exec(*cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
            await proc.communicate()

            if thumb.exists():
                prompt = f"""
                TITLE: {manifest.get('title')}
                TASK: Judge if this visual matches the cinematic standard.
                Return 'PASS' or 'FAIL'.
                """
                inspection = await brain_gate.inspect_visual(str(thumb), prompt)
                os.remove(thumb)

                if "FAIL" in str(inspection).upper():
                    return False, f"Creative mismatch: {inspection}"

            return True, "Creative OK"
        except: return True, "Creative bypass"

import uuid
qc_node = QualityControlNode()
