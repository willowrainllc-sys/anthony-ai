# --- Built by Anthony Christopher | Est 12.19.1987 ---
# --- ARES VERCEL PERFECT SETUP & API DEPLOYER ---
import os
import httpx
import asyncio
from pathlib import Path
from dotenv import load_dotenv
from colony_logger import colony_log

load_dotenv(dotenv_path=Path(__file__).resolve().parent.parent / ".env")

VERCEL_TOKEN = os.getenv("VERCEL_TOKEN")
PROJECT_NAME = "obsidian-city"
DOMAIN_NAME = "obsidian.city"

class VercelPerfectSetup:
    """
    VERCEL PERFECT SETUP & API DEPLOYER:
    Configures and deploys the project to Vercel via official REST API:
    1. Creates/Configures Project 'obsidian-city'.
    2. Links GitHub repository.
    3. Adds custom domains 'obsidian.city' & 'www.obsidian.city'.
    4. Triggers instant production deployment.
    """
    def __init__(self):
        self.headers = {
            "Authorization": f"Bearer {VERCEL_TOKEN}",
            "Content-Type": "application/json"
        }
        self.api_base = "https://api.vercel.com"

    async def setup_and_deploy(self):
        colony_log(f"VERCEL SETUP: Configuring project [{PROJECT_NAME}] for [{DOMAIN_NAME}]...", node="SUPREME")

        if not VERCEL_TOKEN:
            colony_log("[-] VERCEL SETUP FAIL: VERCEL_TOKEN not found in .env.", node="SUPREME")
            return

        async with httpx.AsyncClient(timeout=30.0) as client:
            # 1. Create Project
            proj_url = f"{self.api_base.replace('api', 'api/v9')}/projects"
            proj_payload = {
                "name": PROJECT_NAME,
                "gitRepository": {
                    "type": "github",
                    "repo": "willowrainllc-sys/anthony-ai"
                }
            }
            try:
                resp = await client.post(proj_url, headers=self.headers, json=proj_payload)
                if resp.status_code in [200, 201]:
                    colony_log(f"✓ VERCEL SETUP: Project [{PROJECT_NAME}] created successfully.", node="SUPREME")
                else:
                    colony_log(f"[*] VERCEL SETUP NOTICE: Project creation response: {resp.status_code} - {resp.text}", node="SUPREME")
            except Exception as e:
                colony_log(f"[-] VERCEL PROJECT API ERROR: {e}", node="SUPREME")

            # 2. Add Custom Domains
            for domain in [DOMAIN_NAME, f"www.{DOMAIN_NAME}"]:
                dom_url = f"{self.api_base.replace('api', 'api/v10')}/projects/{PROJECT_NAME}/domains"
                dom_payload = {"name": domain}
                try:
                    resp = await client.post(dom_url, headers=self.headers, json=dom_payload)
                    if resp.status_code in [200, 201]:
                        colony_log(f"✓ VERCEL DOMAIN SUCCESS: [{domain}] linked to [{PROJECT_NAME}].", node="SUPREME")
                    else:
                        colony_log(f"[*] VERCEL DOMAIN NOTICE [{domain}]: {resp.text}", node="SUPREME")
                except Exception as e:
                    colony_log(f"[-] VERCEL DOMAIN API ERROR [{domain}]: {e}", node="SUPREME")

            # 3. Trigger Deployment
            dep_url = f"{self.api_base.replace('api', 'api/v13')}/deployments"
            dep_payload = {
                "name": PROJECT_NAME,
                "gitSource": {
                    "type": "github",
                    "repo": "willowrainllc-sys/anthony-ai",
                    "ref": "master"
                },
                "projectSettings": {
                    "rootDirectory": ""
                }
            }
            try:
                resp = await client.post(dep_url, headers=self.headers, json=dep_payload)
                if resp.status_code in [200, 201]:
                    data = resp.json()
                    url = data.get("url", "N/A")
                    colony_log(f"✓ VERCEL DEPLOY SUCCESS: Live at https://{url}", node="SUPREME")
                    print(f"\n🔱 [VERCEL PERFECT SETUP SUCCESS]:\nProject: {PROJECT_NAME}\nLive URL: https://{url}\nCustom Domain: https://{DOMAIN_NAME}\n")
                else:
                    colony_log(f"[-] VERCEL DEPLOY NOTICE: {resp.text}", node="SUPREME")
            except Exception as e:
                colony_log(f"[-] VERCEL DEPLOY API ERROR: {e}", node="SUPREME")

if __name__ == "__main__":
    setup = VercelPerfectSetup()
    asyncio.run(setup.setup_and_deploy())
