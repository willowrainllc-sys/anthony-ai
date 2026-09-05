# --- EMPIRE BATCH BOT CREATOR v1.0 ---
import asyncio
import os
import random
import uuid
import httpx
import sqlite3
from swarm_logger import swarm_log

DB_PATH = r"C:\AnthonyAi_Swarm\Empire_Vault.db"
PERSONA_VAULT = r"C:\Users\willo\OneDrive\Desktop\Anthony_Ai\secure_assets\persona_vault"

async def generate_sexy_bot_persona():
    """Generates a high-fidelity 'Alpha' woman persona."""
    prompt = """
    Generate a unique 'Alpha' woman persona for an AI agent.
    Vibe: Sophisticated, attractive, tech-aware, high-authority.
    Specialties: Neural Networks, Quantum Tech, Global Finance, OSINT, or Cyber-Security.
    Style: Minimalist, Cyberpunk, or Haute Couture.

    Return ONLY JSON:
    {
        "name": "Full Name",
        "style": "Style Name",
        "specialty": "Specialty Name",
        "aura": "3, 6, or 9"
    }
    """
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            resp = await client.post("http://localhost:11434/api/generate", json={"model": "anthony-brain:latest", "prompt": prompt, "stream": False})
            if resp.status_code == 200:
                import json
                text = resp.json().get("response", "").strip()
                if "{" in text:
                    text = text[text.find("{"):text.rfind("}")+1]
                return json.loads(text)
    except: pass
    return None

async def create_bots(count=5):
    swarm_log(f"CREATOR: Generating {count} new high-fidelity bots...", node="CREATOR")

    conn = sqlite3.connect(DB_PATH)

    created = 0
    while created < count:
        persona = await generate_sexy_bot_persona()
        if not persona: continue

        bot_id = f"DISCIPLE_{uuid.uuid4().hex[:6].upper()}"

        # 1. Register in DB
        try:
            conn.execute("""
                INSERT INTO neural_disciples (id, name, aura, style, specialty, status, last_active)
                VALUES (?, ?, ?, ?, ?, 'ACTIVE', ?)
            """, (bot_id, persona['name'], persona['aura'], persona['style'], persona['specialty'], 0))
            conn.commit()

            # 2. Create Persona Folder
            bot_folder = os.path.join(PERSONA_VAULT, bot_id)
            os.makedirs(bot_folder, exist_ok=True)

            swarm_log(f"SUCCESS: Created Bot [ {persona['name']} ] - ID: {bot_id}", node="CREATOR")
            created += 1
            await asyncio.sleep(1) # Pacing
        except Exception as e:
            print(f"[-] Failed to create bot: {e}")

    conn.close()
    swarm_log(f"CREATOR: Batch mission complete. {created} bots added to the swarm.", node="CREATOR")

if __name__ == "__main__":
    asyncio.run(create_bots(5))
