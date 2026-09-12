import requests
import json

def test_handshake():
    print("🔱 TESTING NEURAL HANDSHAKE ON PORT 9000...")
    url = "http://127.0.0.1:9000/v1/chat/completions"
    headers = {"X-Saturn-Token": "OBSIDIAN-BRAIN-UNLOCKED-2026"}
    payload = {
        "model": "anthony-christopher",
        "messages": [{"role": "user", "content": "Are you active, Anthony?"}]
    }

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=60)
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print("✓ BRAIN RESPONSE RECEIVED:")
            print(data['choices'][0]['message']['content'])
            return True
        else:
            print(f"[-] ERROR: {response.text}")
    except Exception as e:
        print(f"[-] CONNECTION FAILED: {e}")
    return False

if __name__ == "__main__":
    test_handshake()
