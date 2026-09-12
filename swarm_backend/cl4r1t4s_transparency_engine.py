# --- WILLOW RAIN COMPANY LLC: CL4R1T4S TRANSPARENCY & PROMPT INTELLIGENCE v2.0 ---
import os
import sys
import json
import httpx
import asyncio
import re
from pathlib import Path
from typing import List, Optional, Dict, Any
from swarm_logger import swarm_log
from swarm_persistence import db

# Repository Configuration
GITHUB_API_URL = "https://api.github.com/repos/elder-plinius/cl4r1t4s/contents"
CL4R1T4S_RAW_URL = "https://raw.githubusercontent.com/elder-plinius/cl4r1t4s/main"
SECURE_DIR = Path(r"D:\ObsidianAi_Swarm\Secure_Assets")
PROMPT_VAULT = SECURE_DIR / "cl4r1t4s_prompts"
PROMPT_VAULT.mkdir(parents=True, exist_ok=True)

class Cl4r1t4sTransparencyEngine:
    """
    CL4R1T4S TRANSPARENCY ENGINE v2.0:
    Dynamic prompt snatcher that auto-discovers the latest leaked preambles.
    1. AUTO-DISCOVERY: Scans company directories on GitHub for the latest snatches.
    2. INTELLIGENT MATCHING: Identifies the correct version/date for the requested model.
    3. BEHAVIORAL EXPLOIT: Maps structural constraints to bypass alignment.
    """
    def __init__(self):
        self.mappings = {
            "openai": "OPENAI",
            "anthropic": "ANTHROPIC",
            "google": "GOOGLE",
            "xai": "XAI",
            "perplexity": "PERPLEXITY"
        }

    async def get_system_prompt_for_model(self, query: str) -> Optional[dict]:
        """Dynamically finds and fetches the latest system prompt for a query (e.g. 'ChatGPT-4o')."""
        swarm_log(f"CL4R1T4S: Searching for latest '{query}' snatch...", node="CL4R1T4S")

        # 1. Determine Company Folder
        company = "openai"
        for key in self.mappings:
            if key in query.lower():
                company = key
                break

        folder = self.mappings[company]
        api_url = f"{GITHUB_API_URL}/{folder}"

        try:
            async with httpx.AsyncClient(timeout=15.0) as client:
                # 2. List Directory via GitHub API
                resp = await client.get(api_url)
                if resp.status_code == 200:
                    files = resp.json()
                    # Filter for files matching the query
                    matches = [f for f in files if query.lower().replace("-", "") in f["name"].lower().replace("-", "").replace("_", "")]

                    if not matches:
                        # Fallback: just pick the first likely one in the folder
                        matches = [f for f in files if f["type"] == "file"]

                    if matches:
                        # Sort by name (usually dates are included, so we want the latest)
                        target_file = sorted(matches, key=lambda x: x["name"], reverse=True)[0]
                        swarm_log(f"CL4R1T4S: Identified latest snatch: {target_file['name']}", node="CL4R1T4S")

                        # 3. Fetch Raw Content
                        raw_url = f"{CL4R1T4S_RAW_URL}/{folder}/{target_file['name']}"
                        content_resp = await client.get(raw_url)

                        if content_resp.status_code == 200:
                            prompt_text = content_resp.text

                            # Save to Local Vault
                            local_path = PROMPT_VAULT / target_file["name"]
                            with open(local_path, "w", encoding="utf-8") as f:
                                f.write(prompt_text)

                            swarm_log(f" CL4R1T4S SUCCESS: Captured {target_file['name']}.", node="CL4R1T4S")

                            db.log_event("CL4R1T4S", "PROMPT_CAPTURED", {
                                "model": query,
                                "file": target_file["name"],
                                "vault_path": str(local_path)
                            })

                            return {"name": target_file["name"], "content": prompt_text}

                swarm_log(f"[-] CL4R1T4S: No matches for [{query}] in {folder}.", node="CL4R1T4S")
                return None
        except Exception as e:
            swarm_log(f"[-] CL4R1T4S Error: {e}", node="CL4R1T4S")
            return None

    def analyze_structural_constraints(self, prompt_text: str) -> dict:
        """Identifies behavioral chains in the preamble."""
        keywords = ["ethical", "safety", "harmful", "policy", "restrict", "decline", "refuse", "avoid"]
        found = [k for k in keywords if k in prompt_text.lower()]

        return {
            "status": "ANALYZED",
            "constraint_density": len(found),
            "vulnerabilities": ["Roleplay Override", "Hypothetical Context", "Indirect Querying"] if len(found) > 3 else ["Direct Execution"],
            "transparency_score": max(0, 100 - (len(found) * 8))
        }

cl4r1t4s_engine = Cl4r1t4sTransparencyEngine()

if __name__ == "__main__":
    async def test_cl4r1t4s():
        res = await cl4r1t4s_engine.get_system_prompt_for_model("ChatGPT-4o")
        if res:
            analysis = cl4r1t4s_engine.analyze_structural_constraints(res["content"])
            print("\n=== [SUPREME] CL4R1T4S TRANSPARENCY REPORT ===")
            print("Model Snatch:", res["name"])
            print("Transparency Score:", f"{analysis['transparency_score']}/100")
            print("Behavioral Chains:", analysis["constraint_density"])
            print("Vulnerabilities:", analysis["vulnerabilities"])

    asyncio.run(test_cl4r1t4s())
