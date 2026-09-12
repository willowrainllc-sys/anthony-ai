# --- EMPIRE INK EXPLAINER 3.1M-VIEW VIRAL ENGINE v4.0 (100% ORIGINAL WILLOW RAIN TITLES) ---
import os
import sys
import json
import uuid
import time
import random
import re
from pathlib import Path
from swarm_logger import swarm_log
from swarm_persistence import db

SECURE_DIR = Path(r"D:\ObsidianAi_Swarm\Secure_Assets")
EXPLAINER_VAULT = SECURE_DIR / "ink_explainers"
EXPLAINER_VAULT.mkdir(parents=True, exist_ok=True)

# 100% ORIGINAL WILLOW RAIN VIRAL RESEARCH CONCEPTS & TITLES
VIRAL_EXPLAINER_CONCEPTS = [
    {
        "category": "ANCIENT_WORK_HOURS",
        "title": "WILLOW RAIN: The 15-Hour Primitive Work Week & Human Time Illusion",
        "thumbnail_text": "NO JOBS",
        "myth_hook": "We work forty to sixty hours a week believing modern industrial life gives us freedom. But historical work-hour logs reveal ancient hunter-gatherers only worked fifteen hours a weeksnegotiating the rest of their days relaxing, telling stories, and sleeping.",
        "data_proof": "Anthropological studies of the Hazda and !Kung tribes confirmed that hunting and foraging required under three and a half hours per day. The remaining twelve hours were spent in communal rest and feast rituals.",
        "takeaway": "Progress made us richer in technology, but poorer in time. We built an industrial world where we work twice as hard as our ancient ancestors.",
        "prompts": [
            "2D vector illustration of ancient human lounging happily by a campfire in savanna NO JOBS 4k",
            "Modern office worker sitting overwhelmed at desk with huge stack of papers 2d vector",
            "Anthropological study timeline chart comparing work hours ancient vs modern 4k",
            "Ancient tribe members relaxing under giant baobab tree telling stories vector art 4k",
            "Sun setting over prehistoric hunter gatherer campsite golden lighting 4k",
            "Close up 2D vector graphic of hourglass draining sand quickly 4k",
            "Ancient cave painting illuminated by flickering firelight 4k",
            "Vibrant 2D vector animation of starry night sky over prehistoric valley 4k",
            "Modern clock gears spinning fast with glowing neon outline 4k",
            "Dramatic contrast split screen ancient hunter relaxing vs modern corporate commuter 4k"
        ]
    },
    {
        "category": "BIPHASIC_SLEEP",
        "title": "WILLOW RAIN: The Midnight Hour & Forgotten Biphasic Sleep Cycle",
        "thumbnail_text": "2 SLEEPS",
        "myth_hook": "Eight hours of continuous sleep is a modern industrial invention. Before electricity, humans slept in two distinct four-hour shifts separated by a midnight hour of quiet reflection.",
        "data_proof": "Historical diaries and medical journals from the fourteenth century routinely referenced first sleep and second sleep as standard human biology.",
        "takeaway": "If you wake up at three AM unable to sleep, you aren't broken. You're experiencing the natural human sleep cycle.",
        "prompts": [
            "2D vector illustration of medieval bedroom moonlight streaming through window 2 SLEEPS 4k",
            "Vintage hourglass separating two 4-hour sleep blocks vector art 4k",
            "Historical diary page with quill pen and candle lighting 4k",
            "Glowing clock face showing 3 AM midnight awakening 2d vector 4k",
            "Medieval town sleeping quietly under starry blue night sky 4k",
            "Vintage medical manuscript diagram of human brain sleep cycles 4k",
            "Cozy candle flame flickering in dark bedchamber 4k",
            "2D vector graphic of moon phases transitioning across dark night 4k",
            "Modern alarm clock ringing violently at 6 AM 2d vector 4k",
            "Peaceful sunrise over ancient village horizon golden light 4k"
        ]
    },
    {
        "category": "SILURIAN_HYPOTHESIS",
        "title": "WILLOW RAIN: Geochemical Traces & The 50-Million-Year Silurian Question",
        "thumbnail_text": "BEFORE US",
        "myth_hook": "If an industrial civilization existed on Earth fifty million years ago, all buildings, steel, and cities would erode to dust in under ten thousand years. The Silurian Hypothesis asks: what physical markers would remain?",
        "data_proof": "Geological rock stratum layers preserve only chemical signaturescarbon isotope spikes, synthetic plastics, and rare-earth element anomalies that endure across epochal timescales.",
        "takeaway": "Eternity erases architecture, but leaves geochemical footprints. Our entire modern legacy may reduce to a thin millimeter band of plastic in future rock strata.",
        "prompts": [
            "2D vector graphic of prehistoric Earth before humanity BEFORE US 4k",
            "Geological rock stratum layers showing microscopic rare earth element band 4k",
            "Microscopic synthetic plastics preserved in ancient sediment 2d vector",
            "Futuristic satellite mapping Earth geological thermal maximum 4k",
            "Deep earth excavation site paleocene rock layers 4k",
            "Stylized 2D graphic of industrial city eroding to green forest landscape 4k",
            "Ancient limestone monoliths covered in moss 4k",
            "Massive meteorite impact crater from space perspective 8k",
            "Scientific timeline diagram spanning 50 million years 2d vector",
            "Dramatic split screen futuristic metropolis vs deep earth geological core sample 4k"
        ]
    },
    {
        "category": "EXOPLANET_GLASS_RAIN",
        "title": "WILLOW RAIN: Supersonic Glass Storms of Exoplanet HD 189733 b",
        "thumbnail_text": "GLASS RAIN",
        "myth_hook": "One hundred light-years from Earth lies HD 189733 ba world that appears deep cobalt blue from space, but holds the most violent weather in the known universe.",
        "data_proof": "Supersonic equatorial jetstreams drag silicate particles sideways across the atmosphere at five thousand miles per hour, turning rain into razor-sharp molten glass.",
        "takeaway": "In deep space, beauty conceals extreme physics. What looks like a serene ocean from orbit is a supersonic storm of liquid glass.",
        "prompts": [
            "Deep cobalt blue gas giant planet HD 189733 b space perspective GLASS RAIN 8k",
            "Supersonic jetstreams dragging molten glass sideways across blue atmosphere 4k",
            "Spectroscopy light obsidian_global chart space background 2d vector",
            "NASA James Webb Space Telescope array orbiting Earth 8k",
            "Liquid glass droplets condensing in extreme planetary atmosphere 4k",
            "Glowing star shedding solar radiation onto giant exoplanet 4k",
            "3D motion graphic velocity vectors mapping 5000 mph winds 4k",
            "Exoplanet shadow passing across bright white host star 8k",
            "Deep space nebula with glowing star cluster background 8k",
            "Dramatic split screen calm blue ocean view vs supersonic liquid glass storm 4k"
        ]
    }
]

class InkExplainerEngine:
    """
    INK EXPLAINER VIRAL ENGINE v4.0 (100% ORIGINAL WILLOW RAIN TITLES):
    Generates original, non-infringing Willow Rain brand titles & scripts
    grounded in real-world academic research and 10 eye-popper scene clips.
    """
    def generate_viral_explainer_package(self, concept_idx: int = None) -> dict:
        swarm_log("INK_EXPLAINER: Generating original Willow Rain brand explainer package...", node="EXPLAINER")

        if concept_idx is None:
            concept = random.choice(VIRAL_EXPLAINER_CONCEPTS)
        else:
            concept = VIRAL_EXPLAINER_CONCEPTS[concept_idx % len(VIRAL_EXPLAINER_CONCEPTS)]

        explainer_id = f"explainer_{uuid.uuid4().hex[:6]}"
        full_script = f"{concept['myth_hook']} {concept['data_proof']} {concept['takeaway']}"

        payload = {
            "explainer_id": explainer_id,
            "category": concept.get("category", "EXPLAINER"),
            "title": concept["title"],
            "thumbnail_text": concept["thumbnail_text"],
            "full_script": full_script,
            "myth_hook": concept["myth_hook"],
            "data_proof": concept["data_proof"],
            "takeaway": concept["takeaway"],
            "scene_prompts": concept["prompts"],
            "tags": ["#WillowRain", "#OriginalDocumentary", "#History", "#CGI", "#DidYouKnow", "#Education", "#ObsidianMedia"]
        }

        # Save to Vault
        out_file = EXPLAINER_VAULT / f"{explainer_id}.json"
        with open(out_file, "w") as f:
            json.dump(payload, f, indent=4)

        db.log_event("INK_EXPLAINER", "EXPLAINER_PACKAGE_CREATED", {
            "title": concept["title"],
            "category": concept.get("category"),
            "vault_path": str(out_file)
        })

        swarm_log(f" ORIGINAL BRAND EXPLAINER SUCCESS: [{concept['title']}] package ready!", node="EXPLAINER")
        return payload

ink_explainer_engine = InkExplainerEngine()

if __name__ == "__main__":
    res = ink_explainer_engine.generate_viral_explainer_package(0)
    print("ORIGINAL BRAND EXPLAINER PACKAGE RESULT:")
    print(json.dumps(res, indent=2))
