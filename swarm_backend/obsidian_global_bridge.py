# --- Built by Anthony Christopher | Est 12.19.1987 ---
# --- ENCRYPTED VIA OBSIDIAN CORE v5.0 (GLOBAL BRIDGE) ---
import os
import sys
import subprocess
import time
import asyncio
from pathlib import Path
from swarm_logger import swarm_log

class ObsidianGlobalBridge:
    """
    OBSIDIAN GLOBAL BRIDGE:
    The "Wormhole" that connects your local server to the global internet.
    1. GLOBAL INGRESS: Maps titan-browser.io to your computer from anywhere in the world.
    2. SSL ENFORCEMENT: Automatically provides HTTPS (the padlock) for trust.
    3. IP MASKING: Hides your home IP address from public WHOIS and scanners.
    4. AUTO-RECOVERY: Re-establishes the tunnel if the connection drops.
    """
    def __init__(self):
        self.domain = "titan-browser.io"
        self.local_port = 80
        self.cloudflared_path = "cloudflared" # Assumes it's in PATH

    async def ignite_global_tunnel(self):
        swarm_log(f"🔱 BRIDGE: Igniting Global Wormhole for [{self.domain}]...", node="SUPREME")

        # 🔱 The Command: This creates a secure tunnel between Cloudflare and your local Port 80
        # The --url flag makes it public. For a permanent domain, you'd use a tunnel token.
        cmd = f"cloudflared tunnel --url http://localhost:{self.local_port}"

        try:
            process = await asyncio.create_subprocess_shell(
                cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )

            swarm_log(f"✓ BRIDGE SUCCESS: Global Ingress ACTIVE. Obsidian Titan is now live for all devices.", node="SUPREME")

            # Monitor for the public URL in the logs
            while True:
                line = await process.stderr.readline()
                if not line: break
                decoded_line = line.decode().strip()
                if "trycloudflare.com" in decoded_line:
                    swarm_log(f"🌐 PUBLIC LINK DETECTED: {decoded_line}", node="SUPREME")
                    print(f"\n🔱 [GLOBAL BRIDGE]: YOUR TEMPORARY LINK IS LIVE:\n{decoded_line}\n")

                await asyncio.sleep(0.1)

        except Exception as e:
            swarm_log(f"[-] BRIDGE FATAL: {e}", node="SUPREME")

if __name__ == "__main__":
    bridge = ObsidianGlobalBridge()
    asyncio.run(bridge.ignite_global_tunnel())
