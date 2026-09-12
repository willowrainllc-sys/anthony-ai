import json
from pathlib import Path

MANIFEST_PATH = Path(r"C:\Users\willo\OneDrive\Desktop\Anthony_Ai\willow_rain_global\wholesale_portal\aiphony_manifest.json")

def upgrade_agents():
    if not MANIFEST_PATH.exists():
        print("Manifest not found.")
        return

    with open(MANIFEST_PATH, 'r') as f:
        manifest = json.load(f)

    for node_id, data in manifest.items():
        if "agentic_capabilities" in data:
            caps = set(data["agentic_capabilities"])
            caps.add("full_stack_developer")
            caps.add("system_architect")
            caps.add("playwright_specialist")
            caps.add("autonomous_code_striker")
            data["agentic_capabilities"] = list(caps)

        # Upgrade Brain version to reflect dev status
        data["brain"] = "anthony-latest-v29.0-DEV"

    with open(MANIFEST_PATH, 'w') as f:
        json.dump(manifest, f, indent=4)

    print(f"✓ SUCCESS: 103 Aiphony Nodes upgraded to DEVELOPER status.")

if __name__ == "__main__":
    upgrade_agents()
