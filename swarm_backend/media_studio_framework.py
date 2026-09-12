# --- EMPIRE GENERAL-PURPOSE FACELESS AI MEDIA STUDIO FRAMEWORK v4.0 (BLOCKBUSTER & NATGEO THEMES) ---
import os
import sys
import json
import uuid
import time
import random
import re
from pathlib import Path
from dataclasses import dataclass, asdict
from typing import List, Dict, Any, Optional

from swarm_logger import swarm_log
from swarm_persistence import db

# --- 1. BLOCKBUSTER & NATIONAL GEOGRAPHIC THEMED NICHES ---
CONTENT_MODES = [
    "FICTION", "DOCUMENTARY", "EDUCATIONAL", "COMMENTARY",
    "MYSTERY", "STORYTELLING", "MOTIVATIONAL", "ENTERTAINMENT", "NEWS_EXPLAINER"
]

SUPPORTED_NICHES = {
    "natgeo_expeditions": {
        "mode": "DOCUMENTARY",
        "title": "National Geographic Deep Ocean & Abyss Enigmas",
        "style": "National Geographic IMAX 4k 60fps nature cinematography, abyssal trench 8k lighting",
        "theme": "Deep-sea research submersibles mapping 10,000 meters below sea level"
    },
    "blockbuster_scifi": {
        "mode": "FICTION",
        "title": "Hollywood Sci-Fi Spectacle & Cosmic Anomalies",
        "style": "Hollywood IMAX Blockbuster Sci-Fi, Unreal Engine 5.4 Lumen 8k ray-traced lighting",
        "theme": "Quantum event horizons, interstellar wormholes, and planetary defense"
    },
    "badass_heists": {
        "mode": "STORYTELLING",
        "title": "High-Aura Masterminds & Great Vault Heists",
        "style": "Sleek IMAX thriller, neon terminal laser grid, high-aura cinematic 4k",
        "theme": "Covert intelligence networks bypassing triple-layer state security"
    },
    "badass_military": {
        "mode": "DOCUMENTARY",
        "title": "Declassified Military Operations & Defense Files",
        "style": "FLIR thermal radar telemetry, declassified military dossier, night vision 4k",
        "theme": "Unclassified radar tracking logs and supersonic aerial intercepts"
    },
    "natgeo_history": {
        "mode": "DOCUMENTARY",
        "title": "National Geographic Lost Empires & Ancient Monoliths",
        "style": "National Geographic archaeological 4k drone shot, ancient stone ruins golden hour",
        "theme": "Subterranean pyramids, acoustic levitation, and forgotten civilization archives"
    },
    "badass_horror": {
        "mode": "STORYTELLING",
        "title": "Visceral Urban Legends & Dark Folklore",
        "style": "Atmospheric dark horror IMAX, foggy pine forest shadows, eerie 4k",
        "theme": "Isolated wilderness staircases and late-night national park encounters"
    },
    "natgeo_space": {
        "mode": "DOCUMENTARY",
        "title": "National Geographic Deep Space & Lunar Frontiers",
        "style": "National Geographic deep space telescope cosmic nebula IMAX 8k",
        "theme": "Far-side lunar radar scans and magnetar gamma-ray bursts"
    }
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
    body_evidence: str
    climax_payoff: str
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
    CANONICAL BLOCKBUSTER & NATGEO MEDIA STUDIO:
    Constructs high-octane IMAX-quality storyboards for Blockbuster, NatGeo, and Badass themes.
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
                    hook TEXT,
                    climax TEXT,
                    status TEXT DEFAULT 'PLANNED',
                    created_at REAL DEFAULT (strftime('%s', 'now'))
                )
            """)
            try:
                conn.execute("ALTER TABLE studio_episodes ADD COLUMN hook TEXT")
                conn.execute("ALTER TABLE studio_episodes ADD COLUMN climax TEXT")
            except: pass
            conn.commit()

    async def create_studio_channel_series(self, channel_id: str, niche: str) -> dict:
        niche_key = niche.lower().replace(" ", "_")
        niche_info = SUPPORTED_NICHES.get(niche_key, SUPPORTED_NICHES["natgeo_expeditions"])
        series_id = f"series_{channel_id.lower()}_{niche_key}"

        with db._get_connection() as conn:
            row = conn.execute("SELECT * FROM studio_series WHERE series_id=?", (series_id,)).fetchone()
            if row:
                return {
                    "series_id": row[0], "channel_id": row[1], "niche": row[2], "content_mode": row[3],
                    "series_title": row[4], "series_description": row[5], "visual_style": row[6],
                    "narration_style": row[7], "season_number": row[8], "season_theme": row[9], "season_arc": row[10]
                }

        swarm_log(f"STUDIO: Creating Blockbuster/NatGeo Series for [{niche_info['title']}]...", node="STUDIO")

        series_title = f"{niche_info['title']}: Season 1"
        series_description = f"High-budget IMAX production exploring {niche_info['theme']}."
        season_theme = f"Season 1: Unclassified Discovery & First Contact in {niche_info['title']}"
        season_arc = f"10-Episode blockbuster arc detailing discovery, escalation, physical evidence, and final resolution."

        series_data = {
            "series_id": series_id,
            "channel_id": channel_id,
            "niche": niche_key,
            "content_mode": niche_info["mode"],
            "series_title": series_title,
            "series_description": series_description,
            "visual_style": niche_info["style"],
            "narration_style": "Deep, gravelly, IMAX documentary narrator (en-US-ChristopherNeural)",
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

        await self._plan_season_episodes(series_id, "season_01", niche_key)
        return series_data

    async def _plan_season_episodes(self, series_id: str, season_id: str, niche_key: str):
        episodes_plan = [
            (1, "The Unclassified Discovery", f"Initial high-stakes discovery event in {niche_key}", f"At midnight, deep-sea research submersibles mapped a massive submerged metallic hull ten thousand feet down.", f"Sonar telemetry confirmed zero natural corrosion, suggesting a preserved structure.", ["natgeo", "expedition", "abyss", "discovery"]),
            (2, "The Mach 4 Radar Intercept", f"Supersonic radar tracks defying atmospheric drag", f"A military pilot locked radar onto a glowing sphere descending from eighty thousand feet in three seconds.", f"FLIR thermal imaging confirmed zero propulsion exhaust or heat signatures.", ["radar", "supersonic", "flir", "military"]),
            (3, "The 100-Million Vault Heist", f"Covert intelligence network executing a flawless breach", f"They bypassed three layers of state security in under four minutes without setting off alarms.", f"Digital forensics proved zero human code modifications were made for forty days.", ["heist", "mastermind", "stealth", "vault"]),
            (4, "The Subterranean Monolith", f"Archaeological expedition uncovers forgotten pyramids", f"Satellite imagery unsealed a redacted underground complex beneath the ice sheet.", f"Acoustic levitation frequency pulses were recorded emitting from the central chamber.", ["monolith", "pyramid", "archaeology", "ruins"])
        ]

        with db._get_connection() as conn:
            for ep_num, title, subject, hook, climax, keywords in episodes_plan:
                ep_id = f"ep_{series_id}_{season_id}_{ep_num:02d}"
                conn.execute("""
                    INSERT OR IGNORE INTO studio_episodes (episode_id, series_id, season_id, episode_number, title, primary_subject, keywords_json, summary, hook, climax)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (ep_id, series_id, season_id, ep_num, title, subject, json.dumps(keywords), f"IMAX Documentary investigation into {subject}.", hook, climax))
            conn.commit()

    async def get_canonical_context(self, channel_id: str, niche: str, ep_number: int = 1, target_min: int = 12, content_type: str = "LONG_FORM") -> ContentContext:
        series_data = await self.create_studio_channel_series(channel_id, niche)
        series_id = series_data["series_id"]
        season_id = "season_01"
        ep_id = f"ep_{series_id}_{season_id}_{ep_number:02d}"

        with db._get_connection() as conn:
            row = conn.execute("SELECT title, primary_subject, keywords_json, summary, hook, climax FROM studio_episodes WHERE episode_id=?", (ep_id,)).fetchone()
            if row:
                title, subject, kw_json, summary, hook, climax = row[0], row[1], row[2], row[3], row[4], row[5]
                keywords = json.loads(kw_json) if kw_json else [niche, "investigation"]
            else:
                title, subject, keywords = f"Episode {ep_number}", f"High-stakes investigation into {niche}", [niche, "episode"]
                summary = f"IMAX Documentary investigation into {subject}."
                hook = f"At midnight, research teams unsealed an ancient vault holding preserved evidence regarding {subject}."
                climax = f"Physical evidence confirmed that the structures had remained untouched for millennia."

        target_sec = (target_min * 60) if content_type == "LONG_FORM" else 90

        body_ev = f"Deep within {niche.replace('_', ' ').title()} Sector 7, team leads recorded unprecedented physical data patterns. Primary subject {subject} maintained a stable trajectory despite adverse conditions."

        return ContentContext(
            channel_id=channel_id,
            series_id=series_id,
            season_id=season_id,
            episode_id=ep_id,
            niche=niche,
            content_mode=series_data["content_mode"],
            audience="High-retention IMAX documentary & blockbuster storytelling enthusiasts",
            tone="Deep, serious, high-stakes, IMAX atmospheric",
            series_title=series_data["series_title"],
            series_theme=series_data["season_theme"],
            season_theme=series_data["season_theme"],
            episode_number=ep_number,
            episode_title=title,
            episode_topic=f"{title}: {subject}",
            primary_subject=subject,
            secondary_subjects=[niche.replace('_', ' ').title(), "Case Analysis", "Unclassified Files"],
            entities=["Primary Subject", "Investigation Unit", "National Geographic Research"],
            locations=[f"{niche.replace('_', ' ').title()} Sector", "Central Archive"],
            keywords=keywords,
            story_summary=summary,
            hook=hook,
            body_evidence=body_ev,
            climax_payoff=climax,
            unresolved_questions="What unclassified logs remain hidden in the deeper archives?",
            previous_episode_summary="The initial discovery established the baseline evidence.",
            next_episode_tease="Unlocking the secondary vault reveals the remaining truth.",
            target_duration_sec=target_sec,
            content_type=content_type,
            visual_style=series_data["visual_style"],
            narration_style=series_data["narration_style"]
        )

media_studio = NicheDirectorStudio()

if __name__ == "__main__":
    import asyncio
    async def test():
        ctx = await media_studio.get_canonical_context("ANTHONY_AI_OFFICIAL", "natgeo_expeditions", ep_number=1, target_min=1)
        print("NATGEO CONTEXT CREATED:")
        print("Series:", ctx.series_title)
        print("Style:", ctx.visual_style)
    asyncio.run(test())
