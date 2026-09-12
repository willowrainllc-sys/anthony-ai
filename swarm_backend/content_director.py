# --- EMPIRE CONTENT DIRECTOR: MISSION SPECTRUM ORCHESTRATOR v2.4 (SELF-LEARNING) ---
import asyncio
import json
import random
import time
from pathlib import Path
from swarm_logger import swarm_log
from swarm_persistence import db
from swarm_brain import brain_gate
from director_score_engine import director_engine
from trend_engine import trend_engine
from metadata_engine import metadata_engine

class ContentDirector:
    """
    ULTIMATE INTELLIGENCE LAYER: High-Retention Mini-Doc Orchestrator.
    v2.4: Implements Full Self-Learning Loop using Analytics Memory.
    """
    def __init__(self):
        self.active_pages = ["ANTHONY_AI_OFFICIAL", "ACM_ENTERTAINMENT", "OBSIDIAN_GRID"]

    async def run_autopilot_cycle(self):
        page_id = random.choice(self.active_pages)
        swarm_log(f"DIRECTOR: Starting Intelligent cycle for [{page_id}]", node="DIRECTOR")

        # 1. FETCH PAGE PROFILE & ANALYTICS WINS
        profile = await self._get_or_create_profile(page_id)
        analytics_memory = await self._get_performance_summary(page_id)

        # 2. TREND DISCOVERY
        spark = await trend_engine.get_fresh_creative_spark()

        # 3. IDEATION (Data-Aware)
        # We tell the brain what worked last time so it can replicate success.
        prompt = f"""
        You are the Showrunner for [{page_id}].
        NICHE: {profile['niche']}
        PAST WINS: {analytics_memory}
        TRENDING SPARK: {spark['subject']}

        TASK: Architect a 1-5 minute cinematic documentary concept.
        Use the 'Past Wins' to double down on what works (e.g. mystery, high-stakes, macro shots).
        Format: JSON with 'concept', 'pacing_strategy', 'retention_goal'.
        """
        idea_res = await brain_gate.generate_serialized(prompt, format="json", complexity="medium")
        try:
            idea = json.loads(idea_res)
            if isinstance(idea, list) and len(idea) > 0:
                idea = idea[0]
            if not isinstance(idea, dict):
                raise ValueError("Idea is not a dictionary")
        except:
            idea = {"concept": spark['subject'], "pacing_strategy": "Fast-paced cinematic"}

        # 4. SCENE PRODUCTION (Master Design v2.1)
        production_plan = await director_engine.build_high_retention_mini_doc(idea['concept'])

        # 5. METADATA OPTIMIZATION
        optimized = await metadata_engine.optimize_for_grid(
            script_body=production_plan.get('description', ''),
            niche=profile['niche'],
            original_title=production_plan.get('title')
        )

        # 6. FINAL ASSEMBLY
        production_plan['title'] = optimized.get('title', production_plan.get('title', 'Obsidian Strike'))
        production_plan['hashtags'] = optimized.get('hashtags', "#Obsidian #Cinema")
        production_plan['page_id'] = page_id
        production_plan['niche'] = profile['niche']

        return production_plan

    async def _get_or_create_profile(self, page_id: str):
        with db._get_connection() as conn:
            row = conn.execute("SELECT * FROM content_profiles WHERE page_id=?", (page_id,)).fetchone()
            if row:
                return {"page_id": row[0], "niche": row[1], "audience": row[2], "voice": row[3]}

        default_niche = "High-Fidelity AI Cinema"
        with db._get_connection() as conn:
            conn.execute("INSERT OR IGNORE INTO content_profiles (page_id, niche, brand_voice) VALUES (?, ?, ?)", (page_id, default_niche, "Cinematic"))
            conn.commit()
        return {"page_id": page_id, "niche": default_niche, "voice": "Cinematic"}

    async def _get_performance_summary(self, page_id: str):
        """Extracts the 'Winning Patterns' from historical analytics."""
        try:
            with db._get_connection() as conn:
                # Find the top 3 best performing titles/topics for this page
                rows = conn.execute("""
                    SELECT metadata, views FROM empire_events
                    JOIN performance_analytics ON empire_events.metadata LIKE '%' || performance_analytics.job_id || '%'
                    WHERE empire_events.node=? AND event_type='STRIKE_SUCCESS'
                    ORDER BY views DESC LIMIT 3
                """, (page_id,)).fetchall()

                if not rows: return "No analytics yet. Focus on pattern-interruption hooks."

                wins = []
                for r in rows:
                    try:
                        meta = json.loads(r[0])
                        if isinstance(meta, dict):
                            wins.append(f"Title: {meta.get('title', 'Unknown')} ({r[1]} views)")
                    except: continue

                if not wins: return "Focus on pattern-interruption hooks."
                return "Recent High Performers: " + " | ".join(wins)
        except:
            return "Focus on cinematic mystery and high-contrast visuals."

    async def run_autonomous_social_loop(self):
        """
        AGENTIC DAEMON UPGRADE:
        Runs continuously in the background, architecting high-retention cinematic content
        using real analytics feedback, and triggering the production line.
        """
        swarm_log("AGENTIC DAEMON: Content Director loop activated. Feeding social hubs...", node="AGENTIC_DAEMON")

        while True:
            try:
                swarm_log(f"AGENTIC DAEMON: Initiating Full Autopilot Production Cycle...", node="AGENTIC_DAEMON")

                # Run the full intelligent cycle
                production_plan = await self.run_autopilot_cycle()

                swarm_log(f"AGENTIC DAEMON: Production Plan Generated: {production_plan.get('title')}", node="AGENTIC_DAEMON")
                db.log_event("CONTENT_DIRECTOR", "AUTONOMOUS_POST_CREATED", {"title": production_plan.get('title'), "page": production_plan.get('page_id')})

                # (In a real system, you would pass `production_plan` to your video renderer here)
                # Example: await video_engine.render(production_plan)

            except Exception as e:
                swarm_log(f"[-] AGENTIC DAEMON ERROR in Content Loop: {e}. Self-healing and continuing...", node="AGENTIC_DAEMON")

            # Wait a few hours before the next autonomous post (simulated here as 4-8 hours)
            sleep_time = random.uniform(3600 * 4, 3600 * 8)
            swarm_log(f"AGENTIC DAEMON: Content Director resting. Next production cycle in {sleep_time/3600:.1f} hours.", node="AGENTIC_DAEMON")
            await asyncio.sleep(sleep_time)

director = ContentDirector()

if __name__ == "__main__":
    import sys
    mode = sys.argv[1] if len(sys.argv) > 1 else "daemon"
    if mode == "daemon":
        asyncio.run(director.run_autonomous_social_loop())
    else:
        asyncio.run(director.run_autopilot_cycle())
