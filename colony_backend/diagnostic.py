import sys
import os
from pathlib import Path

# Add backend to path
backend_dir = str(Path(__file__).resolve().parent)
if backend_dir not in sys.path: sys.path.append(backend_dir)
os.chdir(backend_dir)

try:
    print("[*] Testing imports...")
    import nexus_core
    print("[OK] nexus_core imported.")
    import media_renderer
    print("[OK] media_renderer imported.")

    print("[*] Checking for 'instance' or 'isinstance' typos...")
    with open('nexus_core.py', 'r', encoding='utf-8') as f:
        content = f.read()
        if ' instance(' in content:
            print("[!] Found ' instance(' typo in nexus_core.py")
        if 'isinstance(' in content:
            print("[OK] Found 'isinstance(' in nexus_core.py")

    with open('media_renderer.py', 'r', encoding='utf-8') as f:
        content = f.read()
        if ' instance(' in content:
            print("[!] Found ' instance(' typo in media_renderer.py")

    print("[*] All checks complete.")
except Exception as e:
    import traceback
    print(f"[!] DIAGNOSTIC FAILED: {e}")
    traceback.print_exc()
