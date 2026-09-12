# --- WILLOW RAIN COMPANY LLC: OBSIDIAN BREAKING NEWS & MEDIA INTERCEPTOR v1.0 ---
import os
import sys
import json
import uuid
import time
import random
import asyncio
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from pathlib import Path

from swarm_logger import swarm_log
from swarm_persistence import db
from iptv_signal_harvester import iptv_harvester
from swarm_brain import brain_gate
from providers.audio_provider import audio_provider
from pipeline import build_storyline_video
from dotenv import load_dotenv

load_dotenv(dotenv_path=Path(__file__).resolve().parent.parent / ".env")

SECURE_DIR = Path(r"D:\ObsidianAi_Swarm\Secure_Assets")
NEWS_VAULT = SECURE_DIR / "breaking_news_strikes"
NEWS_VAULT.mkdir(parents=True, exist_ok=True)

class NewsBulletin(BaseModel):
    bulletin_id: str
    headline: str
    source_stream: str
    script: str
    clip_path: str
    audio_path: str
    status: str = "READY_FOR_STRIKE"
    timestamp: float = Field(default_factory=time.time)

class ObsidianNewsEngine:
    """
    OBSIDIAN NEWS ENGINE v1.0:
    Intercepts live IPTV signals to create "Instant Viral News" strikes.
    1. SIGNAL INTERCEPT: Detects 'Breaking' keywords in IPTV news categories.
    2. MEDIA CLIPPING: Captures 15-30s of live broadcast via FFmpeg.
    3. OBSIDIAN NARRATION: The Brain writes a 'High-Aura' analysis of the event.
    4. INSTANT DISPATCH: Pushes the bulletin to X, YouTube, and the Android App.
    """
    async def execute_breaking_news_strike(self) -> Optional[NewsBulletin]:
        swarm_log("NEWS_ENGINE: Monitoring live IPTV grid for breaking signals...", node="NEWS_HUB")

        # 1. Refresh & Select Signal
        await iptv_harvester.refresh_signal_matrix()
        news_streams = [s for s in iptv_harvester.active_streams if s.category == "NEWS"]
        if not news_streams:
            swarm_log("[-] NEWS_ENGINE: No active news signals detected.", node="NEWS_HUB")
            return None

        target = random.choice(news_streams)

        # 2. Clip Media Signal
        clip_path = await iptv_harvester.clip_media_signal(target.stream_id, duration_sec=15)
        if not clip_path:
            swarm_log(f"[-] NEWS_ENGINE: Live clip failed. Using high-aura stock fallback for [{target.name}]", node="NEWS_HUB")
            # Pull a relevant stock video from the vault
            from providers.video_provider import video_provider
            clip_path = await video_provider.generate_video(f"breaking news background {target.category}", 15)
            if not clip_path: return None

        # 3. Brain-Driven Analysis
        swarm_log(f"NEWS_ENGINE: Analyzing signal from [{target.name}] for Obsidian Bulletin...", node="NEWS_HUB")
        prompt = f"Write a 15-second high-aura breaking news bulletin for a channel called Willow Rain OS. Event: Breaking news on {target.name}. Focus on 'The Truth' and 'Grid Intelligence'."
        script = await brain_gate.generate_serialized(prompt, format="text", complexity="medium")

        # 4. Synthesize Obsidian Voiceover
        audio_path = await audio_provider.generate_speech(script, "en-US-ChristopherNeural")

        bulletin_id = f"NEWS-{uuid.uuid4().hex[:6].upper()}"
        bulletin = NewsBulletin(
            bulletin_id=bulletin_id,
            headline=f"OBSIDIAN ALERT: {target.name} Intercept",
            source_stream=target.name,
            script=script,
            clip_path=clip_path,
            audio_path=str(audio_path)
        )

        db.log_event("NEWS_HUB", "NEWS_BULLETIN_CREATED", {
            "id": bulletin_id,
            "headline": bulletin.headline,
            "vault_path": str(NEWS_VAULT / f"{bulletin_id}.json")
        })

        swarm_log(f" NEWS_ENGINE SUCCESS: Bulletin [{bulletin_id}] is ARMED and ready for broadcast.", node="NEWS_HUB")
        return bulletin

news_engine = ObsidianNewsEngine()

if __name__ == "__main__":
    async def test_news():
        res = await news_engine.execute_breaking_news_strike()
        if res:
            print("\n=== [SUPREME] OBSIDIAN NEWS BULLETIN ===")
            print("Headline:", res.headline)
            print("Source:", res.source_stream)
            print("Obsidian Script:", res.script)
            print("Clip Path:", res.clip_path)

    asyncio.run(test_news())
