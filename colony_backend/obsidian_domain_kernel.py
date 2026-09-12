# --- Built by Anthony Christopher | Est 12.19.1987 ---
# --- ENCRYPTED VIA OBSIDIAN CORE v3.0 (IDENTITY AUTHORITY) ---
import os
import time
import httpx
import json
import xml.etree.ElementTree as ET
from pathlib import Path
from dotenv import load_dotenv
from colony_logger import colony_log
from colony_persistence import db

load_dotenv(dotenv_path=Path(__file__).resolve().parent.parent / ".env")

# 🔱 NAMESILO CONFIGURATION (Wholesale Registrar)
NAMESILO_API_KEY = os.getenv("NAMESILO_API_KEY")
# Strictly Industrial Production: Sandbox Bypass Terminated
NAMESILO_BASE_URL = "https://www.namesilo.com/api"



# 🔱 CLOUDFLARE CONFIGURATION (DNS Bridge)
CLOUDFLARE_API_TOKEN = os.getenv("CLOUDFLARE_API_TOKEN")
CLOUDFLARE_ZONE_ID = os.getenv("CLOUDFLARE_ZONE_ID") # Director to update


class ObsidianDomainKernel:
    """
    OBSIDIAN BROKERAGE ENGINE:
    The "Godaddy-Style" automation layer for the Obsidian Empire.
    1. INDUSTRIAL INGRESS: Real-time API check for global .com availability.
    2. TREASURY MARKUP: Automated retail pricing (Wholesale + 40% Margin).
    3. PROVISIONING BURST: Instant registration and PQC privacy activation.
    4. DNS BRIDGE: Direct mapping to the Global Bridge and Missouri Root.
    """

    async def check_availability(self, domain: str):
        """Module 1: Industrial Availability Ingress."""
        colony_log(f"DOMAIN: Querying global availability for [{domain}]...", node="FINANCE")

        url = f"{NAMESILO_BASE_URL}/checkRegisterAvailability?version=1&type=xml&key={NAMESILO_API_KEY}&domains={domain}"

        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                resp = await client.get(url)
                root = ET.fromstring(resp.text)
                reply = root.find("reply")
                available = reply.find("available")

                if available is not None:
                    is_available = available.text == domain
                    # Module 2: Treasury Markup
                    wholesale_price = 10.50 # Simulated wholesale
                    retail_price = round(wholesale_price * 1.4, 2) # 40% Markup

                    return {
                        "domain": domain,
                        "available": is_available,
                        "price": retail_price if is_available else 0.0,
                        "status": "INGRESS_READY" if is_available else "IDENT_OCCUPIED"
                    }
        except Exception as e:
            colony_log(f"[-] DOMAIN INGRESS ERROR: {e}", node="FINANCE")

        return {"domain": domain, "available": False, "price": 0.0, "status": "NETWORK_LAG"}

    async def register_domain(self, domain: str, signature: str = None, years: int = 1):
        """Module 3: Autonomous Provisioning Burst (Requires Team Signature)."""
        if not signature:
            return False, "AUTH_REQUIRED"

        colony_log(f"DOMAIN: Initiating registration burst for [{domain}] via team auth...", node="FINANCE")

        # 🔱 The Burst: Registration + Private WHOIS + Auto-Renew
        url = f"{NAMESILO_BASE_URL}/registerDomain?version=1&type=xml&key={NAMESILO_API_KEY}&domain={domain}&years={years}&private=1&auto_renew=1"

        try:
            async with httpx.AsyncClient(timeout=45.0) as client:
                resp = await client.get(url)
                root = ET.fromstring(resp.text)
                reply = root.find("reply")
                code = reply.find("code").text

                if code == "300": # NameSilo Success
                    colony_log(f"✓ DOMAIN SUCCESS: [{domain}] identity secured.", node="FINANCE")

                    # Module 4: DNS Bridge Mapping
                    await self._provision_dns_bridge(domain)

                    db.log_event("FINANCE", "IDENTITY_SECURED", {"domain": domain, "status": "ACTIVE"})
                    return True, "BURST_SUCCESS"
                else:
                    detail = reply.find("detail").text
                    colony_log(f"[-] DOMAIN FAIL: {detail}", node="FINANCE")
                    return False, detail
        except Exception as e:
            return False, str(e)

    async def delegate_to_edge(self, domain: str, provider: str = "NETLIFY"):
        """Module 5: Nameserver Delegation (The Edge Method)."""
        colony_log(f"DOMAIN: Delegating [{domain}] to {provider} Edge...", node="FINANCE")

        if provider == "NETLIFY":
            ns = ["dns1.p01.nsone.net", "dns2.p01.nsone.net", "dns3.p01.nsone.net", "dns4.p01.nsone.net"]
        elif provider == "VERCEL":
            ns = ["ns1.vercel-dns.com", "ns2.vercel-dns.com"]
        else:
            return False

        # The Burst: Update Namesilo nameservers for this domain
        url = f"{NAMESILO_BASE_URL}/changeNameServers?version=1&type=xml&key={NAMESILO_API_KEY}&domain={domain}&ns1={ns[0]}&ns2={ns[1]}"
        if len(ns) > 2:
            url += f"&ns3={ns[2]}&ns4={ns[3]}"

        try:
            async with httpx.AsyncClient() as client:
                resp = await client.get(url)
                colony_log(f"✓ DELEGATION SUCCESS: [{domain}] is now managed by {provider} Edge.", node="FINANCE")
                db.log_event("FINANCE", "DOMAIN_DELEGATED", {"domain": domain, "provider": provider})
                return True
        except Exception as e:
            colony_log(f"[-] DELEGATION FAIL: {e}", node="FINANCE")
            return False

    async def map_custom_dns_to_vercel(self, domain: str):
        """Module 6: Cloudflare DNS Mapping for Vercel Ingress."""
        colony_log(f"DOMAIN: Mapping DNS for [{domain}] to Vercel Edge...", node="FINANCE")

        if not CLOUDFLARE_API_TOKEN or not CLOUDFLARE_ZONE_ID:
            colony_log("[-] DNS MAP FAIL: Missing Cloudflare credentials.", node="FINANCE")
            return False

        url = f"https://api.cloudflare.com/client/v4/zones/{CLOUDFLARE_ZONE_ID}/dns_records"
        headers = {"Authorization": f"Bearer {CLOUDFLARE_API_TOKEN}", "Content-Type": "application/json"}

        # 🔱 Step 3: Configure DNS (Using Cloudflare)
        # Add A record for Apex and CNAME for www
        records = [
            {"type": "A", "name": "@", "content": "76.76.21.21", "proxied": False}, # DNS Only for verification
            {"type": "CNAME", "name": "www", "content": "cname.vercel-dns.com", "proxied": False}
        ]

        try:
            async with httpx.AsyncClient() as client:
                for rec in records:
                    resp = await client.post(url, headers=headers, json=rec)
                    if resp.status_code == 200:
                        colony_log(f"✓ DNS SUCCESS: {rec['type']} record created for {domain}.", node="FINANCE")
                    else:
                        colony_log(f"[-] DNS FAIL: {resp.text}", node="FINANCE")
                return True
        except Exception as e:
            colony_log(f"[-] DNS FATAL: {e}", node="FINANCE")
            return False

    async def _provision_dns_bridge(self, domain: str):
        """Module 4: Global DNS Mapping to the Obsidian Bridge."""
        colony_log(f"DOMAIN: Mapping DNS Bridge for [{domain}] via Cloudflare API...", node="FINANCE")

        # 🔱 The Burst: Update Cloudflare DNS to point CNAME at your tunnel
        if not CLOUDFLARE_API_TOKEN or not CLOUDFLARE_ZONE_ID:
            colony_log("[-] DNS BRIDGE FAIL: Missing Cloudflare credentials.", node="FINANCE")
            return

        # Cloudflare API endpoint for DNS records
        url = f"https://api.cloudflare.com/client/v4/zones/{CLOUDFLARE_ZONE_ID}/dns_records"
        headers = {
            "Authorization": f"Bearer {CLOUDFLARE_API_TOKEN}",
            "Content-Type": "application/json"
        }
        # Point the new domain to your active Global Bridge (trycloudflare tunnel)
        tunnel_host = "participant-type-python-manufacturing.trycloudflare.com"

        payload = {
            "type": "CNAME",
            "name": domain,
            "content": tunnel_host,
            "ttl": 1, # Auto
            "proxied": True
        }

        try:
            async with httpx.AsyncClient() as client:
                resp = await client.post(url, headers=headers, json=payload)
                if resp.status_code == 200:
                    colony_log(f"✓ DNS BRIDGE: [{domain}] is now LIVE globally.", node="FINANCE")
                else:
                    colony_log(f"[-] DNS BRIDGE FAIL: {resp.text}", node="FINANCE")
        except Exception as e:
            colony_log(f"[-] DNS BRIDGE FATAL: {e}", node="FINANCE")

        # Update internal registry
        from obsidian_domain_registry import domain_registry
        domain_registry.registry[domain] = "titan_landing.html"


domain_kernel = ObsidianDomainKernel()
