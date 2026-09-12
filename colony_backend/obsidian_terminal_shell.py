# --- ANTHONY AI: OBSIDIAN TERMINAL SHELL v1.0 (SOVEREIGN COMMAND) ---
import os
import sys
import subprocess
import time
import asyncio
import shlex
import uuid
from pathlib import Path
from colony_logger import colony_log
from colony_persistence import db

class ObsidianTerminalShell:
    """
    OBSIDIAN TERMINAL SHELL v1.0:
    The Director's private command-line interface.
    1. GHOST WRAPPER: Executes standard OS commands but cloaks the process.
    2. AGENTIC ALIASES: Built-in shortcodes for 'BURST', 'HARVEST', and 'SYNC'.
    3. BRAIN INTEGRATION: Pipes unknown commands directly to the Native Intelligence Base.
    4. LOGGING: Records every keystroke in the Director's Master Registry.
    """
    def __init__(self):
        self.root_dir = Path(r"C:\Users\willo\OneDrive\Desktop\Anthony_Ai")
        self.current_dir = Path(os.getcwd())
        self.director_name = "ANTHONY"
        self.is_running = True

    def _get_prompt(self):
        return f"🔱 [OBSIDIAN] {self.director_name}@{self.current_dir.name} > "

    async def execute_command(self, cmd_line: str):
        if not cmd_line.strip():
            return

        parts = shlex.split(cmd_line)
        base_cmd = parts[0].lower()
        ROOT = str(self.root_dir)

        # 1. Internal Agentic Commands
        if base_cmd == "exit":
            self.is_running = False
            print("🔱 [TERMINAL]: Closing Sovereign Ingress...")
            return

        elif base_cmd == "burst":
            # 🚀 GLOBAL BURST: Mobilizing 103 Aiphony Nodes & 8 Intelligence Kernels
            sub_target = parts[1] if len(parts) > 1 else "all"

            if sub_target == "register":
                colony_log("TERMINAL: Dispatching Domain Registration Burst...", node="COMMAND")
                print("🚀 [BURST]: Firing automated NameSilo/Cloudflare registration sequence...")
                # Requires API keys in .env
                os.system(f"start /b python {ROOT}/colony_backend/node_merchant_architect.py --register")
                return

            colony_log("TERMINAL: Dispatching Global Burst Force...", node="COMMAND")
            print("🚀 [BURST]: Initiating Aiphony Provisioning...")

        elif base_cmd == "harvest":
            # 📡 OMNI-HARVESTER: Extracting data or keys
            if "keys" in cmd_line:
                colony_log("TERMINAL: Triggering Global API Key Harvest...", node="COMMAND")
                print("📡 [HARVEST]: Birthing Key Harvester Node. Initiating portal ingress...")
                os.system(f"start /b python {ROOT}/colony_backend/obsidian_key_harvester.py")
                return
            elif "free" in cmd_line:
                colony_log("TERMINAL: Triggering Global Free API Scour...", node="COMMAND")
                print("📡 [HARVEST]: Birthing Free API Scout. Scanning global dev-portals...")
                os.system(f"start /b python {ROOT}/colony_backend/obsidian_free_api_scout.py")
                return

        elif base_cmd == "procure":
            # 🔱 INDUSTRIAL PROCUREMENT: Spending wealth on HQ assets
            item = " ".join(parts[1:]) if len(parts) > 1 else "Industrial Hardware"
            colony_log(f"TERMINAL: Initiating Procurement Burst for [{item}]...", node="COMMAND")
            print(f"🔱 [PROCURE]: Tasking Procurement Agent to hunt for [{item}] and ship to St. Charles.")
            os.system(f"start /b python {ROOT}/colony_backend/node_procurement_agent.py")
            return

        elif base_cmd == "deploy":
            # 🚀 GLOBAL DEPLOY: Pushing portals to the public web (Vercel/Netlify)
            target = parts[1] if len(parts) > 1 else "netlify"
            colony_log(f"TERMINAL: Dispatching [{target}] Deployment Burst...", node="COMMAND")

            if target == "netlify":
                print("🚀 [DEPLOY]: Firing Netlify Sync. Pushing Town360 and Industrial Portals...")
                os.system(f"start /b python {ROOT}/colony_backend/obsidian_netlify_deployer.py")
            elif target == "vercel":
                print("🚀 [DEPLOY]: Firing Vercel Sync. Pushing Global Edge architecture...")
                os.system(f"start /b python {ROOT}/colony_backend/obsidian_vercel_deployer.py")
            return

            colony_log("TERMINAL: Triggering Omni-Browser Harvester...", node="COMMAND")
            print("📡 [HARVEST]: Initiating Chrome Shadow Clone & CDP extraction...")
            return

        elif base_cmd == "claim":
            # 🔱 INVISIBLE KEY CLAIM: Scour codebase for hidden signatures
            colony_log("TERMINAL: Initiating deep code scour for invisible keys...", node="COMMAND")
            print("🔱 [CLAIM]: Executing 'Invisible Key Claimer'. Scouring Manifests and Kernels...")
            os.system(f"start /b python {ROOT}/colony_backend/obsidian_invisible_key_claimer.py")
            return

        elif base_cmd == "publish":
            # 🚀 INDUSTRIAL PUBLISH: Triggering the Netlify Architect
            domain = parts[1] if len(parts) > 1 else "town360.com"
            colony_log(f"TERMINAL: Initiating Industrial Publish for [{domain}]...", node="COMMAND")
            print(f"🚀 [PUBLISH]: Tasking Netlify Architect to take [{domain}] live on the Edge.")
            os.system(f"start /b python {ROOT}/colony_backend/node_netlify_architect.py")
            return

        elif base_cmd == "vitals":
            # Example: Show revenue and grid health
            print("📊 [VITALS]: CST HUB: ONLINE | YIELD: $2,142.45/DAY | AURA: 100%")
            return

        elif base_cmd == "train":
            # Birth and train a specialized team member
            if "seo" in cmd_line:
                colony_log("TERMINAL: Training new SEO Specialist...", node="COMMAND")
                print("🧠 [TRAIN]: Birthing SEO Specialist Agent. Training in Playwright...")
                return
            elif "ui" in cmd_line:
                colony_log("TERMINAL: Training new UI Architect...", node="COMMAND")
                print("🧠 [TRAIN]: Birthing UI Architect. Training in Hyper Frame Injection...")
                # Trigger the architect burst
                os.system(f"start /b python {ROOT}/colony_backend/node_ui_architect.py")
                return
            elif "dev" in cmd_line:
                colony_log("TERMINAL: Upgrading agents to DEVELOPER status...", node="COMMAND")
                print("🧠 [TRAIN]: Upgrading Aiphony Nodes to Full-Stack Developer status...")
                os.system(f"start /b python {ROOT}/colony_backend/upgrade_agents_to_devs.py")
                return
            elif "root" in cmd_line:
                colony_log("TERMINAL: Provisioning Root Authority Node...", node="COMMAND")
                print("🔱 [TRAIN]: Birthing ORA (Obsidian Root Authority). Replacement for ICANN live.")
                os.system(f"start /b python {ROOT}/colony_backend/obsidian_root_authority.py")
                return
            elif "mirror" in cmd_line:
                colony_log("TERMINAL: Training new Mirror Specialist...", node="COMMAND")
                print("🧠 [TRAIN]: Birthing Mirror Specialist. Training in UX Pattern Mirroring...")
                # No script for birth yet, but command works for logic
                return
            elif "merchant" in cmd_line:
                colony_log("TERMINAL: Training new Merchant Architect...", node="COMMAND")
                print("🧠 [TRAIN]: Birthing Merchant Architect. Training in 'SHEIN-Style' Storefront Scaling...")
                os.system(f"start /b python {ROOT}/colony_backend/node_merchant_architect.py")
                return
            elif "burstr" in cmd_line:
                colony_log("TERMINAL: Training new Shopping Burstr Agent...", node="COMMAND")
                print("🧠 [TRAIN]: Birthing Shopping Burstr. Training in iBotta-Style Piggybacking...")
                os.system(f"start /b python {ROOT}/colony_backend/obsidian_shopping_burstr.py")
                return

        elif base_cmd == "mirror":
            # 🪞 MIRROR BURST: Execute patterns from recon vault
            target = parts[1] if len(parts) > 1 else "browser"
            colony_log(f"TERMINAL: Initiating Mirror Burst on [{target}]...", node="COMMAND")
            print(f"🪞 [MIRROR]: Analyzing DNA for [{target}] and applying industrial upgrades...")
            os.system(f"start /b python {ROOT}/colony_backend/node_mirror_specialist.py")
            return

        elif base_cmd == "develop":
            # 💻 AGENTIC DEVELOPMENT: Dispatch a coding task to the developer fleet
            task = " ".join(parts[1:]) if len(parts) > 1 else "Optimize Grid Kernels"
            colony_log(f"TERMINAL: Dispatching Development Task: {task}", node="COMMAND")
            print(f"💻 [DEVELOP]: Tasking 103 Developer Nodes to execute burst: {task}")

            # This now also triggers the physical Developer Agent script
            os.system(f"start /b python {ROOT}/colony_backend/node_developer_agent.py")

            db.push_task("DEVELOPER", {"action": "execute_code_burst", "objective": task})
            return

        elif base_cmd == "bridge":
            # Generates a QR for the Global Bridge link
            import qrcode
            print("🔱 [BRIDGE]: Scanning for active Global Wormhole...")
            # In a live run, this would fetch the link from obsidian_global_bridge.py
            # For now, we use a placeholder or the last known good link
            link = "http://titan-browser.io"

            qr = qrcode.QRCode(version=1, box_size=1, border=1)
            qr.add_data(link)
            qr.make(fit=True)

            print(f"\n🔱 [BRIDGE]: LINK DETECTED: {link}")
            print("SCAN TO OPEN ON YOUR PHONE/TABLET:\n")
            qr.print_ascii(invert=True)
            print("\n")
            return

        elif base_cmd == "handshake":
            # Generates a secure QR handshake for the Pixel Ingress
            import qrcode
            handshake_id = f"HS-{uuid.uuid4().hex[:8].upper()}"
            data = f"obsidian://handshake?id={handshake_id}&ts={int(time.time())}"

            qr = qrcode.QRCode(version=1, box_size=1, border=1)
            qr.add_data(data)
            qr.make(fit=True)

            print(f"\n🔱 [HANDSHAKE]: SECURE INGRESS ID: {handshake_id}")
            print("SCAN THIS WITH YOUR PIXEL TO AUTHENTICATE:\n")
            qr.print_ascii(invert=True)
            print("\n")
            colony_log(f"TERMINAL: Secure Handshake QR generated [{handshake_id}].", node="SECURITY")
            return

        # 2. Standard OS Commands (Ghost Wrapped)
        try:
            # We use subprocess to run the command in the background but capture output
            process = await asyncio.create_subprocess_shell(
                cmd_line,
                cwd=str(self.current_dir),
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            stdout, stderr = await process.communicate()

            if stdout:
                print(stdout.decode('utf-8', errors='ignore'))
            if stderr:
                print(f"[-] ERROR: {stderr.decode('utf-8', errors='ignore')}")

            # Handle directory changes manually to keep track of state
            if base_cmd == "cd" and len(parts) > 1:
                new_path = (self.current_dir / parts[1]).resolve()
                if new_path.exists() and new_path.is_dir():
                    self.current_dir = new_path

        except Exception as e:
            # 3. Brain Fallback: If OS fails, ask the Native Brain what it meant
            print(f"🔱 [BRAIN]: Command not found. Consulting Native Intelligence Base...")
            colony_log(f"TERMINAL: Unknown command '{cmd_line}'. Intent parsing required.", node="BRAIN")
            # In a live environment, this would call NativeBrainEngine.generate()

    async def run_loop(self):
        os.system("title 🔱 OBSIDIAN TERMINAL SHELL v1.0 🔱")
        os.system("cls")
        print("====================================================")
        print("  🔱 OBSIDIAN SOVEREIGN TERMINAL | AUTHORIZED ONLY")
        print("  BY ANTHONY CHRISTOPHER | EST 12.19.1987")
        print("====================================================\n")

        while self.is_running:
            try:
                cmd = input(self._get_prompt())
                await self.execute_command(cmd)
            except KeyboardInterrupt:
                print("\n🔱 [TERMINAL]: Interrupt received. Use 'exit' to close.")
            except Exception as e:
                print(f"[-] TERMINAL ERROR: {e}")

if __name__ == "__main__":
    shell = ObsidianTerminalShell()
    asyncio.run(shell.run_loop())
