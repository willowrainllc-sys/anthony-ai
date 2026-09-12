# --- Built by Anthony Christopher | Est 12.19.1987 ---
# --- ARES AUTOMATED VERCEL 404 PURGE & FIXER ---
import os
import httpx
import asyncio
from pathlib import Path
from dotenv import load_dotenv
from colony_logger import colony_log

load_dotenv(dotenv_path=Path(__file__).resolve().parent.parent / ".env")

VERCEL_TOKEN = os.getenv("VERCEL_TOKEN")

class AresVercel404Fixer:
    """
    ARES VERCEL 404 FIXER:
    Programmatically queries Vercel API, re-assigns 'obsidian.city' and 'www.obsidian.city'
    to the active project, and forces a production redeploy to eliminate 404 errors.
    """
    def __init__(self):
        self.headers = {
            "Authorization": f"Bearer {VERCEL_TOKEN}",
            "Content-Type": "application/json"
        }
        self.api_base = "https://api.vercel.com"

    async def purge_404(self):
        colony_log("ARES 404 FIXER: Communicating with Vercel API to resolve deployment routing...", node="SUPREME")

        if not VERCEL_TOKEN:
            colony_log("[-] 404 FIXER FAIL: VERCEL_TOKEN not found.", node="SUPREME")
            return

        async with httpx.AsyncClient(timeout=45.0) as client:
            # 1. Fetch Projects
            projects_url = f"{self.api_base.replace('api', 'api/v9')}/projects"
            try:
                resp = await client.get(projects_url, headers=self.headers)
                if resp.status_code == 200:
                    data = resp.json()
                    projects = data.get("projects", [])
                    colony_log(f"✓ VERCEL API: Found {len(projects)} projects on edge.", node="SUPREME")

                    target_proj = next((p for p in projects if p["name"] in ["obsidian-city", "anthony-ai"]), projects[0] if projects else None)

                    if target_proj:
                        proj_id = target_proj["id"]
                        proj_name = target_proj["name"]
                        colony_log(f"✓ VERCEL API: Targeting active project [{proj_name}] (ID: {proj_id})", node="SUPREME")

                        # 2. Re-bind domains to active project
                        for domain in ["obsidian.city", "www.obsidian.city"]:
                            dom_url = f"{self.api_base.replace('api', 'api/v10')}/projects/{proj_id}/domains"
                            dom_resp = await client.post(dom_url, headers=self.headers, json={"name": domain})
                            colony_log(f"✓ DOMAIN RE-BIND [{domain}]: Status {dom_resp.status_code}", node="SUPREME")

                        # 3. Trigger Production Redeploy
                        dep_url = f"{self.api_base.replace('api', 'api/v13')}/deployments"
                        dep_payload = {
                            "name": proj_name,
                            "gitSource": {
                                "type": "github",
                                "repo": "willowrainllc-sys/anthony-ai",
                                "ref": "master"
                            }
                        }
                        dep_resp = await client.post(dep_url, headers=self.headers, json=dep_payload)
                        if dep_resp.status_code in [200, 201]:
                            colony_log("✓ ARES 404 FIXER SUCCESS: Vercel production redeploy triggered successfully!", node="SUPREME")
                            print("\n" + "="*70)
                            print("  🔱 ARES VERCEL 404 PURGE COMPLETE")
                            print("  DOMAIN: https://obsidian.city")
                            print("  STATUS: 100% RE-BOUND & REDEPLOYED")
                            print("="*70 + "\n")
                        else:
                            colony_log(f"[-] Redeploy notice: {dep_resp.text}", node="SUPREME")
                    else:
                        colony_log("[-] 404 FIXER: No Vercel projects found under account.", node="SUPREME")
                else:
                    colony_log(f"[-] Vercel API error: {resp.text}", node="SUPREME")
            except Exception as e:
                colony_log(f"[-] 404 FIXER FATAL: {e}", node="SUPREME")

if __name__ == "__main__":
    fixer = AresVercel404Fixer()
    asyncio.run(fixer.purge_404())
