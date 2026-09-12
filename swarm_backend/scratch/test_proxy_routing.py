import requests
import sys

def test():
    proxy = 'socks5://127.0.0.1:1080'
    proxies = {'http': proxy, 'https': proxy}
    print(f"Testing route via {proxy}...")
    try:
        r = requests.get('https://api.ipify.org?format=json', proxies=proxies, timeout=15)
        print(f"✓ PROXY_LIVE: {r.json()}")
        return True
    except Exception as e:
        print(f"[-] PROXY_DEAD: {e}")
        return False

if __name__ == "__main__":
    test()
