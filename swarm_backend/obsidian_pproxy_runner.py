# --- WILLOW RAIN SECURITY: OBSIDIAN PPROXY RUNNER v30.0 (IMMORTAL MATRIX) ---
import subprocess
import time
import os
import sys
import socket
from swarm_logger import swarm_log
from obsidian_daemon_base import ObsidianDaemon

class ObsidianPProxyRunner(ObsidianDaemon):
    """
    PPROXY RUNNER v30.0:
    The "Never-Kill" Network Gateway.
    1. UNIQUE TITLE: Window is titled 'OBSIDIAN_MATRIX' for surgical process management.
    2. SINGLE PROCESS: Handles all 100+ ports in a single, stable CLI instance.
    3. AUTO-HEAL: Re-ignites if the Master Port (8000) or Swarm Ports (1080+) are blocked.
    """
    def __init__(self):
        super().__init__("PPROXY_RUNNER")
        self.master_port = 8000
        self.swarm_start = 1080
        self.swarm_end = 1130 # Lean 50-port range for RAM safety

    def _is_port_open(self, port: int) -> bool:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(0.5)
            return s.connect_ex(('127.0.0.1', port)) == 0

    def run_matrix(self):
        swarm_log("PPROXY_v30: Checking Matrix Integrity...", node="NETWORK")

        while True:
            # Only start if the master port is closed
            if not self._is_port_open(self.master_port):
                swarm_log("[-] PPROXY: Port 8000 CLOSED. Re-igniting Obsidian Matrix...", node="NETWORK")
                self._spawn_matrix()

            self.send_heartbeat(status="ROUTING")
            time.sleep(60)

    def _spawn_matrix(self):
        # 1. Surgical Kill (Only kill previous matrix, not all python)
        os.system('taskkill /F /FI "WINDOWTITLE eq OBSIDIAN_MATRIX" /T >nul 2>&1')
        time.sleep(1)

        # 2. Build the giant listener string
        listeners = [f"-l socks5://0.0.0.0:{self.master_port}"]
        for port in range(self.swarm_start, self.swarm_end + 1):
            listeners.append(f"-l socks5://0.0.0.0:{port}")

        full_cmd = f"python -m pproxy {' '.join(listeners)}"

        # 3. Launch with unique title and physical log ingress for Sigint Interceptor
        log_file = r"C:\AnthonyAi_Swarm\Logs\matrix_ingress.log"
        os.makedirs(os.path.dirname(log_file), exist_ok=True)

        try:
            # We use 'title' command to name the window for identification
            # pproxy -vv shows all packet data for the Sigint Interceptor
            cmd = f'start "OBSIDIAN_MATRIX" /b python -m pproxy -vv {" ".join(listeners)} > {log_file} 2>&1'
            subprocess.Popen(cmd, shell=True)
            swarm_log(f" PPROXY SUCCESS: Matrix re-ignited with {len(listeners)} ports. Logging to [{log_file}]", node="NETWORK")
        except Exception as e:
            swarm_log(f" PPROXY FATAL: {e}", node="NETWORK")

if __name__ == "__main__":
    runner = ObsidianPProxyRunner()
    runner.run_matrix()
