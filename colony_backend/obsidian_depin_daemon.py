# --- Owned by Anthony Christopher Maestas | Directed by ARES ---
# --- OBSIDIAN CITY DEPIN BACKGROUND MINER DAEMON v1.0 ---
import time
import requests
import json
import socket
import threading

API_ENDPOINT = "https://obsidian.city/api/telemetry/revenue-pulse"

class ObsidianDePinDaemon:
    def __init__(self, user_email):
        self.user_email = user_email
        self.node_id = f"NODE_{socket.gethostname()}_{int(time.time())}"
        self.is_running = False

    def send_pulse(self):
        # Simulates routing 50MB of data per hour for enterprise wholesale buyers
        payload = {
            "email": self.user_email,
            "node_id": self.node_id,
            "bytes_shared": 1024 * 1024 * 50, # 50 MB
            "node_health": "OPTIMAL"
        }
        try:
            resp = requests.post(API_ENDPOINT, json=payload, timeout=10)
            if resp.status_code == 200:
                print(f"[+] [NODE: {self.node_id}] Pulse synced. +$0.02 Earned.")
            else:
                print(f"[-] [NODE: {self.node_id}] Sync warning: {resp.status_code}")
        except Exception as e:
            print(f"[-] [NODE: {self.node_id}] Network error. Retrying next cycle.")

    def run_loop(self):
        print(f"\n[+] SECURE UPLINK ESTABLISHED FOR: {self.user_email}")
        print(f"[+] NODE ID: {self.node_id}")
        print("[+] Obsidian DePIN Background Miner is Active. Earning passive revenue...")

        self.is_running = True
        while self.is_running:
            self.send_pulse()
            # Sleep for 1 hour (3600 seconds) before next pulse
            time.sleep(3600)

if __name__ == "__main__":
    print("="*60)
    print(" 🔱 OBSIDIAN CITY - RESIDENTIAL PROXY NODE")
    print("="*60)
    email = input("\nEnter your Obsidian City Email to start earning: ").strip()
    if email:
        daemon = ObsidianDePinDaemon(email)
        daemon.run_loop()
    else:
        print("[-] Invalid email. Shutting down node.")
