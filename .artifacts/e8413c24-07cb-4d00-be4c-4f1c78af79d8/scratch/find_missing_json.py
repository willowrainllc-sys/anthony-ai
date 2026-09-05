import os
import re

backend_dir = r"C:\Users\willo\OneDrive\Desktop\Anthony_Ai\swarm_backend"
files = [f for f in os.listdir(backend_dir) if f.endswith(".py")]

for f in files:
    path = os.path.join(backend_dir, f)
    with open(path, "r", encoding="utf-8", errors="ignore") as file:
        content = file.read()
        if "json." in content and "import json" not in content:
            print(f"MISSING IMPORT: {f}")
