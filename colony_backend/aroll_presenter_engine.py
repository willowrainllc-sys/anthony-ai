# --- EMPIRE A-ROLL CINEMATIC PRESENTER & HOST ENGINE v1.0 ---
import os
import sys
import asyncio
import json
import uuid
import random
import httpx
from pathlib import Path
from colony_logger import colony_log
from dotenv import load_dotenv

load_dotenv(dotenv_path=Path(__file__).resolve().parent.parent / ".env")

SECURE_DIR = Path(r"D:\ObsidianAi_Colony\Secure_Assets")
AROLL_DIR = SECURE_DIR / "aroll_presenters"
AROLL_DIR.mkdir(parents=True, exist_ok=True)

class ArollPresenterEngine:
    """
    A-ROLL PRESENTER & HOST ENGINE:
    Snipes and generates A-Roll primary presenter footage (talking host, lead investigator speaking directly to camera, news anchor, studio host)
    to anchor the main storyline before cutting to supporting B-roll.
    """
    def __init__(self):
        self.pexels_key = os.getenv("PEXELS_API_KEY")

    async def get_aroll_presenter_clip(self, category: str = "documentary", width: int = 720, height: int = 1280) -> str:
        colony_log(f"A-ROLL: Sniping primary A-Roll presenter host for [{category.upper()}]...", node="AROLL")

        aroll_queries = [
            "documentary host speaking to camera 4k",
            "news anchor reporter presenting story 4k",
            "podcast host speaking into microphone studio 4k",
            "investigator talking to camera studio 4k",
            "scientist presenter speaking cinematic 4k"
        ]

        chosen_query = random.choice(aroll_queries)
        if self.pexels_key:
            try:
                orientation = "portrait" if height > width else "landscape"
                url = f"https://api.pexels.com/videos/search?query={chosen_query}&per_page=10&orientation={orientation}"

                async with httpx.AsyncClient(timeout=15.0) as client:
                    resp = await client.get(url, headers={"Authorization": self.pexels_key})
                    if resp.status_code == 200:
                        videos = resp.json().get("videos", [])
                        if videos:
                            v_data = random.choice(videos)
                            files = v_data.get("video_files", [])
                            best_file = next((f['link'] for f in files if f.get('width') and f.get('width') >= 720), files[0]['link'] if files else None)

                            if best_file:
                                out_path = AROLL_DIR / f"aroll_host_{uuid.uuid4().hex[:6]}.mp4"
                                async with client.stream("GET", best_file, follow_redirects=True) as v_stream:
                                    with open(out_path, "wb") as f:
                                        async for chunk in v_stream.aiter_bytes():
                                            f.write(chunk)

                                if out_path.exists() and out_path.stat().st_size > 300000:
                                    colony_log(f" A-ROLL SUCCESS: Sniped primary presenter: {out_path.name}", node="AROLL")
                                    return str(out_path)
            except Exception as e:
                colony_log(f"[-] A-Roll Snipe Note: {e}", node="AROLL")

        return None

aroll_engine = ArollPresenterEngine()

if __name__ == "__main__":
    res = asyncio.run(aroll_engine.get_aroll_presenter_clip())
    print("A-Roll Presenter Result:", res)
