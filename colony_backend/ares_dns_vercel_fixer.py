# --- Built by Anthony Christopher | Est 12.19.1987 ---
# --- ARES MASTER DNS & VERCEL REDEPLOY FIXER ---
import asyncio
import os
import httpx
from pathlib import Path
from dotenv import load_dotenv
from colony_logger import colony_log
from obsidian_ares_engine import ares

load_dotenv(dotenv_path=Path(__file__).resolve().parent.parent / ".env")

CLOUDFLARE_API_TOKEN = os.getenv("CLOUDFLARE_API_TOKEN")
CLOUDFLARE_ZONE_ID = os.getenv("CLOUDFLARE_ZONE_ID")

class AresDnsVercelFixer:
    """
    ARES MASTER DNS & VERCEL REDEPLOY FIXER:
    1. Validates and pushes correct Cloudflare DNS records for Vercel ingress.
       - A Record (@ -> 76.76.21.21)
       - CNAME Record (www -> cname.vercel-dns.com)
    2. Triggers ARES browser automation to redeploy Vercel and clear cache.
    """
    def __init__(self):
        self.boss = "Anthony-Supreme-v29"

    async def execute_fix(self):
        colony_log("ARES DNS & VERCEL FIXER: Initializing infrastructure repair...", node="SUPREME")

        # 1. Verify/Configure Cloudflare DNS via API if credentials exist
        if CLOUDFLARE_API_TOKEN and CLOUDFLARE_ZONE_ID:
            colony_log("ARES DNS: Pushing Vercel A & CNAME records to Cloudflare...", node="SUPREME")
            url = f"https://api.cloudflare.com/client/v4/zones/{CLOUDFLARE_ZONE_ID}/dns_records"
            headers = {"Authorization": f"Bearer {CLOUDFLARE_API_TOKEN}", "Content-Type": "application/json"}

            records = [
                {"type": "A", "name": "@", "content": "76.76.21.21", "proxied": False},
                {"type": "CNAME", "name": "www", "content": "cname.vercel-dns.com", "proxied": False}
            ]
            async with httpx.AsyncClient() as client:
                for rec in records:
                    try:
                        resp = await client.post(url, headers=headers, json=rec)
                        colony_log(f"[*] DNS record {rec['type']} ({rec['name']}): status {resp.status_code}", node="SUPREME")
                    except Exception as e:
                        colony_log(f"[-] DNS API notice: {e}", node="SUPREME")
        else:
            colony_log("[*] Cloudflare API tokens not set in .env. Skipping automated DNS push.", node="SUPREME")

        # 2. Trigger ARES Vercel Redeploy
        colony_log("ARES VERCEL: Triggering autonomous Vercel redeploy and cache purge...", node="SUPREME")
        await ares.autonomous_vercel_redeploy(project_name="obsidian-city", domain="obsidian.city")

        colony_log("✓ ARES DNS & VERCEL FIXER: Infrastructure repair complete!", node="SUPREME")

if __name__ == "__main__":
    fixer = AresDnsVercelFixer()
    asyncio.run(fixer.execute_fix())
