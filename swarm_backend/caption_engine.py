# --- EMPIRE CAPTION ENGINE: RETENTION ARCHITECT v1.1 ---
import asyncio
import os
import json
import re
from pathlib import Path
from swarm_logger import swarm_log
from providers.transcription_provider import transcription_provider

class CaptionEngine:
    """
    BUSINESS NODE: Accessibility & Retention.
    Transcribes audio and generates mobile-optimized, strategically emphasized captions.
    """
    async def generate_mobile_captions(self, audio_path: str):
        swarm_log("CAPTIONS: Transcribing narrative for mobile optimization...", node="CAPTIONS")

        # 1. TRANSCRIBE via Provider
        segments = await transcription_provider.transcribe_audio(audio_path)

        # 2. STRATEGIC EMPHASIS
        emphasized = self._apply_emphasis(segments)

        return emphasized

    def _apply_emphasis(self, segments: list):
        """Adds 'emphasis' flag to high-impact keywords."""
        keywords = ["SECRET", "VANISHING", "SUPREME", "DANGER", "UNKNOWN", "POWER", "AWAKENS", "EXISTENCE"]
        for seg in segments:
            if any(k in seg['text'].upper() for k in keywords):
                seg['emphasis'] = True
        return segments

    def generate_ass_file(self, segments: list, output_path: str):
        """Generates an Advanced Substation Alpha file for mobile-optimized rendering."""
        header = """[Script Info]
ScriptType: v4.00+
PlayResX: 720
PlayResY: 1280

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,Impact,80,&H00FFFFFF,&H000000FF,&H00000000,&H00000000,1,0,0,0,100,100,0,0,1,3,0,2,20,20,100,1
Style: Emphasis,Impact,95,&H0000FFFF,&H000000FF,&H00000000,&H00000000,1,0,0,0,100,100,0,0,1,4,2,2,20,20,100,1
"""
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(header)
            f.write("\n[Events]\nFormat: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n")
            for seg in segments:
                style = "Emphasis" if seg.get('emphasis') else "Default"
                start = self._fmt_time(seg['start'])
                end = self._fmt_time(seg['end'])
                f.write(f"Dialogue: 0,{start},{end},{style},,0,0,0,,{seg['text']}\n")
        return output_path

    def _fmt_time(self, seconds: float):
        td = float(seconds)
        h = int(td // 3600)
        m = int((td % 3600) // 60)
        s = int(td % 60)
        ms = int((td % 1) * 100)
        return f"{h:01}:{m:02}:{s:02}.{ms:02}"

caption_engine = CaptionEngine()
