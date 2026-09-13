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
from colony_logger import colony_log
from colony_persistence import db
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
    OBSIDIAN BRAIN v5.0 (SUPREME):
    Beyond Anthropic. Multi-model Mixture-of-Experts (MoE) cluster.
    - Layer 1: Human Output (Warm, simple, conversational)
    - Layer 2: Machine Control (Strict JSON schemas)
    - Layer 3: Supreme Orchestration (Claude 3.5 + GPT-4o + Gemini 1.5)
    """
    def __init__(self):
        from ares_supreme_orchestrator import orchestrator
        self.orchestrator = orchestrator
        self.lock = asyncio.Lock()
        self.native_supreme = "Anthony-Supreme-v29"

    async def generate_serialized(self, prompt: str, system_msg: str = "", task_type: str = "reasoning", format: str = "text", use_web: bool = False):
        """Dispatches commands to the Supreme Orchestrator for high-aura reasoning."""
        colony_log(f"BRAIN: Executing Supreme command for [{task_type}]...", node="BRAIN")

        # 🔱 Add System Instruction if provided
        final_prompt = f"{system_msg}\n\n{prompt}"

        response = await self.orchestrator.execute_supreme_command(final_prompt, task_type=task_type)

        if format == "json":
            # Attempt to extract JSON from response
            try:
                json_match = re.search(r'(\{.*\}|\[.*\])', response, re.DOTALL)
                return json_match.group(1) if json_match else response
            except: pass

        return response

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
            colony_log(f"BRAIN VISION: Frame inspection note: {e}", node="BRAIN")
        return "FRAME_INSPECTION_UNAVAILABLE"

    async def _generate_cloud(self, prompt: str, system_msg: str, format: str):
        if not OPENROUTER_KEY: return None

        headers = {
            "Authorization": f"Bearer {OPENROUTER_KEY}",
            "Content-Type": "application/json",
            "X-Title": "Anthony AI the Supreme Obsidian"
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
                        colony_log(f"BRAIN: Cloud rate limited (429). Retrying in {wait}s...", node="BRAIN")
                        await asyncio.sleep(wait)
                    else:
                        colony_log(f"BRAIN: Cloud Error {resp.status_code}: {resp.text[:100]}", node="BRAIN")
                        return None
            except Exception as e:
                colony_log(f"BRAIN: Cloud connection exception: {e}", node="BRAIN")
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
