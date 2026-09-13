# --- Built by Anthony Christopher | Est 12.19.1987 ---
# --- DOMAIN RESELLER API TEST v1.0 ---
import os
import httpx
import xml.etree.ElementTree as ET
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(dotenv_path=Path(__file__).resolve().parent.parent / ".env")

NAMESILO_KEY = os.getenv("NAMESILO_API_KEY")
# Using Sandbox URL for testing to avoid charging real funds
BASE_URL = "https://www.namesilo.com/api"

async def test_namesilo_handshake():
    print(f"🔱 TESTING NAMESILO HANDSHAKE: Key [{NAMESILO_KEY[:10]}...]")

    # Simple check for account balance or status
    url = f"{BASE_URL}/getAccountBalance?version=1&type=xml&key={NAMESILO_KEY}"

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.get(url)
            print(f"[*] Response Status: {resp.status_code}")

            root = ET.fromstring(resp.text)
            reply = root.find("reply")
            code = reply.find("code").text
            detail = reply.find("detail").text

            if code == "300":
                balance = reply.find("balance").text
                print(f"✓ HANDSHAKE SUCCESS: Account Balance: ${balance}")
                return True
            else:
                print(f"[-] HANDSHAKE FAIL: Code {code} - {detail}")
                if "invalid" in detail.lower() or "sandbox" in detail.lower():
                    print("    Note: Prefix 'cert_' requires NameSilo Sandbox Mode.")
                return False
    except Exception as e:
        print(f"[-] CRITICAL ERROR: {e}")
        return False

if __name__ == "__main__":
    import asyncio
    asyncio.run(test_namesilo_handshake())
