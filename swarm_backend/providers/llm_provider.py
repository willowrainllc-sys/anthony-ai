# --- EMPIRE LLM PROVIDER: SOVEREIGN REASONING ADAPTER v1.0 ---
import asyncio
import json
from .base_provider import LLMProvider
from swarm_brain import brain_gate

class SovereignLLMProvider(LLMProvider):
    """
    Adapter for the Central Brain reasoning gateway.
    Uses local 'anthony-brain' with cloud failover.
    """
    async def generate_text(self, prompt: str, system_msg: str = "", format: str = "text") -> str:
        # Route to brain_gate which already handles routing and parse hardening
        complexity = "high" if "script" in prompt.lower() or "story" in prompt.lower() else "medium"
        return await brain_gate.generate_serialized(
            prompt,
            system_msg=system_msg,
            format=format,
            complexity=complexity
        )

llm_provider = SovereignLLMProvider()
