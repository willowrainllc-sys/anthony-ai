# --- EMPIRE FAL.AI PROVIDER (REMOVED FROM BUILD) ---
from .base_provider import VideoProvider

class FalWanVideoProvider(VideoProvider):
    """REMOVED: fal.ai is completely disabled in build."""
    async def generate_video(self, prompt: str, duration: int, bible: dict = None) -> str:
        return None

fal_wan_provider = FalWanVideoProvider()
