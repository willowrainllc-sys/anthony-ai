# --- EMPIRE BRADAUTOMATES CLAUDE-VIDEO ENGINE v1.0 ---
import os
import sys
import json
import asyncio
import httpx
from pathlib import Path
from swarm_logger import swarm_log
from dotenv import load_dotenv

load_dotenv(dotenv_path=Path(__file__).resolve().parent.parent / ".env")

class BradAutomatesClaudeVideoEngine:
    """
    BRADAUTOMATES CLAUDE-VIDEO ENGINE:
    Automated video script & visual prompt orchestration.
    Converts raw topic ideas into high-retention 3-second micro-storyboard scenes.
    """
    def __init__(self):
        self.api_key = os.getenv("ANTHROPIC_API_KEY") or os.getenv("OPENROUTER_API_KEY")
        self.anthropic_endpoint = "https://api.anthropic.com/v1/messages"

    async def generate_script_and_storyboard(self, topic: str, target_length: str = "short") -> dict:
        swarm_log(f"BRADAUTOMATES: Processing claude-video pipeline for [{topic[:30]}]...", node="BRADAUTOMATES")

        # System prompt inspired by BradAutomates video generation architecture
        system_prompt = """
        You are BradAutomates Claude-Video AI Engine.
        Your job is to generate a viral, high-retention video script and exact 4K visual scene prompts.
        RULES:
        1. 0-second pattern interrupt hook.
        2. Fast 3-to-5 second scene cuts.
        3. Clear narration script matching 4K visual search prompts.
        4. Return JSON format strictly.
        """

        user_prompt = f"""
        TOPIC: {topic}
        FORMAT: {target_length}

        OUTPUT JSON SCHEMA:
        {{
            "title": "Viral Title",
            "script": "Full narrative voiceover text...",
            "scenes": [
                {{
                    "scene_num": 1,
                    "narration": "First hook sentence...",
                    "visual_prompt": "4K cinematic shot description for video search...",
                    "on_screen_text": "HOOK TEXT"
                }}
            ],
            "tags": ["#Shorts", "#Documentary", "#Viral"]
        }}
        """

        # 1. Try Claude via direct Anthropic API if key exists
        if os.getenv("ANTHROPIC_API_KEY"):
            try:
                headers = {
                    "x-api-key": os.getenv("ANTHROPIC_API_KEY"),
                    "anthropic-version": "2023-06-01",
                    "content-type": "application/json"
                }
                payload = {
                    "model": "claude-3-5-sonnet-20241022",
                    "max_tokens": 2048,
                    "system": system_prompt,
                    "messages": [{"role": "user", "content": user_prompt}]
                }
                async with httpx.AsyncClient(timeout=45.0) as client:
                    resp = await client.post(self.anthropic_endpoint, json=payload, headers=headers)
                    if resp.status_code == 200:
                        raw = resp.json()['content'][0]['text']
                        if "```json" in raw: raw = raw.split("```json")[1].split("```")[0]
                        elif "```" in raw: raw = raw.split("```")[1].split("```")[0]
                        data = json.loads(raw.strip())
                        swarm_log("✓ BRADAUTOMATES: Successfully generated script via Anthropic Claude.", node="BRADAUTOMATES")
                        return data
            except Exception as e:
                swarm_log(f"BRADAUTOMATES Claude Direct Note: {e}", node="BRADAUTOMATES")

        # 2. Fallback: Use Sovereign Central Brain / Local Ollama
        from swarm_brain import brain_gate
        try:
            raw_res = await brain_gate.generate_serialized(
                prompt=user_prompt,
                system_msg=system_prompt,
                format="json",
                complexity="high"
            )
            if raw_res:
                data = json.loads(raw_res)
                swarm_log("✓ BRADAUTOMATES: Generated script via Sovereign Central Brain.", node="BRADAUTOMATES")
                return data
        except Exception as e:
            swarm_log(f"BRADAUTOMATES Central Brain Note: {e}", node="BRADAUTOMATES")

        # 3. Hardened Backup Payload
        return {
            "title": f"The Secret of {topic}",
            "script": f"Deep beneath the surface, researchers uncovered an unclassified data anomaly regarding {topic}. The findings change everything.",
            "scenes": [
                {
                    "scene_num": 1,
                    "narration": f"Deep beneath the surface, researchers uncovered an anomaly regarding {topic}.",
                    "visual_prompt": f"{topic} aerial cinematic drone 4k",
                    "on_screen_text": "UNCLASSIFIED DATA"
                },
                {
                    "scene_num": 2,
                    "narration": "The findings were wiped from public feeds, but the raw logs remain.",
                    "visual_prompt": f"{topic} close up high contrast studio 4k",
                    "on_screen_text": "RAW LOGS REMAIN"
                }
            ],
            "tags": ["#Documentary", "#Shorts", "#Unexplained"]
        }

brad_claude_engine = BradAutomatesClaudeVideoEngine()

if __name__ == "__main__":
    res = asyncio.run(brad_claude_engine.generate_script_and_storyboard("Subterranean Amazon Complex"))
    print(json.dumps(res, indent=4))
