import httpx
import asyncio

async def test():
    proxy = "socks5://127.0.0.1:8000"
    print(f"Testing proxy: {proxy}")
    try:
        # Use httpx.AsyncClient(proxy=...) for single proxy
        async with httpx.AsyncClient(proxy=proxy, timeout=15.0) as client:
            resp = await client.get("https://api.ipify.org?format=json")
            print("SUCCESS:", resp.json())
    except Exception as e:
        print("FAILED:", e)

if __name__ == "__main__":
    asyncio.run(test())
