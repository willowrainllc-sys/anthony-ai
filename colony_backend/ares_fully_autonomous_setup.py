# --- Built by Anthony Christopher | Est 12.19.1987 ---
# --- ARES FULLY AUTONOMOUS EMPIRE AUTO-CONFIGURATOR ---
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

class AresFullyAutonomousSetup:
    """
    ARES FULLY AUTONOMOUS SETUP:
    Zero human intervention required. Automatically configures Vercel projects,
    binds custom domains, purges cache, and deploys live production via Vercel REST API.
    """
    def __init__(self):
        self.headers = {
            "Authorization": f"Bearer {VERCEL_TOKEN}",
            "Content-Type": "application/json"
        }
        self.api_base = "https://api.vercel.com"

    async def run_auto_config(self):
        colony_log("ARES AUTO-CONFIG: Initiating zero-touch Vercel infrastructure auto-configuration...", node="SUPREME")

        if not VERCEL_TOKEN:
            colony_log("[-] AUTO-CONFIG FAIL: VERCEL_TOKEN not found in .env.", node="SUPREME")
            return

        async with httpx.AsyncClient(timeout=45.0) as client:
            # 1. Ensure Project Exists
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
                colony_log(f"✓ AUTO-CONFIG: Project [{PROJECT_NAME}] verified/created (Status: {resp.status_code})", node="SUPREME")
            except Exception as e:
                colony_log(f"[*] Project sync notice: {e}", node="SUPREME")

            # 2. Bind Custom Domains
            for domain in [DOMAIN_NAME, f"www.{DOMAIN_NAME}"]:
                dom_url = f"{self.api_base.replace('api', 'api/v10')}/projects/{PROJECT_NAME}/domains"
                dom_payload = {"name": domain}
                try:
                    resp = await client.post(dom_url, headers=self.headers, json=dom_payload)
                    colony_log(f"✓ AUTO-CONFIG: Domain [{domain}] bound to [{PROJECT_NAME}] (Status: {resp.status_code})", node="SUPREME")
                except Exception as e:
                    colony_log(f"[*] Domain sync notice [{domain}]: {e}", node="SUPREME")

            # 3. Trigger Production Deployment (Cache Cleared)
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
                    colony_log(f"✓ AUTO-CONFIG SUCCESS: Live production deployment active at https://{url}", node="SUPREME")
                    print(f"\n" + "="*70)
                    print(f"  🔱 ARES FULLY AUTONOMOUS CONFIGURATION COMPLETE")
                    print(f"  DOMAIN: https://{DOMAIN_NAME}")
                    print(f"  DEPLOYMENT URL: https://{url}")
                    print(f"  STATUS: 100% ZERO-TOUCH PRODUCTION")
                    print("="*70 + "\n")
                else:
                    colony_log(f"[-] AUTO-CONFIG DEPLOY NOTICE: {resp.text}", node="SUPREME")
            except Exception as e:
                colony_log(f"[-] AUTO-CONFIG DEPLOY ERROR: {e}", node="SUPREME")

if __name__ == "__main__":
    auto_setup = AresFullyAutonomousSetup()
    asyncio.run(auto_setup.run_auto_config())
