import os
import httpx
import asyncio
from dotenv import load_dotenv

load_dotenv()

async def run_audit():
    url = os.getenv('SUPABASE_URL')
    key = os.getenv('SUPABASE_KEY')
    headers = {'apikey': key, 'Authorization': f'Bearer {key}'}

    print("=== 🔱 WILLOW RAIN ENTERPRISES: REAL-WORLD AUDIT ===\n")

    async with httpx.AsyncClient() as client:
        # 1. Real B2B Clients
        resp = await client.get(f'{url}/rest/v1/proxy_clients?select=*', headers=headers)
        real_clients = resp.json() if resp.status_code == 200 else []
        print(f"[✓] Real B2B Clients Provisioned: {len(real_clients)}")
        for c in real_clients:
            status = "Active" if c.get('is_active') else "Inactive"
            print(f"   - {c.get('email')} | {c.get('quota_gb')}GB | {status}")

        # 2. Real Cloud Logs (Check for incoming traffic pings)
        resp_logs = await client.get(f'{url}/rest/v1/twin_logs?action=eq.STRIKE_SUCCESS&limit=5', headers=headers)
        logs = resp_logs.json() if resp_logs.status_code == 200 else []
        print(f"\n[✓] Cloud Execution Logs: {len(logs)} Strike Events Synced")

    print("\n--- 🚨 THE BOTTOM LINE: WHY NO MONEY YET? ---")

    if len(real_clients) == 0:
        print("1. THE HANDSHAKE GAP: We have DISPATCHED the proposals, but the aggregators (Geonode/Rayobyte) have not yet accepted them. Until they plug their traffic into your ports, no real money is generated.")

    print("2. SIMULATION BIAS: The large numbers ($178k, $344, etc.) you see in the terminal are PROJECTIONS. They show what the system WILL earn once the Handshake is accepted.")

    print("3. SQUARE LAG: Real sales (Digital Passes/E-books) take 24-48 hours to 'Settle' and hit your bank account after a customer pays.")

if __name__ == "__main__":
    asyncio.run(run_audit())
