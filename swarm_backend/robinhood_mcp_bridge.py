# --- EMPIRE ROBINHOOD MCP & TRADING BRIDGE v3.5 (REAL-WORLD EXECUTION) ---
import os
import sys
import json
import time
import base64
import uuid
import hmac
import hashlib
import asyncio
import httpx
from cryptography.hazmat.primitives.asymmetric import ed25519
from pathlib import Path
from swarm_logger import swarm_log
from swarm_persistence import db
from dotenv import load_dotenv

load_dotenv(dotenv_path=Path(__file__).resolve().parent.parent / ".env")

API_KEY_ID = os.getenv("ROBINHOOD_API_KEY")
PEM_PATH = Path(r"C:\Users\willo\OneDrive\Desktop\Anthony_Ai\swarm_vault\robinhood_private.pem")

class RobinhoodCloudAPI:
    """
    OFFICIAL ROBINHOOD CRYPTO TRADING API v1.2:
    Handles Ed25519 signing and REAL-WORLD order submission.
    """
    def __init__(self):
        self.api_key_id = API_KEY_ID
        self.base_url = "https://trading.robinhood.com"
        self._load_key()

    def _load_key(self):
        if not PEM_PATH.exists():
            self.private_key = None
            return
        with open(PEM_PATH, "rb") as f:
            raw_key = f.read().decode('utf-8')
            b64_content = "".join(raw_key.split('\n')[1:-2])
            key_bytes = base64.b64decode(b64_content)
            # Standard ed25519 32-byte seed extraction from OpenSSH PEM
            self.private_key = ed25519.Ed25519PrivateKey.from_private_bytes(key_bytes[-32:])

    def _get_signature(self, method, path, body, timestamp):
        # Format: API_KEY + TIMESTAMP + PATH + METHOD + BODY
        message = f"{self.api_key_id}{timestamp}{path}{method}{body}"
        signature = self.private_key.sign(message.encode('utf-8'))
        return base64.b64encode(signature).decode('utf-8')

    async def request(self, method: str, path: str, body_dict: dict = None):
        if not self.private_key:
            return None

        timestamp = str(int(time.time()))
        body_json = json.dumps(body_dict) if body_dict else ""

        headers = {
            "x-api-key": self.api_key_id,
            "x-signature": self._get_signature(method, path, body_json, timestamp),
            "x-timestamp": timestamp,
            "Content-Type": "application/json"
        }

        async with httpx.AsyncClient(timeout=30.0) as client:
            url = f"{self.base_url}{path}"
            if method == "GET":
                return await client.get(url, headers=headers)
            else:
                return await client.post(url, headers=headers, content=body_json)

class RobinhoodMcpBridge:
    def __init__(self):
        self.api = RobinhoodCloudAPI()
        self.is_real = bool(self.api.private_key)
        self.stop_loss_pct = 1.0

    async def get_portfolio_summary(self) -> dict:
        swarm_log("ROBINHOOD_MCP: Fetching real-world balance...", node="ROBINHOOD")

        from robinhood_browser_bot import robinhood_bot
        check = await robinhood_bot.get_real_status()

        if check.get("status") == "SESSION_ACTIVE":
            # Convert scraped strings like "$25.98" to float
            def to_float(val):
                try: return float(val.replace('$', '').replace(',', ''))
                except: return 0.0

            return {
                "status": "REAL_WORLD_ACTIVE",
                "portfolio_value_usd": to_float(check.get("portfolio", "0.00")),
                "buying_power_usd": to_float(check.get("buying_power", "0.00")),
                "connection": "GHOST_VERIFIED"
            }
        return {"status": "ERROR", "message": check.get("message", "Session Inactive")}

    async def execute_algorithmic_trade(self, symbol: str, action: str, amount_usd: float) -> dict:
        """EXECUTES A REAL-WORLD GHOST TRADE. NO SIMULATION."""
        swarm_log(f"ROBINHOOD_MCP: Executing real {action} on [{symbol}] for ${amount_usd} (Ghost Mode)...", node="ROBINHOOD")

        from robinhood_browser_bot import robinhood_bot
        res = await robinhood_bot.execute_real_trade(symbol, action, amount_usd)

        if res.get("status") == "SUCCESS":
            swarm_log(f" ROBINHOOD SUCCESS: Real order filled for [{symbol}].", node="ROBINHOOD")
            return res
        else:
            swarm_log(f"[-] ROBINHOOD ERROR: {res.get('message', res.get('reason'))}", node="ROBINHOOD")
            return res

robinhood_bridge = RobinhoodMcpBridge()
