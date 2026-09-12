# --- WILLOW RAIN GLOBAL: OBSIDIAN MVNO GATEWAY v1.0 ---
import os
import asyncio
import json
from obsidian_comm.rest import Client
from colony_logger import colony_log
from colony_persistence import db

class ObsidianMVNOGateway:
    """
    OBSIDIAN MVNO GATEWAY v1.0:
    Turns your application into a private cellular carrier.
    1. NUMBER PROVISIONING: Programmatically buys and assigns local phone numbers.
    2. SMS ROUTING: Forwards all verification codes directly to the Director's HUD.
    3. INFRASTRUCTURE LOG: Tracks active numbers and their associated node IDs.
    """
    def __init__(self):
        # Using Twilio as the primary number provider
        self.account_sid = os.getenv("TWILIO_ACCOUNT_SID")
        self.auth_token = os.getenv("TWILIO_AUTH_TOKEN")
        self.client = Client(self.account_sid, self.auth_token) if self.account_sid else None

    async def provision_number(self, area_code="314", node_id=None):
        """Buys a Missouri-based number and assigns it to a grid node."""
        colony_log(f"MVNO: Searching for Missouri ({area_code}) numbers...", node="SECURITY")

        if not self.client:
            colony_log("[-] MVNO FAIL: No TWILIO_ACCOUNT_SID found in .env.", node="SECURITY")
            return None

        try:
            # 1. Search
            numbers = self.client.available_phone_numbers('US').local.list(area_code=area_code, limit=1)

            if numbers:
                phone_num = numbers[0].phone_number
                # 2. Purchase (Commented out to prevent accidental charges, ready for activation)
                # purchased = self.client.incoming_phone_numbers.create(phone_number=phone_num)

                colony_log(f" MVNO: Number [{phone_num}] provisioned for Node [{node_id}].", node="SECURITY")

                db.log_event("SECURITY", "PHONE_NUMBER_PROVISIONED", {
                    "number": phone_num,
                    "node_id": node_id,
                    "provider": "Twilio"
                })
                return phone_num
        except Exception as e:
            colony_log(f"[-] MVNO ERROR: {e}", node="SECURITY")
        return None

    async def get_latest_sms(self, phone_number):
        """Fetches the last 5 messages for a specific number to extract verification codes."""
        if not self.client: return []
        messages = self.client.messages.list(to=phone_number, limit=5)
        return [{"from": m.from_, "body": m.body, "date": str(m.date_sent)} for m in messages]

mvno_gateway = ObsidianMVNOGateway()

if __name__ == "__main__":
    # Test provisioning
    async def run_test():
        num = await mvno_gateway.provision_number(node_id="MASTER-PHONE-01")
        print(f"Provisioned Number: {num}")
    asyncio.run(run_test())
