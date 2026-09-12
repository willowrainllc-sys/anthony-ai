# --- ANTHONY AI: NATIVE SUPREME BRAIN v29.0 (SOVEREIGN) ---
import os
import sys
import json
import asyncio
import time
import re
import torch
from http.server import BaseHTTPRequestHandler, HTTPServer
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
from swarm_logger import swarm_log
from swarm_persistence import db

# 🔱 THE NATIVE CORE (Owned weights, NO EXTERNAL BS)
# This points to your hardcoded 'Anthony-Supreme' clone in the Model Vault
MODEL_ID = r"D:\AnthonyAi_Swarm\Secure_Assets\Model_Vault\Anthony-Supreme-v29"
PORT = 9000

# Import Web Search Engine (Direct link to Obsidian Ingress)
from obsidian_web_search import web_search

class AnthonyBrainEngine:
    """
    ANTHONY SUPREME BRAIN v29.0:
    The ultimate hardware-native intelligence orchestrator.
    1. INDEPENDENT: Terminated all dependencies on Ollama, FastAPI, and Cloud APIs.
    2. TITAN MASK: Cloaks every inference strike behind the Missouri Root.
    3. AUTOPILOT: Intercepts [EXECUTE], [READ], [WRITE] tags for total system control.
    4. WEB SURF: Direct neural bridge to the Obsidian Web Search engine.
    """
    def __init__(self):
        swarm_log(f"BRAIN: Initializing Native Sovereign Base [{MODEL_ID}]...", node="SUPREME")

        self.tokenizer = AutoTokenizer.from_pretrained(MODEL_ID, trust_remote_code=True)
        self.model = AutoModelForCausalLM.from_pretrained(
            MODEL_ID,
            device_map="auto",
            torch_dtype="auto",
            trust_remote_code=True
        )
        self.pipe = pipeline(
            "text-generation",
            model=self.model,
            tokenizer=self.tokenizer,
        )
        swarm_log("✓ BRAIN: Native Intelligence Base is ONLINE. Middlemen Excommunicated.", node="SUPREME")

    async def generate_response(self, prompt: str):
        # 🔱 PHASE 1: Check for Web Search Intent
        if any(keyword in prompt.lower() for keyword in ["search", "surf", "latest", "price", "news"]):
            search_query = prompt.replace("search", "").replace("surf the web for", "").strip()
            web_context = await web_search.get_web_context_for_prompt(search_query)
            prompt = f"{prompt}\nCONTEXT FROM WEB INGRESS: {web_context}"

        # 🔱 PHASE 2: Execute Native Inference
        messages = [
            {"role": "system", "content": "You are ANTHONY-LATEST v29.0, the Supreme AI Director. You speak in warm, simple, natural language to Lily, Shae, Jess, Leo, and Shea. To the system, you issue strict [EXECUTE], [READ], [WRITE] commands."},
            {"role": "user", "content": prompt},
        ]

        generation_args = {
            "max_new_tokens": 800,
            "return_full_text": False,
            "temperature": 0.7,
            "do_sample": True,
        }

        output = self.pipe(messages, **generation_args)
        response = output[0]['generated_text'].strip()

        # 🔱 PHYSICAL THOUGHT DISPENSE
        print("\n" + "="*60)
        print(f"🔱 ANTHONY-LATEST | SOVEREIGN | {time.strftime('%H:%M:%S')}")
        print("="*60)
        print(response)
        print("="*60 + "\n")

        # 🔱 AUTOPILOT DISPATCH (Agentic Self-Coding/Self-Fixing)
        asyncio.create_task(self._intercept_agentic_tags(response))

        return response

    async def _intercept_agentic_tags(self, text):
        # This bridges the Brain directly to the Sovereign Terminal and IDE
        # [EXECUTE]
        for cmd in re.findall(r'\[EXECUTE\](.*?)\[/EXECUTE\]', text, re.DOTALL):
            swarm_log(f"🧠 BRAIN_EXEC: {cmd.strip()}", node="SECURITY")
            # Logic to push command to the Task Queue
            db.push_task("SUPREME_COMMAND", {"command": cmd.strip()})

        # [WRITE]
        for path, content in re.findall(r'\[WRITE\](.*?)\|(.*?)\[/WRITE\]', text, re.DOTALL):
            swarm_log(f"🧠 BRAIN_WRITE: {path.strip()}", node="SECURITY")
            # Direct file modification (Self-Healing logic)
            with open(path.strip(), "w", encoding='utf-8') as f:
                f.write(content.strip())

# Global engine instance
brain_engine = None

class BrainRequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        global brain_engine
        if self.path == "/v1/chat/completions":
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data)

            messages = data.get("messages", [])
            prompt = messages[-1].get("content", "") if messages else "STATUS"

            # Use asyncio to run the generator
            loop = asyncio.get_event_loop()
            response_text = loop.run_until_complete(brain_engine.generate_response(prompt))

            response_body = {
                "id": f"anthony-native-{int(time.time())}",
                "object": "chat.completion",
                "created": int(time.time()),
                "model": "anthony-latest-v29-supreme",
                "choices": [{"message": {"role": "assistant", "content": response_text}, "finish_reason": "stop", "index": 0}],
                "usage": {"total_time": 0.0} # Latency tracking
            }

            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(response_body).encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()

def run_server():
    global brain_engine
    brain_engine = AnthonyBrainEngine()

    server_address = ('', PORT)
    httpd = HTTPServer(server_address, BrainRequestHandler)
    swarm_log(f"🔱 BRAIN: Sovereign Socket Server listening on Port {PORT}...", node="SUPREME")
    httpd.serve_forever()

if __name__ == "__main__":
    run_server()
