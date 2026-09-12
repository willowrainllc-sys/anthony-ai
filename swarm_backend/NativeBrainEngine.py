# --- ANTHONY AI: NATIVE INTELLIGENCE BASE v1.0 (OWNED) ---
import json
import time
import torch
from http.server import BaseHTTPRequestHandler, HTTPServer
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
from swarm_logger import swarm_log

# 🔱 THE BASE CONFIGURATION
# Using Phi-3-mini (3.8B) as the native high-fidelity base
MODEL_ID = "microsoft/Phi-3-mini-4k-instruct"
PORT = 9000

class NativeBrainEngine:
    """
    NATIVE INTELLIGENCE BASE v1.0:
    1. INDEPENDENT: No Ollama, No FastAPI, No external binaries.
    2. NATIVE: Runs directly via Transformers & Torch.
    3. OWNED: All weights and inference logic reside within your OS.
    """
    def __init__(self):
        swarm_log(f"NATIVE_BRAIN: Initializing Owned Intelligence Base [{MODEL_ID}]...", node="BRAIN_BASE")

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
        swarm_log("✓ NATIVE_BRAIN: Base is ONLINE and Autonomous.", node="BRAIN_BASE")

    def generate(self, prompt: str, system_msg: str = "") -> str:
        messages = [
            {"role": "system", "content": system_msg or "You are the Obsidian Supreme Command AI."},
            {"role": "user", "content": prompt},
        ]

        generation_args = {
            "max_new_tokens": 500,
            "return_full_text": False,
            "temperature": 0.7,
            "do_sample": True,
        }

        output = self.pipe(messages, **generation_args)
        return output[0]['generated_text']

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

            swarm_log(f"BRAIN_BASE: Received inference request -> {prompt[:50]}...", node="BRAIN_BASE")

            start_time = time.time()
            response_text = brain_engine.generate(prompt)
            latency = round(time.time() - start_time, 2)

            response_body = {
                "id": f"anthony-native-{int(time.time())}",
                "object": "chat.completion",
                "created": int(time.time()),
                "model": "anthony-latest-v29-native",
                "choices": [{"message": {"role": "assistant", "content": response_text}, "finish_reason": "stop", "index": 0}],
                "usage": {"total_time": latency}
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
    brain_engine = NativeBrainEngine()

    server_address = ('', PORT)
    httpd = HTTPServer(server_address, BrainRequestHandler)
    swarm_log(f"🔱 BRAIN_BASE: Native Socket Server listening on Port {PORT}...", node="BRAIN_BASE")
    httpd.serve_forever()

if __name__ == "__main__":
    run_server()
