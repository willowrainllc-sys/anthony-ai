# --- EMPIRE CLAUDE-VIDEO ENGINE: ANTHROPIC CINEMATIC STORYBOARDING v1.0 ---
import os
import json
import asyncio
import httpx
from pathlib import Path
from swarm_logger import swarm_log
from dotenv import load_dotenv

load_dotenv(dotenv_path=Path(__file__).resolve().parent.parent / ".env")

ANTHROPIC_KEY = os.getenv("ANTHROPIC_API_KEY")

class ClaudeVideoEngine:
    """
    CLAUDE-VIDEO ARCHITECTURE:
    Uses Anthropic Claude (claude-3-5-sonnet / claude-3-opus) to generate
    ultra-vivid, high-retention 3-second micro-storyboards, narrative scripts,
    and visual prompts mapped directly to video scene generation.
    """
    def __init__(self):
        self.api_key = ANTHROPIC_KEY
        self.endpoint = "https://api.anthropic.com/v1/messages"
        self.model = "claude-3-5-sonnet-20241022"

    async def generate_claude_storyboard(self, topic: str, duration_tier: str = "short") -> dict:
        swarm_log(f"CLAUDE-VIDEO: Architecting storyboard for [{topic}]...", node="CLAUDE_VIDEO")

        if not self.api_key:
            swarm_log("[-] CLAUDE-VIDEO: ANTHROPIC_API_KEY missing in .env. Falling back to local brain.", node="CLAUDE_VIDEO")
            return None

        prompt = f"""
        You are an ELITE HOLLYWOOD DOCUMENTARY DIRECTOR AND VISUAL SHOWRUNNER.
        MISSION: Create a cinematic, high-retention storyboard for a documentary titled: "{topic}".
        DURATION FORMAT: {duration_tier} (short = 60s vertical 9:16, mid = 3-5m 16:9, long = 15-20m 16:9).

        STRICT REQUIREMENTS:
        1. 0-SECOND HOOK: The first sentence must open a shocking curiosity gap.
        2. MICRO-SCENES: Break the video down into precise 3 to 5-second scenes.
        3. 4K VISUAL PROMPTS: Each scene MUST have a hyper-vivid 4K visual prompt for stock/AI video rendering.
        4. ON-SCREEN TEXT: High-impact 2-4 word captions for kinetic center overlays.

        OUTPUT FORMAT (JSON ONLY):
        {{
            "title": "{topic}",
            "niche": "doc_investigation",
            "full_script": "Complete narrative script text...",
            "storyboard": [
                {{
                    "scene": 1,
                    "duration": 5,
                    "spoken_script": "...",
                    "visual_prompt": "...",
                    "on_screen_text": "..."
                }}
            ],
            "tags": ["#Documentary", "#Shorts", "#Unexplained"]
        }}
        """

        headers = {
            "x-api-key": self.api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json"
        }

        payload = {
            "model": self.model,
            "max_tokens": 2048,
            "messages": [
                {"role": "user", "content": prompt}
            ]
        }

        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                resp = await client.post(self.endpoint, json=payload, headers=headers)
                if resp.status_code == 200:
                    data = resp.json()
                    text = data['content'][0]['text'].strip()

                    if "```json" in text:
                        text = text.split("```json")[1].split("```")[0].strip()
                    elif "```" in text:
                        text = text.split("```")[1].split("```")[0].strip()

                    storyboard_pkg = json.loads(text)
                    swarm_log(f"✓ CLAUDE-VIDEO SUCCESS: Storyboard generated for [{storyboard_pkg.get('title')}]", node="CLAUDE_VIDEO")
                    return storyboard_pkg
                else:
                    swarm_log(f"[-] CLAUDE-VIDEO API Error: {resp.status_code} - {resp.text}", node="CLAUDE_VIDEO")
        except Exception as e:
            swarm_log(f"[-] CLAUDE-VIDEO Exception: {e}", node="CLAUDE_VIDEO")

        return None

claude_video = ClaudeVideoEngine()
