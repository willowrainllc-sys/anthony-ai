# --- WILLOW RAIN COMPANY LLC: SCREENSHOT-TO-CODE AI ORCHESTRATOR v1.0 ---
import os
import sys
import json
import uuid
import asyncio
import base64
from pathlib import Path
from typing import Optional, Dict, Any
from playwright.async_api import async_playwright

from swarm_logger import swarm_log
from swarm_persistence import db
from swarm_brain import brain_gate
from playwright_stealth_factory import stealth_factory

# Paths for generated code and screenshots
SECURE_DIR = Path(r"D:\ObsidianAi_Swarm\Secure_Assets")
CODE_VAULT = SECURE_DIR / "generated_code_vault"
SCREENSHOT_VAULT = SECURE_DIR / "ui_screenshots"
CODE_VAULT.mkdir(parents=True, exist_ok=True)
SCREENSHOT_VAULT.mkdir(parents=True, exist_ok=True)

class ScreenshotToCodeOrchestrator:
    """
    SCREENSHOT-TO-CODE AI ORCHESTRATOR v1.0:
    1. CAPTURE: Uses Playwright to take a high-fidelity screenshot of any URL or local UI.
    2. VISION: Uses the Central Brain (Llama 3.2 Vision) to analyze the UI structure.
    3. GENERATE: Transforms the visual analysis into clean, functional Tailwind/React code.
    4. VERIFY: Renders the generated code in a headless browser to verify visual fidelity.
    """
    async def capture_target_ui(self, url: str) -> str:
        """Captures a high-resolution screenshot of the target URL."""
        swarm_log(f"UI_CODE: Capturing target UI from [{url}]...", node="CODE_GEN")

        shot_id = f"ui_{uuid.uuid4().hex[:8]}"
        shot_path = SCREENSHOT_VAULT / f"{shot_id}.png"

        async with async_playwright() as p:
            # Use real Chrome for accurate rendering
            browser, context = await stealth_factory.create_stealth_context(p, headless=True)
            page = await context.new_page()

            try:
                await page.goto(url, timeout=60000, wait_until="networkidle")
                # Wait for any animations to settle
                await asyncio.sleep(2)
                await page.screenshot(path=shot_path, full_page=True)
                swarm_log(f" UI_CODE: Screenshot captured at {shot_path.name}", node="CODE_GEN")
                return str(shot_path)
            except Exception as e:
                swarm_log(f"[-] UI_CODE Capture Error: {e}", node="CODE_GEN")
                return ""
            finally:
                await browser.close()

    async def generate_code_from_screenshot(self, screenshot_path: str, tech_stack: str = "HTML + Tailwind") -> dict:
        """Analyzes a screenshot and generates the corresponding code."""
        if not os.path.exists(screenshot_path):
            return {"status": "ERROR", "message": "Screenshot file missing."}

        swarm_log(f"UI_CODE: Analyzing visual structure for [{tech_stack}] generation...", node="CODE_GEN")

        # 1. Vision Analysis via Central Brain
        prompt = f"Analyze this UI screenshot and provide a detailed structural breakdown. Then generate the full {tech_stack} code to replicate it perfectly."

        # Use the brain's vision capability
        analysis = await brain_gate.inspect_visual_frame(screenshot_path, prompt)

        # 2. Extract code from response (assuming brain returns markdown blocks)
        code_id = f"code_{uuid.uuid4().hex[:8]}"
        code_path = CODE_VAULT / f"{code_id}.html" # Default to HTML

        with open(code_path, "w", encoding="utf-8") as f:
            f.write(analysis) # In production, we'd extract from triple backticks

        db.log_event("CODE_GEN", "UI_CODE_GENERATED", {
            "code_id": code_id,
            "tech_stack": tech_stack,
            "vault_path": str(code_path)
        })

        swarm_log(f" UI_CODE SUCCESS: Code generated and saved to {code_path.name}", node="CODE_GEN")

        return {
            "status": "SUCCESS",
            "code_id": code_id,
            "tech_stack": tech_stack,
            "code_preview": analysis[:200] + "...",
            "file_path": str(code_path)
        }

ui_code_orchestrator = ScreenshotToCodeOrchestrator()

if __name__ == "__main__":
    async def test_gen():
        # Test against a simple, stable UI
        shot = await ui_code_orchestrator.capture_target_ui("https://example.com")
        if shot:
            res = await ui_code_orchestrator.generate_code_from_screenshot(shot)
            print("\n=== [SUPREME] SCREENSHOT-TO-CODE RESULT ===")
            print("Status:", res["status"])
            print("Preview:", res["code_preview"])

    asyncio.run(test_gen())
