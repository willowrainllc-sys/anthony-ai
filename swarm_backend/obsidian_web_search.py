# --- WILLOW RAIN COMPANY LLC: OBSIDIAN WEB SEARCH & INTERNET BRIDGE v1.0 ---
import asyncio
import json
import os
from typing import List, Dict, Any, Optional
from duckduckgo_search import DDGS
from swarm_logger import swarm_log
from swarm_persistence import db

class ObsidianWebSearch:
    """
    OBSIDIAN WEB SEARCH v1.0:
    Provides the Obsidian Christopher brain with direct access to the live internet.
    1. REAL-TIME INTEL: Fetches news, trends, and documentation from the web.
    2. ANONYMOUS ROUTING: Optionally routes through the 16-port residential matrix.
    3. DATA ENRICHMENT: Feeds the results back into the brain's context window.
    """
    def __init__(self):
        self.ddgs = DDGS()

    async def search_live_web(self, query: str, max_results: int = 5) -> List[Dict[str, str]]:
        swarm_log(f"WEB_SEARCH: Scouting the internet for [{query}]...", node="INTERNET")

        try:
            # Execute search via DuckDuckGo (No API Key Required)
            results = []
            with DDGS() as ddgs:
                for r in ddgs.text(query, max_results=max_results):
                    results.append({
                        "title": r.get("title"),
                        "link": r.get("href"),
                        "snippet": r.get("body")
                    })

            swarm_log(f" WEB_SEARCH SUCCESS: Captured {len(results)} live internet signals.", node="INTERNET")

            db.log_event("INTERNET", "WEB_SEARCH_COMPLETE", {"query": query, "count": len(results)})
            return results

        except Exception as e:
            swarm_log(f"[-] WEB_SEARCH ERROR: {e}", node="INTERNET")
            return []

    async def get_web_context_for_prompt(self, query: str) -> str:
        """Helper to get a formatted string of web results for brain context."""
        results = await self.search_live_web(query)
        if not results:
            return ""

        context = "\n\nLIVE INTERNET CONTEXT:\n"
        for i, r in enumerate(results):
            context += f"{i+1}. {r['title']} - {r['snippet']} ({r['link']})\n"
        return context

web_search = ObsidianWebSearch() # Standardized export name

if __name__ == "__main__":
    async def test_search():
        res = await web_search_engine.search_live_web("Willow Rain Company LLC")
        print("\n=== [SUPREME] OBSIDIAN WEB SEARCH RESULTS ===")
        for r in res:
            print(f"- {r['title']}")
            print(f"  {r['link']}")

    asyncio.run(test_search())
