# --- EMPIRE THEME ENGINE: MASTER CREATIVE BIBLE GENERATOR v4.1 ---
import random
import json
import asyncio
from swarm_logger import swarm_log
from swarm_brain import brain_gate

class ThemeEngine:
    """
    BUSINESS NODE: Showrunner & Visual DNA Architect.
    Uses SERIALIZED BRAIN GATE to ensure stability.
    """
    def __init__(self):
        self.genres = ["bad-ass_fantasy", "immersive_documentary"]
        self.visual_styles = ["1080p_studio_54_aesthetic", "cinematic_realism_high_fidelity"]

    async def generate_creative_bible(self, concept_title: str):
        """Builds a complete 'Production Bible'."""
        genre = random.choice(self.genres)
        style = random.choice(self.visual_styles)

        prompt = f"""
        Act as a Hollywood Showrunner for project: "{concept_title}".
        Generate a 'Creative Bible' (JSON).

        Genre: {genre}
        Visual Style: {style}
        Constraints: Natural skin tones, Studio 54 lighting, zero archival footage, NO AI/tech buzzwords.

        Define:
        1. location: settings description.
        2. characters: physical protagonist detail (natural skin tones).
        3. palette: Studio 54 neon-noir meets high-fidelity realism.
        4. lighting: cinematic logic, high contrast.
        5. camera_dna: 1080p high-fidelity lens/motion.
        """

        swarm_log(f"THEME_ENGINE: Architecting DNA for {concept_title}...", node="BRAIN")

        raw_resp = await brain_gate.generate_serialized(prompt)
        if raw_resp:
            try:
                bible = json.loads(raw_resp)
                bible['visual_style'] = style
                return bible
            except: pass

        # Robust Fallback
        return {
            "metadata": {"genre": genre, "style": style},
            "visual_style": style,
            "world": {"location": "undisclosed", "lighting": "natural cinematic"},
            "visual_identity": {"palette": "natural", "texture": "sharp 1080p"},
            "characters": {"main": {"description": "explorer"}},
            "rules": ["Neutral whites", "BT.709 guard"]
        }

theme_engine = ThemeEngine()
