# --- OBSIDIAN GLOBAL: GHOST VISION (LIVE FEED) v1.0 ---
import asyncio
import os
from pathlib import Path
from colony_logger import colony_log
from colony_persistence import db

class ObsidianGhostVision:
    """
    GHOST VISION ENGINE:
    Streams the physical work of the commerce bots to the Director.
    1. SCREEN CAPTURE: Grabs real-time visual proof of browser actions.
    2. STREAM SYNC: Pushes images to the Saturn Cloud dashboard.
    3. AI CORRECTION: Allows 'Anthony' to see what the bot sees and fix UI blocks.
    """
    def __init__(self):
        self.output_dir = Path(r"D:\AnthonyAi_Colony\Secure_Assets\Ghost_Vision")
        self.output_dir.mkdir(parents=True, exist_ok=True)

    async def broadcast_action(self, page, bot_name):
        """Captures the current bot frame and saves it for the Live View."""
        filename = f"{bot_name}_live.png"
        path = self.output_dir / filename

        try:
            await page.screenshot(path=str(path), full_page=False)
            # Update the OIS with the visual evidence
            db.log_event("MEDIA", "GHOST_VISION_PULSE", {"bot": bot_name, "image_path": str(path)})
        except:
            pass

ghost_vision = ObsidianGhostVision()
