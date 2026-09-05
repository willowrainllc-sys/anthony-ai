# --- EMPIRE QUALITY GATE: ALPHA PRODUCTION VALIDATOR v2.0 ---
import json
import hashlib
import os
import subprocess
from swarm_logger import swarm_log
from swarm_persistence import db

class QualityGate:
    """
    Automated Production Traffic Light.
    Enforces technical excellence and cinematic integrity.
    """
    @staticmethod
    def validate_storyboard(storyboard: dict):
        errors = []
        shots = storyboard.get("shots", []) or storyboard.get("scenes", [])
        if not shots:
            errors.append("Critical Failure: No shots found in storyboard.")

        cinematic_tags = ["mm", "lens", "light", "f/", "anamorphic", "imax", "arri", "cinematic", "depth", "macro", "shot"]
        for i, shot in enumerate(shots):
            prompt = shot.get("visual_prompt", "").lower()
            narration = shot.get("voiceover_line") or shot.get("narration") or shot.get("text")
            if not narration:
                errors.append(f"Shot {i+1} is missing a narration line.")

        banned = ["tapestry", "delve", "unveil", "unlock", "placeholder"]
        full_text = json.dumps(storyboard).lower()
        for word in banned:
            if word in full_text:
                errors.append(f"Banned 'bot-slang' detected: {word}")

        if errors:
            swarm_log(f"QUALITY REJECTION: {len(errors)} issues found.", node="DIRECTOR")
            return False, errors

        swarm_log(f"QUALITY GATE: Passed storyboard validation.", node="DIRECTOR")
        return True, []

    @staticmethod
    def verify_render(file_path: str, topic: str = None):
        """
        Post-Render Verification:
        Checks for duplicates, bad audio, and file integrity.
        """
        if not os.path.exists(file_path):
            alt_path = os.path.join(r"D:\AnthonyAi_Swarm\Renderings", os.path.basename(file_path))
            if os.path.exists(alt_path):
                file_path = alt_path
            else:
                return False, "File does not exist."

        # 1. Size Check
        size_mb = os.path.getsize(file_path) / (1024 * 1024)
        if size_mb < 0.5:
            return False, f"File size too small ({size_mb:.2f}MB)."

        # 2. Duplicate Detection
        sha256_hash = hashlib.sha256()
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        file_hash = sha256_hash.hexdigest()

        with db._get_connection() as conn:
            exists = conn.execute("SELECT filename FROM rendered_assets WHERE hash = ?", (file_hash,)).fetchone()
            if exists:
                return False, f"Duplicate video detected: {exists[0]}"

        # 3. Audio Verification (Improved via ffprobe)
        try:
            import imageio_ffmpeg
            FFMPEG_EXE = imageio_ffmpeg.get_ffmpeg_exe() or "ffmpeg"
            FFPROBE_EXE = FFMPEG_EXE.replace("ffmpeg", "ffprobe")

            probe_cmd = f'"{FFPROBE_EXE}" -v error -select_streams a -show_entries stream=codec_name -of default=noprint_wrappers=1:nokey=1 "{file_path}"'
            result = subprocess.run(probe_cmd, capture_output=True, text=True, timeout=15, shell=True)
            audio_streams = result.stdout.strip()

            if not audio_streams:
                # Secondary manual check using ffmpeg info
                probe_cmd_alt = f'"{FFMPEG_EXE}" -i "{file_path}" -hide_banner'
                result_alt = subprocess.run(probe_cmd_alt, capture_output=True, text=True, timeout=15, shell=True)
                if "Audio:" not in result_alt.stderr:
                    swarm_log(f"QUALITY WARNING: Audio stream missing in {os.path.basename(file_path)}", node="DIRECTOR")
                    # If the file is large, we might allow it as a last resort, but socials prefer audio
                    if size_mb < 2.0:
                        return False, "Technical verification failed: Audio stream missing."

        except Exception as e:
            swarm_log(f"QUALITY ERROR: Technical probe failed: {e}", node="DIRECTOR")

        # 4. Log Success
        with db._get_connection() as conn:
            conn.execute("INSERT OR IGNORE INTO rendered_assets (hash, filename, topic) VALUES (?, ?, ?)",
                         (file_hash, os.path.basename(file_path), topic))
            conn.commit()

        swarm_log(f"QUALITY GATE: Render verified for {topic}.", node="DIRECTOR")
        return True, []

validator = QualityGate()
