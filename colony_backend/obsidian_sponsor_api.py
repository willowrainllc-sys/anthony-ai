# --- OBSIDIAN GLOBAL: SOVEREIGN SPONSOR API v1.0 ---
import random
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Obsidian Sponsor Engine")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

SPONSORS = [
    {"text": "VORTEX GLOBAL: Unlimited 5G Mesh. Claim your sovereignty.", "url": "https://vortex-global.io"},
    {"text": "GHOST VAULT: Your identity is your asset. Liquidate now.", "url": "https://ghost-vault.com"},
    {"text": "BRICK & BITCOIN: Flipping the world in BTC. Pueblo Manor now live.", "url": "https://brick-bitcoin.net"},
    {"text": "SOVEREIGN NODE: Bulletproof .onion hosting. No logs. No middlemen.", "url": "https://sovereign-node.org"},
    {"text": "Maestas Legacy: God, Family, Business. Est 12.19.1987", "url": "https://obsidian-global.io"}
]

@app.get("/v1/next-sponsor")
async def get_sponsor():
    """Returns the next high-aura sponsor message for the ASI Thinking state."""
    return random.choice(SPONSORS)

if __name__ == "__main__":
    import uvicorn
    # Running on Port 8003 to keep Port 9000/8001/8002 clear
    uvicorn.run(app, host="127.0.0.1", port=8003)
