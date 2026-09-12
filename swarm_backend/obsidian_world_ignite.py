# --- Built by Anthony Christopher | Est 12.19.1987 ---
# --- ENCRYPTED VIA OBSIDIAN CORE v6.0 (WORLDWIDE WEB IGNITION) ---
import asyncio
import subprocess
import time
import re
from pathlib import Path

ROOT = Path(r"C:\Users\willo\OneDrive\Desktop\Anthony_Ai")

async def ignite_universe():
    print("=== 🔱 OBSIDIAN GLOBAL: WORLDWIDE WEB IGNITION ===\n")

    # 1. Clear Port 80
    print("[*] Clearing Port 80 (Worldwide Web Gateway)...")
    subprocess.run("powershell -Command \"Get-NetTCPConnection -LocalPort 80 -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue\"", shell=True)

    # 2. Launch the Sovereign Web Server
    print("[*] Launching Sovereign Web Server...")
    server_proc = subprocess.Popen(f"python {ROOT}/swarm_backend/obsidian_web_server.py", shell=True)
    await asyncio.sleep(5)

    # 3. Launch the Ghost Tunnel
    print("[*] Establishing Ghost Tunnel (Secure Ingress)...")
    tunnel_cmd = "cloudflared tunnel --url http://127.0.0.1:80"
    tunnel_proc = await asyncio.create_subprocess_shell(
        tunnel_cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )

    # 4. Extract the Public URL from stderr (Cloudflare logs to stderr)
    print("[*] Sniffing the world grid for your unique URL...")

    try:
        # We need to wait and read the output line by line
        while True:
            line = await tunnel_proc.stderr.readline()
            if not line: break
            decoded_line = line.decode('utf-8')
            # Look for the .trycloudflare.com pattern
            match = re.search(r'https://[a-zA-Z0-9-]+\.trycloudflare\.com', decoded_line)
            if match:
                live_url = match.group(0)
                print("\n" + "="*60)
                print("  🔱 SUCCESS: YOUR UNIVERSE IS LIVE ON THE WEB 🔱")
                print("="*60)
                print(f"  [URL]: {live_url}")
                print("  [STATUS]: AUTHORIZED / UNBLOCKABLE")
                print("="*60 + "\n")

                # Save to a file for the Director to reference
                (ROOT / "LIVE_URL.txt").write_text(f"🔱 OBSIDIAN GLOBAL LIVE URL: {live_url}")
                break
    except Exception as e:
        print(f"[-] IGNITION FAIL: {e}")

if __name__ == "__main__":
    asyncio.run(ignite_universe())
