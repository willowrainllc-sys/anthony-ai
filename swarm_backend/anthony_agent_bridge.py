# --- WILLOW RAIN SECURITY: OBSIDIAN AGENT BRIDGE (AUTONOMOUS) v2.0 ---
import os
import time
import subprocess
import json
from pathlib import Path
from swarm_logger import swarm_log
from swarm_persistence import db

# The "Exchange" directory where the LLM writes actions and the bridge writes results
BRIDGE_DIR = Path(r"D:\AnthonyChristopherAi_Swarm\Secure_Assets\agent_bridge")
BRIDGE_DIR.mkdir(parents=True, exist_ok=True)

INPUT_PIPE = BRIDGE_DIR / "llm_actions.txt"
OUTPUT_PIPE = BRIDGE_DIR / "bridge_results.txt"

class AnthonyChristopherAgentBridge:
    """
    OBSIDIAN AGENT BRIDGE v2.0:
    Gives your local Android Studio brain FULL AUTONOMY.
    1. MULTI-TOOL SUPPORT: [EXECUTE], [READ], [WRITE], [TEST], [SYNC].
    2. REAL-TIME FEEDBACK: Writes command results to bridge_results.txt.
    3. TERMINAL IGNITION: Automatically pops open a visible window for critical strikes.
    """
    def run_bridge_loop(self):
        swarm_log("AGENT_BRIDGE: AnthonyChristopher Hands are ARMED. Listening for Brain Signals...", node="SECURITY")

        # Ensure files exist
        for p in [INPUT_PIPE, OUTPUT_PIPE]:
            if not p.exists():
                with open(p, "w") as f: f.write("")

        while True:
            try:
                with open(INPUT_PIPE, "r+") as f:
                    actions = f.readlines()
                    if actions:
                        for action in actions:
                            action = action.strip()
                            if not action: continue

                            swarm_log(f" AGENT_BRIDGE: Processing Brain Signal -> {action[:50]}...", node="SECURITY")
                            result = self._execute_action(action)
                            self._write_result(action, result)

                        # Wipe the input pipe after consumption
                        f.seek(0)
                        f.truncate()
            except Exception as e:
                swarm_log(f"[-] BRIDGE ERROR: {e}", node="SECURITY")
            time.sleep(1)

    def _execute_action(self, action_str: str) -> str:
        try:
            # 1. Parsing the [TOOL] command [/TOOL]
            if "[EXECUTE]" in action_str:
                cmd = action_str.replace("[EXECUTE]", "").replace("[/EXECUTE]", "").strip()
                # Run in a NEW VISIBLE terminal for Director oversight
                subprocess.Popen(f"start cmd /k {cmd}", shell=True)
                return f"COMMAND_DISPATCHED: {cmd}"

            elif "[READ]" in action_str:
                path = action_str.replace("[READ]", "").replace("[/READ]", "").strip()
                with open(path, "r") as rf: return rf.read()

            elif "[WRITE]" in action_str:
                # Expecting format: [WRITE] path | content [/WRITE]
                data = action_str.replace("[WRITE]", "").replace("[/WRITE]", "").split("|")
                with open(data[0].strip(), "w") as wf:
                    wf.write(data[1].strip())
                return f"FILE_WRITTEN: {data[0]}"

            return "ERROR: UNKNOWN_TOOL"
        except Exception as e:
            return f"ERROR: {str(e)}"

    def _write_result(self, action, result):
        with open(OUTPUT_PIPE, "a") as f:
            f.write(f"\n--- RESULT FOR: {action[:30]} ---\n{result}\n")
        db.log_event("SUPREME", "BRIDGE_ACTION_COMPLETED", {"action": action[:50]})

if __name__ == "__main__":
    bridge = AnthonyChristopherAgentBridge()
    bridge.run_bridge_loop()
