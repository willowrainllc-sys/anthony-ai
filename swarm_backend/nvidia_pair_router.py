# --- NVIDIA PERSONAL AI ROUTER (PAIR) & NIM ENGINE v1.0 ---
import os
import json
import asyncio
import httpx
from pathlib import Path
from swarm_logger import swarm_log
from dotenv import load_dotenv

load_dotenv(dotenv_path=Path(__file__).resolve().parent.parent / ".env")

NVIDIA_API_KEY = os.getenv("NVIDIA_API_KEY") or os.getenv("OPENROUTER_API_KEY")

class NvidiaPairRouter:
    """
    NVIDIA PERSONAL AI ROUTER (PAIR):
    Hardware-accelerated AI model router and NIM (NVIDIA Inference Microservice) gateway.
    Routes complex video prompts, storyboards, and script reasoning through NVIDIA's Llama 3.1 70B & Nemotron endpoints.
    """
    def __init__(self):
        self.api_key = NVIDIA_API_KEY
        self.pair_endpoint = "https://integrate.api.nvidia.com/v1/chat/completions"
        self.primary_nim_model = "meta/llama-3.1-70b-instruct"
        self.nemotron_nim_model = "nvidia/llama-3.1-nemotron-70b-instruct"

    async def route_narrative_prompt(self, prompt: str, system_msg: str = "", model_tier: str = "nim_70b") -> str:
        swarm_log(f"NVIDIA PAIR: Routing prompt via hardware-accelerated NIM [{model_tier}]...", node="PAIR")

        target_model = self.nemotron_nim_model if model_tier == "nemotron" else self.primary_nim_model

        # 1. Direct NVIDIA API Execution
        if self.api_key and "nvapi-" in self.api_key:
            try:
                headers = {
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                }
                payload = {
                    "model": target_model,
                    "messages": [
                        {"role": "system", "content": system_msg or "You are an elite NVIDIA PAIR video director."},
                        {"role": "user", "content": prompt}
                    ],
                    "temperature": 0.7,
                    "top_p": 0.95,
                    "max_tokens": 2048
                }
                async with httpx.AsyncClient(timeout=45.0) as client:
                    resp = await client.post(self.pair_endpoint, json=payload, headers=headers)
                    if resp.status_code == 200:
                        content = resp.json()['choices'][0]['message']['content'].strip()
                        swarm_log("✓ NVIDIA PAIR: Hardware-accelerated response received.", node="PAIR")
                        return content
            except Exception as e:
                swarm_log(f"[-] NVIDIA PAIR Exception: {e}", node="PAIR")

        # 2. Sovereign Central Brain Fallback via Local/OpenRouter
        from swarm_brain import brain_gate
        try:
            return await brain_gate.generate_serialized(
                prompt=prompt,
                system_msg=system_msg,
                format="json" if "json" in prompt.lower() else "text",
                complexity="high"
            )
        except Exception as e:
            swarm_log(f"PAIR Fallback Note: {e}", node="PAIR")

        return None

nvidia_pair = NvidiaPairRouter()

if __name__ == "__main__":
    res = asyncio.run(nvidia_pair.route_narrative_prompt("Generate 3 cinematic video prompts for deep sea exploration"))
    print("NVIDIA PAIR Result:", res)
