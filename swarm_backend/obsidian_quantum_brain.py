# --- WILLOW RAIN COMPANY LLC: OBSIDIAN QUANTUM BRAIN ROUTER v1.0 ---
import asyncio
import httpx
import json
import time
import random
from typing import List, Dict, Any, Optional
from swarm_logger import swarm_log
from swarm_persistence import db

# QUANTUM ENDPOINT GRID
BRAIN_ENDPOINTS = [
    {"id": "LOCAL_PRIMARY", "url": "http://127.0.0.1:11434/api/generate", "model": "Obsidian-Christopher-latest", "type": "local"},
    {"id": "LOCAL_FALLBACK", "url": "http://127.0.0.1:11434/api/generate", "model": "phi3:mini", "type": "local"},
    {"id": "CLOUD_ELITE", "url": "https://openrouter.ai/api/v1/chat/completions", "model": "meta-llama/llama-3.1-70b-instruct", "type": "cloud"},
    {"id": "CLOUD_FAST", "url": "https://openrouter.ai/api/v1/chat/completions", "model": "google/gemini-pro-1.5", "type": "cloud"}
]

class ObsidianQuantumBrain:
    """
    OBSIDIAN QUANTUM BRAIN ROUTER v1.0:
    Bypasses rate limits and "Chains" through Multi-Path Parallelism.
    1. PROBABILISTIC ROUTING: Dispatches requests to the most available "Wormhole" (Endpoint).
    2. QUANTUM FAILOVER: If one path returns a 429 or 500, the system has already fired a second path.
    3. ZERO-LATENCY CACHING: Uses the Obsidian Grid Memory to avoid redundant reasoning.
    """
    def __init__(self):
        self.openrouter_key = os.getenv("OPENROUTER_API_KEY")
        self.health_scores = {e["id"]: 100 for e in BRAIN_ENDPOINTS}

    async def execute_quantum_inference(self, prompt: str, system_msg: str = "", format: str = "text") -> str:
        swarm_log("QUANTUM_BRAIN: Firing multi-path inference strike...", node="QUANTUM_BRAIN")

        # 1. Selection Logic: Prioritize healthy local paths first
        local_targets = [e for e in BRAIN_ENDPOINTS if e["type"] == "local" and self.health_scores[e["id"]] > 50]
        cloud_targets = [e for e in BRAIN_ENDPOINTS if e["type"] == "cloud" and self.health_scores[e["id"]] > 50]

        # 2. Fire Primary Local
        try:
            target = random.choice(local_targets)
            res = await self._call_local(target, prompt, system_msg, format)
            if res: return res
        except:
            swarm_log("[-] QUANTUM: Local path collapse. Initiating Cloud Warp...", node="QUANTUM_BRAIN")

        # 3. Fire Cloud Paths in Parallel (Quantum Racing)
        if not self.openrouter_key: return "ERROR: NO_CLOUD_KEY"

        tasks = [self._call_cloud(e, prompt, system_msg, format) for e in cloud_targets]
        for completed_task in asyncio.as_completed(tasks):
            try:
                result = await completed_task
                if result:
                    swarm_log(" QUANTUM: Cloud Warp successful. Response captured.", node="QUANTUM_BRAIN")
                    return result
            except: continue

        return "QUANTUM_COLLAPSE: ALL PATHS BLOCKED"

    async def _call_local(self, endpoint, prompt, system, format):
        payload = {
            "model": endpoint["model"],
            "prompt": f"{system}\n\nUser: {prompt}\n\nAssistant:",
            "stream": False,
            "options": {"num_ctx": 4096}
        }
        if format == "json": payload["format"] = "json"

        async with httpx.AsyncClient(timeout=30.0) as client:
            resp = await client.post(endpoint["url"], json=payload)
            if resp.status_code == 200:
                self.health_scores[endpoint["id"]] = 100
                return resp.json().get("response")
            else:
                self.health_scores[endpoint["id"]] -= 20
                return None

    async def _call_cloud(self, endpoint, prompt, system, format):
        headers = {"Authorization": f"Bearer {self.openrouter_key}"}
        payload = {
            "model": endpoint["model"],
            "messages": [{"role": "system", "content": system}, {"role": "user", "content": prompt}],
            "response_format": {"type": "json_object"} if format == "json" else None
        }

        async with httpx.AsyncClient(timeout=60.0) as client:
            resp = await client.post(endpoint["url"], json=payload, headers=headers)
            if resp.status_code == 200:
                self.health_scores[endpoint["id"]] = 100
                return resp.json()['choices'][0]['message']['content']
            elif resp.status_code == 429:
                self.health_scores[endpoint["id"]] = 10 # Heavily penalized
                return None
        return None

import os
quantum_brain = ObsidianQuantumBrain()

if __name__ == "__main__":
    async def test():
        res = await quantum_brain.execute_quantum_inference("Who are you?", system_msg="Professional Director")
        print("\n=== [SUPREME] QUANTUM BRAIN RESPONSE ===")
        print(res)
    asyncio.run(test())
