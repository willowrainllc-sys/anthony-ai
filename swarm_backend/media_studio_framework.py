# --- EMPIRE GENERAL-PURPOSE FACELESS AI MEDIA STUDIO FRAMEWORK v1.0 ---
import os
import sys
import json
import uuid
import time
import random
import re
from pathlib import Path
from dataclasses import dataclass, asdict, field
from typing import List, Dict, Any, Optional

from swarm_logger import swarm_log
from swarm_persistence import db

# --- 1. SUPPORTED CONTENT MODES & NICHES ---
CONTENT_MODES = [
    "FICTION", "DOCUMENTARY", "EDUCATIONAL", "COMMENTARY",
    "MYSTERY", "STORYTELLING", "MOTIVATIONAL", "ENTERTAINMENT", "NEWS_EXPLAINER"
]

SUPPORTED_NICHES = {
    "fantasy": {"mode": "FICTION", "style": "Cinematic dark fantasy 8k render, epic lighting"},
    "anime_scifi": {"mode": "FICTION", "style": "Stylized 2D/3D anime aesthetic, glowing cyberpunk neon"},
    "horror": {"mode": "STORYTELLING", "style": "Atmospheric dark horror, fog drenched shadows, 4k"},
    "mythology": {"mode": "FICTION", "style": "Ancient mythical gods and creatures, cinematic National Geographic style"},
    "scifi": {"mode": "FICTION", "style": "Futuristic space exploration, James Webb nebula cosmic renders"},
    "mystery": {"mode": "MYSTERY", "style": "Classified dossier, dark obsidian matrix, high-contrast studio"},
    "finance": {"mode": "EDUCATIONAL", "style": "Motion graphics, high-end Wall Street terminal visuals, luxury dark theme"},
    "psychology": {"mode": "EDUCATIONAL", "style": "Mind matrix, glowing neural network, high-contrast human portraits"},
    "history": {"mode": "DOCUMENTARY", "style": "Historical archival 4k, parchment maps, dramatic lighting"},
    "motivation": {"mode": "MOTIVATIONAL", "style": "Inspiring mountain peaks, intense cinematic training footage"},
    "gaming_lore": {"mode": "STORYTELLING", "style": "Unreal Engine 5.4 3D environment, high-res gaming render"},
    "sports_stories": {"mode": "DOCUMENTARY", "style": "High-octane stadium lights, slow-motion athletic cinematography"}
}

# --- 2. CANONICAL CONTENT CONTEXT (SINGLE SOURCE OF TRUTH) ---
@dataclass
class ContentContext:
    channel_id: str
    series_id: str
    season_id: str
    episode_id: str
    niche: str
    content_mode: str
    audience: str
    tone: str
    series_title: str
    series_theme: str
    season_theme: str
    episode_number: int
    episode_title: str
    episode_topic: str
    primary_subject: str
    secondary_subjects: List[str]
    entities: List[str]
    locations: List[str]
    keywords: List[str]
    story_summary: str
    hook: str
    evidence_or_climax: str
    unresolved_questions: str
    previous_episode_summary: str
    next_episode_tease: str
    target_duration_sec: int
    content_type: str # "LONG_FORM" or "SHORT_FORM"
    visual_style: str
    narration_style: str
    parent_episode_id: Optional[str] = None

# --- 3. NICHE & SERIES DIRECTOR ---
class NicheDirectorStudio:
    """
    GENERAL-PURPOSE AI MEDIA STUDIO:
    Converts any niche request into a persistent Series Bible, Season 1 Arc, and Episode Plan.
    """
    def __init__(self):
        self._init_studio_tables()

    def _init_studio_tables(self):
        with db._get_connection() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS studio_series (
                    series_id TEXT PRIMARY KEY,
                    channel_id TEXT,
                    niche TEXT,
                    content_mode TEXT,
                    series_title TEXT,
                    series_description TEXT,
                    visual_style TEXT,
                    narration_style TEXT,
                    season_number INTEGER DEFAULT 1,
                    season_theme TEXT,
                    season_arc TEXT,
                    created_at REAL DEFAULT (strftime('%s', 'now'))
                )
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS studio_episodes (
                    episode_id TEXT PRIMARY KEY,
                    series_id TEXT,
                    season_id TEXT,
                    episode_number INTEGER,
                    title TEXT,
                    primary_subject TEXT,
                    keywords_json TEXT,
                    summary TEXT,
                    status TEXT DEFAULT 'PLANNED',
                    created_at REAL DEFAULT (strftime('%s', 'now'))
                )
            """)
            conn.commit()

    async def create_studio_channel_series(self, channel_id: str, niche: str) -> dict:
        niche_key = niche.lower().replace(" ", "_")
        niche_info = SUPPORTED_NICHES.get(niche_key, {"mode": "DOCUMENTARY", "style": "Cinematic 4k high contrast"})
        series_id = f"series_{channel_id.lower()}_{niche_key}"

        with db._get_connection() as conn:
            row = conn.execute("SELECT * FROM studio_series WHERE series_id=?", (series_id,)).fetchone()
            if row:
                return {
                    "series_id": row[0], "channel_id": row[1], "niche": row[2], "content_mode": row[3],
                    "series_title": row[4], "series_description": row[5], "visual_style": row[6],
                    "narration_style": row[7], "season_number": row[8], "season_theme": row[9], "season_arc": row[10]
                }

        swarm_log(f"STUDIO: Creating General-Purpose Series for [{niche.upper()}] (Mode: {niche_info['mode']})...", node="STUDIO")

        series_title = f"{niche.title()}: The Complete Chronicles"
        series_description = f"Sovereign AI Media Studio production exploring {niche} across Season 1."
        season_theme = f"Season 1: Awakening & First Contact in {niche.title()}"
        season_arc = f"10-Episode arc detailing origin, escalation, climax, and resolution for {niche}."

        series_data = {
            "series_id": series_id,
            "channel_id": channel_id,
            "niche": niche_key,
            "content_mode": niche_info["mode"],
            "series_title": series_title,
            "series_description": series_description,
            "visual_style": niche_info["style"],
            "narration_style": "Deep, authoritative, gravelly documentary/storyteller narrator (en-US-ChristopherNeural)",
            "season_number": 1,
            "season_theme": season_theme,
            "season_arc": season_arc
        }

        with db._get_connection() as conn:
            conn.execute("""
                INSERT INTO studio_series (series_id, channel_id, niche, content_mode, series_title, series_description, visual_style, narration_style, season_number, season_theme, season_arc)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (series_data["series_id"], series_data["channel_id"], series_data["niche"], series_data["content_mode"], series_data["series_title"], series_data["series_description"], series_data["visual_style"], series_data["narration_style"], series_data["season_number"], series_data["season_theme"], series_data["season_arc"]))
            conn.commit()

        # Build 10 Season 1 Episodes
        await self._plan_season_episodes(series_id, "season_01", niche_key)
        return series_data

    async def _plan_season_episodes(self, series_id: str, season_id: str, niche_key: str):
        episodes_plan = [
            (1, "The Awakening", f"Initial discovery and origin event of {niche_key}", [niche_key, "awakening", "origin", "entry"]),
            (2, "First Shadows", f"Uncovering hidden patterns and early evidence in {niche_key}", [niche_key, "shadows", "evidence", "discovery"]),
            (3, "The Escalation", f"Conflict and stakes increase dramatically across {niche_key}", [niche_key, "escalation", "stakes", "conflict"]),
            (4, "The Unseen Force", f"Revealing the mastermind or underlying mechanism", [niche_key, "unseen", "force", "mastermind"]),
            (5, "Deep Investigation", f"Comprehensive analysis of data and historical logs", [niche_key, "investigation", "analysis", "logs"]),
            (6, "The Contradiction", f"A major twist or conflicting piece of evidence emerges", [niche_key, "contradiction", "twist", "evidence"]),
            (7, "The Climax", f"Major confrontation or ultimate discovery in {niche_key}", [niche_key, "climax", "confrontation", "revelation"]),
            (8, "The Fallout", f"Immediate aftermath and impact on the world", [niche_key, "fallout", "aftermath", "impact"]),
            (9, "Reconstructing the Truth", f"Putting all pieces together for the final verdict", [niche_key, "truth", "reconstruction", "verdict"]),
            (10, "Season Conclusion", f"Final resolution and teaser for Season 2", [niche_key, "conclusion", "season 2", "future"])
        ]

        with db._get_connection() as conn:
            for ep_num, title, subject, keywords in episodes_plan:
                ep_id = f"ep_{series_id}_{season_id}_{ep_num:02d}"
                conn.execute("""
                    INSERT OR IGNORE INTO studio_episodes (episode_id, series_id, season_id, episode_number, title, primary_subject, keywords_json, summary)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (ep_id, series_id, season_id, ep_num, title, subject, json.dumps(keywords), f"Season 1 Episode {ep_num}: {subject}"))
            conn.commit()

    async def get_canonical_context(self, channel_id: str, niche: str, ep_number: int = 1, target_min: int = 12, content_type: str = "LONG_FORM") -> ContentContext:
        series_data = await self.create_studio_channel_series(channel_id, niche)
        series_id = series_data["series_id"]
        season_id = "season_01"
        ep_id = f"ep_{series_id}_{season_id}_{ep_number:02d}"

        with db._get_connection() as conn:
            row = conn.execute("SELECT title, primary_subject, keywords_json, summary FROM studio_episodes WHERE episode_id=?", (ep_id,)).fetchone()
            if row:
                title, subject, kw_json, summary = row[0], row[1], row[2], row[3]
                keywords = json.loads(kw_json)
            else:
                title, subject, keywords, summary = f"Episode {ep_number}", f"Investigation into {niche}", [niche, "episode"], f"Episode {ep_number} coverage."

        target_sec = (target_min * 60) if content_type == "LONG_FORM" else 90 # Default Short 90s

        return ContentContext(
            channel_id=channel_id,
            series_id=series_id,
            season_id=season_id,
            episode_id=ep_id,
            niche=niche,
            content_mode=series_data["content_mode"],
            audience="High-retention documentary & storytelling enthusiasts",
            tone="Deep, serious, high-stakes, atmospheric",
            series_title=series_data["series_title"],
            series_theme=series_data["season_theme"],
            season_theme=series_data["season_theme"],
            episode_number=ep_number,
            episode_title=title,
            episode_topic=f"{title}: {subject}",
            primary_subject=subject,
            secondary_subjects=[niche.title(), "Case Analysis", "Unclassified Files"],
            entities=["Primary Subject", "Investigation Unit", "Archival Intelligence"],
            locations=[f"{niche.title()} Sector", "Central Archive"],
            keywords=keywords,
            story_summary=summary,
            hook=f"In the opening phase of {title}, a major discovery altered our understanding of {subject}.",
            evidence_or_climax=f"Declassified logs and physical evidence confirm the timeline of {subject}.",
            unresolved_questions=f"What lies beyond the findings of Episode {ep_number}?",
            previous_episode_summary=f"Episode {ep_number - 1} introduced the initial evidence." if ep_number > 1 else "Season 1 Premiere.",
            next_episode_tease=f"In Episode {ep_number + 1}, we explore the deeper consequences.",
            target_duration_sec=target_sec,
            content_type=content_type,
            visual_style=series_data["visual_style"],
            narration_style=series_data["narration_style"]
        )

media_studio = NicheDirectorStudio()

if __name__ == "__main__":
    import asyncio
    async def test():
        ctx = await media_studio.get_canonical_context("ANTHONY_AI_OFFICIAL", "fantasy", ep_number=1, target_min=12)
        print("CANONICAL CONTEXT CREATED:")
        print("Series:", ctx.series_title)
        print("Episode:", ctx.episode_title, "| Mode:", ctx.content_mode)
        print("Visual Style:", ctx.visual_style)
    asyncio.run(test())
