# --- EMPIRE CENTRAL BRAIN: OBSIDIAN PRODUCTION ORCHESTRATOR & TASK ROUTER v4.0 ---
import asyncio
import httpx
import json
import re
import os
import base64
import time
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field
from swarm_logger import swarm_log
from swarm_persistence import db
from dotenv import load_dotenv
from pathlib import Path

load_dotenv(dotenv_path=Path(__file__).resolve().parent.parent / ".env")

OPENROUTER_KEY = os.getenv("OPENROUTER_API_KEY")

# ============================================================
# 1. TASK ROUTING MATRIX & PRODUCTION CONTRACT SCHEMAS
# ============================================================

TASK_ROUTING = {
    "story_architecture": "Anthony-Supreme-v29",
    "character_bible": "Anthony-Supreme-v29",
    "shot_planning": "Anthony-Supreme-v29",
    "simple_metadata": "Anthony-Supreme-v29", # Middlemen (Phi-3) excommunicated
    "classification": "Anthony-Supreme-v29",
    "visual_qa": "Anthony-Supreme-v29",
    "frame_comparison": "Anthony-Supreme-v29",
    "complex_recovery": "Anthony-Supreme-v29" # Cloud Llama ditched
}

HUMAN_OUTPUT_INSTRUCTION = """
You are an expert, friendly AI assistant.
Speak in warm, simple, natural, conversational human language ONLY.
No technical jargon or AI buzzwords. Keep sentences clear, engaging, and direct.
"""

MACHINE_CONTROL_INSTRUCTION = """
You are a strict JSON Production Orchestrator.
Output ONLY valid, parseable JSON matching the requested schema.
No conversational filler, no markdown wrapping.
"""

class PublishPolicy(BaseModel):
    requires_qa: bool = True
    minimum_score: int = 90
    publish_live_env: bool = False

class ProductionContract(BaseModel):
    job_id: str
    objective: str
    story_id: str
    required_beats: List[str] = Field(default_factory=list)
    characters: Dict[str, Any] = Field(default_factory=dict)
    locations: Dict[str, Any] = Field(default_factory=dict)
    shots: List[Dict[str, Any]] = Field(default_factory=list)
    audio_plan: Dict[str, Any] = Field(default_factory=dict)
    caption_plan: Dict[str, Any] = Field(default_factory=dict)
    metadata: Dict[str, Any] = Field(default_factory=dict)
    qa_requirements: Dict[str, Any] = Field(default_factory=dict)
    publish_policy: PublishPolicy = Field(default_factory=PublishPolicy)

# ============================================================
# 2. CENTRAL BRAIN SYSTEM ARCHITECTURE
# ============================================================

class CentralBrain:
    """
    OBSIDIAN BRAIN v4.0:
    3-Layer Architecture:
    - Layer 1: Human Output (Warm, simple, conversational for users)
    - Layer 2: Machine Control (Strict JSON schemas for internal agents)
    - Layer 3: Task-Based Model Routing (Obsidian AI local fast/deep/vision + Cloud fallback)
    """
    def __init__(self):
        self.lock = asyncio.Lock()
        self.local_url = "http://127.0.0.1:9000/v1/chat/completions" # Points to Native Supreme Base
        self.cloud_url = None # Excommunicated

        self.native_supreme = "Anthony-Supreme-v29"
        self.local_vision = "Anthony-Vision-v1"

    def get_model_for_task(self, task_type: str) -> str:
        """Explicit task-based routing rule lookup."""
        return TASK_ROUTING.get(task_type, self.local_deep)

    def _get_local_context(self, query: str) -> str:
        context_parts = []
        try:
            with db._get_connection() as conn:
                rows = conn.execute("SELECT name, description, url FROM heretic_resources WHERE name LIKE ? OR category LIKE ? OR description LIKE ? LIMIT 3",
                                    (f"%{query}%", f"%{query}%", f"%{query}%")).fetchall()
                for r in rows: context_parts.append(f"RESOURCE: {r[0]} - {r[1]} ({r[2]})")

                tools = conn.execute("SELECT name, utility, description FROM ai_toolkit WHERE utility LIKE ? OR description LIKE ? LIMIT 3",
                                     (f"%{query}%", f"%{query}%")).fetchall()
                for t in tools: context_parts.append(f"TOOL: {t[0]} - {t[1]} ({t[2]})")
        except: pass
        return "\n".join(context_parts)

    async def generate_serialized(self, prompt: str, system_msg: str = "", timeout: int = 300, format: str = "json", task_type: str = "story_architecture", complexity: str = "medium", use_web: bool = False, bot_id: str = None, security_headers: dict = None):
        """
        UPGRADED: SECURE QUANTUM ROUTING.
        If a bot_id is provided, the request must pass the Obsidian Brain Gate.
        """
        # 1. SECURITY VALIDATION
        if bot_id:
            from obsidian_brain_gate import brain_gate_security
            is_valid = await brain_gate_security.validate_access(bot_id, security_headers or {})
            if not is_valid:
                return {"status": "error", "message": "SECURITY_BLOCK: ACCESS DENIED BY BRAIN GATE"}

        # 2. LIVE WEB ENRICHMENT
        web_context = ""
        if use_web or "search" in prompt.lower() or "latest" in prompt.lower():
            try:
                from obsidian_web_search import web_search_engine
                # Extract a search query from the prompt
                search_query = prompt[:100] # Simplification
                web_context = await web_search_engine.get_web_context_for_prompt(search_query)
            except: pass

        try:
            from obsidian_quantum_brain import quantum_brain
            enriched_prompt = f"{prompt}{web_context}"
            return await quantum_brain.execute_quantum_inference(enriched_prompt, system_msg, format)
        except Exception as e:
            swarm_log(f"BRAIN: Quantum override failed ({e}). Falling back to legacy routing.", node="BRAIN")

        # Legacy fallback logic below...

    async def inspect_visual_frame(self, image_path: str, query: str) -> str:
        """Layer 3: Visual Inspection via Llama3.2-Vision model."""
        if not os.path.exists(image_path): return "FRAME_NOT_FOUND"
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
            swarm_log(f"BRAIN VISION: Frame inspection note: {e}", node="BRAIN")
        return "FRAME_INSPECTION_UNAVAILABLE"

    async def _generate_cloud(self, prompt: str, system_msg: str, format: str):
        if not OPENROUTER_KEY: return None

        headers = {
            "Authorization": f"Bearer {OPENROUTER_KEY}",
            "Content-Type": "application/json",
            "X-Title": "Obsidian AI Obsidian"
        }
        payload = {
            "model": self.cloud_elite,
            "messages": [
                {"role": "system", "content": system_msg},
                {"role": "user", "content": prompt}
            ],
            "response_format": {"type": "json_object"} if format == "json" else None
        }

        for attempt in range(3):
            try:
                async with httpx.AsyncClient(timeout=60.0) as client:
                    resp = await client.post(self.cloud_url, json=payload, headers=headers)
                    if resp.status_code == 200:
                        result = resp.json()['choices'][0]['message']['content'].strip()
                        return self._hardened_parse(result, format)
                    elif resp.status_code == 429:
                        wait = (attempt + 1) * 10
                        swarm_log(f"BRAIN: Cloud rate limited (429). Retrying in {wait}s...", node="BRAIN")
                        await asyncio.sleep(wait)
                    else:
                        swarm_log(f"BRAIN: Cloud Error {resp.status_code}: {resp.text[:100]}", node="BRAIN")
                        return None
            except Exception as e:
                swarm_log(f"BRAIN: Cloud connection exception: {e}", node="BRAIN")
                await asyncio.sleep(5)

        return None

    def _hardened_parse(self, text: str, format: str):
        if format != "json": return text
        json_match = re.search(r'(\{.*\}|\[.*\])', text, re.DOTALL)
        if json_match:
            result = json_match.group(1)
            try:
                json.loads(result)
                return result
            except: pass
        return text

brain_gate = CentralBrain()

if __name__ == "__main__":
    print("Central Brain v4.0 Task Router Initialized.")
    print("Story Architecture Model:", brain_gate.get_model_for_task("story_architecture"))
    print("Classification Model:", brain_gate.get_model_for_task("classification"))
    print("Visual QA Model:", brain_gate.get_model_for_task("visual_qa"))
