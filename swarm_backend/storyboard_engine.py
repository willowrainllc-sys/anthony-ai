# --- EMPIRE STORYBOARD ENGINE: SCENE-LOCKED FACTORY v2.0 (INFINITE DYNAMIC TOPICS) ---
import random
import json
from topic_engine import generate_unique_daily_content

MASTER_STORYBOARD_LIBRARY = [
    {
        "niche": "classified_heists",
        "title": "The 4-Minute State Reserve Vault Heist That Baffled Investigators",
        "storyboard": [
            {
                "scene": 1,
                "duration": 5,
                "spoken_script": "The blueprint of the state reserve had a structural flaw only one man knew about.",
                "visual_prompt": "Cinematic macro shot of architectural vault blueprint under dark studio lighting 4k",
                "on_screen_text": "THE STRUCTURAL FLAW"
            },
            {
                "scene": 2,
                "duration": 5,
                "spoken_script": "They bypassed three layers of state security in under four minutes without setting off alarms.",
                "visual_prompt": "Blue laser security grid museum vault door opening 4k cinematic",
                "on_screen_text": "4-MINUTE OVERRIDE"
            },
            {
                "scene": 3,
                "duration": 5,
                "spoken_script": "The artifact vanished from a locked vault while guards watched live camera feeds. Zero forensic traces were left behind.",
                "visual_prompt": "Empty high security steel bank vault door open in dim lighting 4k",
                "on_screen_text": "ZERO TRACES LEFT"
            }
        ],
        "tags": ["#GreatHeists", "#TrueCrime", "#VaultHeist", "#DocumentaryShorts", "#MysteryFiles"]
    },
    {
        "niche": "high_aura_masterminds",
        "title": "The Covert Intelligence Network Operating in Plain Sight",
        "storyboard": [
            {
                "scene": 1,
                "duration": 5,
                "spoken_script": "Her covert intelligence network operated in total stealth, outsmarting four global agencies at once.",
                "visual_prompt": "Cinematic 4k shot of elegant female strategist reviewing glowing maps in high-tech command center",
                "on_screen_text": "OPERATING IN STEALTH"
            },
            {
                "scene": 2,
                "duration": 5,
                "spoken_script": "She calculated complex market movements and security protocols in under three minutes without leaving a digital trace.",
                "visual_prompt": "Attractive woman wearing futuristic neural visor in dark neon studio 4k",
                "on_screen_text": "ZERO DIGITAL TRACE"
            },
            {
                "scene": 3,
                "duration": 5,
                "spoken_script": "By the time the breach was detected, the high-aura founder had already built an unbreachable sovereign AI grid.",
                "visual_prompt": "High-aura female creator standing before holographic data feeds 8k",
                "on_screen_text": "SOVEREIGN AI GRID"
            }
        ],
        "tags": ["#Masterminds", "#HighAura", "#Biography", "#Documentary", "#LuxuryTech", "#Power"]
    },
    {
        "niche": "deep_space_physics",
        "title": "What Deep Space Sensors Captured Near the Event Horizon",
        "storyboard": [
            {
                "scene": 1,
                "duration": 5,
                "spoken_script": "A massive magnetar ten thousand light-years away just released a gamma-ray burst that bent Earth's ionosphere.",
                "visual_prompt": "James Webb space telescope cosmic nebula deep space 8k",
                "on_screen_text": "GAMMA-RAY BURST"
            },
            {
                "scene": 2,
                "duration": 5,
                "spoken_script": "Near the accretion disk of Sagittarius A*, sub-atomic particles were recorded traveling faster than light.",
                "visual_prompt": "Glowing magnetar gamma ray burst bending spacetime light rays 4k",
                "on_screen_text": "FASTER THAN LIGHT"
            },
            {
                "scene": 3,
                "duration": 5,
                "spoken_script": "Sub-surface ocean radar on Europa detected hydrothermal plumes thirty miles high emitting rhythmic energy signals.",
                "visual_prompt": "Europa moon subsurface ice ocean thermal plume exploration 4k",
                "on_screen_text": "RHYTHMIC PULSES"
            }
        ],
        "tags": ["#SpaceDiscovery", "#Astronomy", "#NASA", "#Cosmos", "#Universe", "#BlackHole"]
    }
]

def build_synchronized_package(niche_key=None):
    """
    Guarantees 100% scene-locked alignment with infinite fresh daily topics.
    """
    # 1. First check if a fresh dynamic topic is generated from topic_engine
    try:
        dynamic_pkg = generate_unique_daily_content()
        if dynamic_pkg and dynamic_pkg.get("hook"):
            prompts = dynamic_pkg.get("prompts", [])
            hook = dynamic_pkg["hook"]
            niche = dynamic_pkg.get("niche", "unexplained_anomalies")

            storyboard = [
                {
                    "scene": 1,
                    "duration": 5,
                    "spoken_script": f"{hook}",
                    "visual_prompt": prompts[0] if len(prompts) > 0 else f"{niche} 4k cinematic documentary",
                    "on_screen_text": f"{hook[:20].upper()}"
                },
                {
                    "scene": 2,
                    "duration": 5,
                    "spoken_script": "Deep beneath the surface, satellite radar uncovered unexplainable data patterns. Breathtaking evidence preserved for centuries.",
                    "visual_prompt": prompts[1] if len(prompts) > 1 else f"{niche} exploration 4k",
                    "on_screen_text": "UNEXPLAINED DATA"
                },
                {
                    "scene": 3,
                    "duration": 5,
                    "spoken_script": "The unclassified archives are now open. Follow Anthony AI to unlock phase two.",
                    "visual_prompt": prompts[2] if len(prompts) > 2 else f"{niche} discovery 4k",
                    "on_screen_text": "DECLASSIFIED"
                }
            ]

            return {
                "title": dynamic_pkg["title"],
                "script": " ".join([s["spoken_script"] for s in storyboard]),
                "scene_prompts": [s["visual_prompt"] for s in storyboard],
                "storyboard": storyboard,
                "tags": dynamic_pkg.get("tags", ["#Documentary", "#Shorts"]),
                "niche": niche
            }
    except Exception as e:
        print("Dynamic topic generation fallback:", e)

    # 2. Hardened Static Fallback Library
    if niche_key:
        matches = [t for t in MASTER_STORYBOARD_LIBRARY if t["niche"] == niche_key]
        item = random.choice(matches) if matches else random.choice(MASTER_STORYBOARD_LIBRARY)
    else:
        item = random.choice(MASTER_STORYBOARD_LIBRARY)

    full_script = " ".join([s["spoken_script"] for s in item["storyboard"]])
    scene_prompts = [s["visual_prompt"] for s in item["storyboard"]]

    return {
        "title": item["title"],
        "script": full_script,
        "scene_prompts": scene_prompts,
        "storyboard": item["storyboard"],
        "tags": item["tags"],
        "niche": item["niche"]
    }

if __name__ == "__main__":
    print(json.dumps(build_synchronized_package(), indent=4))
