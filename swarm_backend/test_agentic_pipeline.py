# --- EMPIRE END-TO-END TEST: AGENTIC PRODUCTION PIPELINE v3.1 ---
import asyncio
import os
import json
import time
from pathlib import Path
from swarm_logger import swarm_log
from viral_idea_engine import idea_engine
from theme_engine import theme_engine
from node_showrunner import showrunner
from node_quality_control import qa_agent
from media_renderer import create_reel_package

async def run_end_to_end_test():
    print("--- 🔱 STARTING AGENTIC PIPELINE END-TO-END TEST (COLOR-GUARD) ---")

    # 1. ORIGINAL CONCEPT (Blockbuster Engine)
    print("[*] Phase 1: Inventing Original Concept...")
    concept = await idea_engine.generate_original_concept()
    print(f"[✓] Concept Invented: {concept['title']}")

    # 2. SHOWRUNNER ARCHITECT (Manifest & Bible)
    print("[*] Phase 2: Showrunner architecting manifest...")
    strategy = {
        "concept_title": concept['title'],
        "niche": concept.get('niche', 'Viral Strategy'),
        "strategy": "PROVEN"
    }
    manifest = await showrunner.build_comprehensive_manifest(strategy)

    if not manifest:
        print("[!] Showrunner failed.")
        return
    print(f"[✓] Manifest Locked. Format: {manifest['format']} Scenes: {len(manifest['scenes'])}")

    # 3. QA EVALUATION (Pre-Production)
    print("[*] Phase 3: Pre-Production QA Check...")
    qa_check = await qa_agent.evaluate_production_plan(manifest)
    print(f"[✓] QA Status: {qa_check['status']}")

    # 4. BLOCKBUSTER PRODUCTION (Assembly & Color Guard)
    print("[*] Phase 4: Launching Media Renderer...")
    # Map bible style to psy_mode
    style = manifest['bible']['metadata']['style']
    filename = await create_reel_package(
        topic_title=concept['title'],
        body_text=json.dumps(manifest),
        psy_mode=style
    )

    if filename:
        local_path = Path(r"C:\AnthonyAi_Swarm\Renderings") / filename
        print(f"[✓] Render Complete: {filename}")

        # 5. TECHNICAL VERIFICATION (Pixel Analysis for Color Casts)
        print("[*] Phase 5: Running Pixel-Level Color Guard Scan...")
        passed, reason = await qa_agent.verify_final_asset(str(local_path))
        if passed:
            print(f"--- 🔱 TEST SUCCESS: AGENTIC PIPELINE FULLY OPERATIONAL ---")
            print(f"PAYLOAD: {local_path}")
            print(f"QUALITY PASS: {reason}")
        else:
            print(f"[!] QA REJECTION: {reason}")
    else:
        print("[!] Production Agent failed.")

if __name__ == "__main__":
    asyncio.run(run_end_to_end_test())
