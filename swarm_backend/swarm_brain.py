# --- EMPIRE CENTRAL BRAIN: SOVEREIGN REASONING GATEWAY v2.1 (STABLE IMPORTS) ---
import asyncio
import httpx
import json
import re
import os
import base64
from swarm_logger import swarm_log
from dotenv import load_dotenv
from pathlib import Path

# Load env
load_dotenv(dotenv_path=Path(__file__).resolve().parent.parent / ".env")

OPENROUTER_KEY = os.getenv("OPENROUTER_API_KEY")

class CentralBrain:
    """
    SOVEREIGN BRAIN v2.2: Multi-model routing + Knowledge Retrieval.
    """
    def __init__(self):
        self.lock = asyncio.Lock()
        self.local_url = "http://localhost:11434/api/generate"
        self.cloud_url = "https://openrouter.ai/api/v1/chat/completions"

        # Model Hierarchy
        self.local_fast = "llama3.1:8b"
        self.local_deep = "anthony-brain:latest"
        self.local_vision = "llama3.2-vision:latest"
        self.cloud_elite = "meta-llama/llama-3.1-70b-instruct"

    def _get_local_context(self, query: str):
        """Retrieves matching Heretic or AI Toolkit resources for context injection."""
        from swarm_persistence import db
        context_parts = []
        try:
            with db._get_connection() as conn:
                # Search Heretic Resources
                rows = conn.execute("SELECT name, description, url FROM heretic_resources WHERE name LIKE ? OR category LIKE ? OR description LIKE ? LIMIT 3",
                                    (f"%{query}%", f"%{query}%", f"%{query}%")).fetchall()
                for r in rows: context_parts.append(f"RESOURCE: {r[0]} - {r[1]} ({r[2]})")

                # Search AI Toolkit
                tools = conn.execute("SELECT name, utility, description FROM ai_toolkit WHERE utility LIKE ? OR description LIKE ? LIMIT 3",
                                     (f"%{query}%", f"%{query}%")).fetchall()
                for t in tools: context_parts.append(f"TOOL: {t[0]} - {t[1]} ({t[2]})")
        except: pass
        return "\n".join(context_parts)

    async def generate_serialized(self, prompt: str, system_msg: str = "", timeout: int = 180, format: str = "json", complexity: str = "medium"):
        async with self.lock:
            # Inject local knowledge context
            local_context = self._get_local_context(prompt)
            if local_context:
                system_msg += f"\n\nUSE THIS LOCAL KNOWLEDGE IF RELEVANT:\n{local_context}"

            model = self.local_fast if complexity == "low" else self.local_deep
            if complexity == "high" and OPENROUTER_KEY:
                return await self._generate_cloud(prompt, system_msg, format)

            try:
                combined_prompt = f"{system_msg}\n\n{prompt}" if system_msg else prompt
                payload = {
                    "model": model,
                    "prompt": combined_prompt,
                    "stream": False,
                    "options": {"temperature": 0.8, "num_ctx": 32768}
                }
                if format == "json": payload["format"] = "json"

                async with httpx.AsyncClient(timeout=float(timeout)) as client:
                    resp = await client.post(self.local_url, json=payload)
                    if resp.status_code == 200:
                        result = resp.json().get("response", "").strip()
                        return self._hardened_parse(result, format)
            except Exception as e:
                swarm_log(f"BRAIN: Local miss ({e}). Falling back to Cloud...", node="BRAIN")
                return await self._generate_cloud(prompt, system_msg, format)

    async def inspect_visual(self, image_path: str, query: str):
        if not os.path.exists(image_path): return "IMAGE_NOT_FOUND"
        try:
            with open(image_path, "rb") as f:
                img_base64 = base64.b64encode(f.read()).decode('utf-8')

            payload = {
                "model": self.local_vision,
                "prompt": query,
                "images": [img_base64],
                "stream": False
            }
            async with httpx.AsyncClient(timeout=60.0) as client:
                resp = await client.post(self.local_url, json=payload)
                if resp.status_code == 200:
                    return resp.json().get("response", "").strip()
        except Exception as e:
            swarm_log(f"BRAIN VISION: Inspection failed: {e}", node="BRAIN")
        return "INSPECTION_UNAVAILABLE"

    async def _generate_cloud(self, prompt: str, system_msg: str, format: str):
        if not OPENROUTER_KEY: return None
        try:
            headers = {
                "Authorization": f"Bearer {OPENROUTER_KEY}",
                "Content-Type": "application/json",
                "X-Title": "Anthony AI Sovereign"
            }
            payload = {
                "model": self.cloud_elite,
                "messages": [
                    {"role": "system", "content": system_msg or "You are an elite Hollywood director."},
                    {"role": "user", "content": prompt}
                ],
                "response_format": {"type": "json_object"} if format == "json" else None
            }
            async with httpx.AsyncClient(timeout=60.0) as client:
                resp = await client.post(self.cloud_url, json=payload, headers=headers)
                if resp.status_code == 200:
                    result = resp.json()['choices'][0]['message']['content'].strip()
                    return self._hardened_parse(result, format)
        except: return None

    def _hardened_parse(self, text, format):
        if format != "json": return text
        json_match = re.search(r'(\{.*\}|\[.*\])', text, re.DOTALL)
        if json_match:
            result = json_match.group(1)
            try:
                json.loads(result)
                return result
            except: pass
        return text

# --- GLOBAL INSTANCE: Define before exports ---
brain_gate = CentralBrain()
