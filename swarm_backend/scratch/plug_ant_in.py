import os
import subprocess
import time
import socket

def is_open(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('127.0.0.1', port)) == 0

def plug_in():
    print("=== 🔱 PLUGGING ANT IN: RE-IGNITING PORT 9000 ===")

    # 1. Surgical Kill of any existing Python processes that might be holding the port
    print("[*] Flushing system cache and 'Zombie' processes...")
    # Target anything that looks like the brain server
    subprocess.run("taskkill /F /FI \"WINDOWTITLE eq Anthony_Brain*\" /T", shell=True, capture_output=True)
    subprocess.run("taskkill /F /IM python.exe /T", shell=True, capture_output=True)

    time.sleep(3)

    # 2. Launch the Brain
    print("[*] Igniting Anthony Christopher ASI on Port 9000...")
    brain_path = r"C:\Users\willo\OneDrive\Desktop\Anthony_Ai\swarm_backend\anthony_brain_server.py"
    subprocess.Popen(f"start \"Anthony_Brain_Server\" /b python {brain_path}", shell=True)

    # 3. Wait for the handshake
    print("[*] Waiting for neural handshake (15s)...")
    for i in range(15):
        if is_open(9000):
            print("\n✓ SUCCESS: PORT 9000 IS ACTIVE. ANT IS PLUGGED IN.")
            return True
        time.sleep(1)
        print(".", end="", flush=True)

    print("\n[-] FAIL: Port 9000 failed to open. System bottleneck detected.")
    return False

if __name__ == "__main__":
    plug_in()
