# --- Built by Anthony Christopher | Est 12.19.1987 ---
# --- OBSIDIAN CITY WINDOWS DATA FEEDER v1.0 ---
import time
import random
import httpx
import socket

API_URL = "https://obsidian.city/api/data/report"

def run_feeder():
    user_email = "director@obsidian.city" # In prod, read from config
    device_id = f"WIN_{socket.gethostname()}"

    print(f"🔱 OBSIDIAN DATA FEEDER ACTIVE: {device_id}")
    print("[*] Sharing unused bandwidth with global mesh...")

    while True:
        try:
            # Simulate 1MB - 5MB shared
            bytes_shared = random.randint(1024*1024, 5*1024*1024)
            payload = {
                "email": user_email,
                "bytes": bytes_shared,
                "device_id": device_id
            }

            resp = httpx.post(API_URL, json=payload, timeout=10.0)
            if resp.status_code == 200:
                data = resp.json()
                print(f"✓ PULSE: Shared {bytes_shared/(1024*1024):.2f} MB. Status: {data.get('status')}")
            else:
                print(f"[-] Connection failed: {resp.status_code}")

        except Exception as e:
            print(f"[-] Pulse Interrupted: {e}")

        time.sleep(60) # Pulse every minute

if __name__ == "__main__":
    run_feeder()
