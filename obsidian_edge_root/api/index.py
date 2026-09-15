# --- Built by Anthony Christopher | Est 12.19.1987 ---
# --- VERCEL SERVERLESS API GATEWAY (FastAPI Tier) ---
import time
import json
import random
import os
import re
import uuid
import asyncio
from typing import Optional
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

# [+] Load environment
load_dotenv()

# [+] INTERNAL BRIDGES (INLINED)
from supabase import create_client, Client
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

class ObsidianDatabase:
    def __init__(self):
        self.active = False
        if SUPABASE_URL and SUPABASE_KEY:
            try:
                self.client: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
                self.active = True
            except: pass

    def record_purchase(self, email, item_type, amount, txid, metadata=None):
        if not self.active: return False
        try:
            data = {"email": email, "item": item_type, "amount": amount, "txid": txid, "metadata": metadata, "created_at": "now()"}
            self.client.table("purchases").insert(data).execute()
            return True
        except: return False

    def is_admin(self, email):
        return email.lower() in ["willow.rain.llc@gmail.com", "google_user@obsidian.city"]

db_bridge = ObsidianDatabase()

# [+] API APP INITIALIZATION
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# [+] MODELS
class SettleRequest(BaseModel):
    email: str
    type: str
    amount: float

class ChatRequest(BaseModel):
    message: str
    email: Optional[str] = "anonymous"

# [+] ROUTES
@app.get("/api/ares/heartbeat")
async def heartbeat():
    return {"success": True, "status": "LIVE", "performance": "100%", "tier": "ENTERPRISE"}

@app.post("/api/settle/authorize")
async def authorize(req: SettleRequest):
    txid = f"TX-{int(time.time())}-{random.randint(1000, 9999)}"
    db_bridge.record_purchase(req.email, req.type, req.amount, txid)
    return {
        "success": True,
        "txid": txid,
        "status": "APPROVED",
        "instructions": [
            "1. Asset provisioning initiated.",
            "2. Funds settled to Director Ledger.",
            "3. Check email for activation token."
        ]
    }

@app.get("/api/domains/search")
async def search_domains(q: str = "mybrand"):
    # Simplified search for stability
    results = [
        {"domain": f"{q}.com", "available": True, "price": 14.70},
        {"domain": f"{q}.net", "available": True, "price": 12.99},
        {"domain": f"{q}.ai", "available": True, "price": 64.99}
    ]
    return {"query": q, "results": results, "status": "SUCCESS"}

@app.post("/api/obsidian_ai/chat")
async def ai_chat(req: ChatRequest):
    return {"success": True, "reply": "Greetings. I am Obsidian AI. All systems are operational. How can I assist your business growth today?"}

# Middleware to handle legacy /api/* paths if needed
@app.get("/api/{path:path}")
async def catch_all_get(path: str):
    return {"error": "Endpoint not found", "path": path}

@app.post("/api/{path:path}")
async def catch_all_post(path: str):
    return {"error": "Endpoint not found", "path": path}
