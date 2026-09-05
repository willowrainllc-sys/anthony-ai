# --- EMPIRE AUTONOMOUS TOPIC & THEME FACTORY v3.0 (HIGH-AURA MASTERMINDS, HEISTS & DECLASSIFIED SECRETS) ---
import os
import time
import random
import json
from datetime import datetime

# --- HIGH-INTENSITY BADASS ARCHETYPES & THEMES ---
UNIQUE_ARCHETYPES = {
    "high_aura_masterminds": {
        "hooks": [
            "Her covert intelligence network operated in total stealth, outsmarting four global agencies at once.",
            "The high-aura strategist who built a multi-billion dollar sovereign AI infrastructure in total secrecy.",
            "She bypassed state security protocols in under three minutes without leaving a digital trace.",
            "The secret mastermind behind the world's most lucrative trading algorithm revealed."
        ],
        "tags": ["#Masterminds", "#HighAura", "#Biography", "#Documentary", "#LuxuryTech", "#Power"],
        "visual_themes": ["glamour_cyber_glow", "high_contrast_studio", "cinematic_noir_portrait"],
        "prompts": [
            "Cinematic 4k shot of beautiful high-aura woman wearing futuristic neural visor reviewing holographic data in luxury studio",
            "Elegant female strategist walking through rainy illuminated Neo-Tokyo boulevard cinematic 4k",
            "High-profile female tech founder standing before massive glowing glass server array 8k",
            "Glamorous woman in dark tailored suit looking at financial telemetry displays 4k"
        ]
    },
    "classified_heists": {
        "hooks": [
            "The underground vault contained fifty tons of unclassified gold that vanished without a single alarm sounding.",
            "The museum security feeds froze for ninety seconds. When they reconnected, the artifact was gone.",
            "This mastermind executed a hundred-million-dollar heist and left zero forensic DNA.",
            "The blueprint of the state reserve had a structural flaw only one man knew about."
        ],
        "tags": ["#GreatHeists", "#TrueCrime", "#UnsolvedMysteries", "#Documentary", "#Masterminds", "#Secrets"],
        "visual_themes": ["vault_laser_noir", "blueprint_cyber_grid", "classified_dossier_matrix"],
        "prompts": [
            "Sleek museum vault illuminated by blue security lasers 4k",
            "High-contrast shadowy figure in tailored suit walking through dark obsidian hallway cinematic",
            "Close up of mechanical safe combination vault door unlocking in slow motion 4k",
            "Futuristic bank vault glowing laser security grid reflection 4k"
        ]
    },
    "unexplained_anomalies": {
        "hooks": [
            "Satellite radar uncovered a massive unmapped subterranean complex three thousand feet beneath desert sand.",
            "Declassified sonar logs confirmed a giant submerged metallic sphere moving against ocean currents at 100 knots.",
            "The coordinates of this lost military mountain base were scrubbed from every international map in 1952.",
            "For three hours, every atomic clock in the research sector stopped at exactly 3:14."
        ],
        "tags": ["#Unexplained", "#Declassified", "#SecretHistory", "#Documentary", "#Anomalies", "#DeepDive"],
        "visual_themes": ["radar_green_scan", "deep_sea_sonar_glow", "classified_redacted_noir"],
        "prompts": [
            "Satellite LIDAR scan uncovering massive subterranean desert ruins aerial drone 4k",
            "Military research submarine spotlight illuminating gigantic submerged ancient structure deep sea 4k",
            "Extreme mountain peak blizzard sweeping over mysterious high-altitude radar dome 8k",
            "Declassified government dossier folder stamped secret illuminated by desk lamp 4k"
        ]
    },
    "deep_space_physics": {
        "hooks": [
            "James Webb Space Telescope just captured a gamma-ray burst from a magnetar that bent local spacetime.",
            "Near the event horizon of Sagittarius A*, sub-atomic particles were recorded traveling faster than light.",
            "A planetary ring system three hundred times larger than Saturn was confirmed orbiting an exoplanet.",
            "Sub-surface ocean radar on Europa detected hydrothermal plumes thirty miles high."
        ],
        "tags": ["#SpaceDiscovery", "#Astronomy", "#NASA", "#Cosmos", "#Universe", "#BlackHole"],
        "visual_themes": ["nebula_cosmic_glow", "lunar_far_side_monochrome", "quantum_star_field"],
        "prompts": [
            "James Webb space telescope cosmic nebula deep space 8k",
            "Glowing magnetar gamma ray burst bending spacetime light rays 4k",
            "Black hole event horizon accretion disk pulling in cosmic dust cinematic 8k",
            "Europa moon subsurface ice ocean thermal plume exploration 4k"
        ]
    },
    "apex_predators_and_wilderness": {
        "hooks": [
            "The black panther stalking its territory under a full moon in deep jungle night.",
            "Stranded fifty miles off the grid in minus-forty arctic cold, his survival protocol defied all odds.",
            "The alpha wolf leading its pack through vertical snow-covered mountain canyons in 8K.",
            "In the deep shadow of the canyon, an unseen predator moves with zero sound."
        ],
        "tags": ["#ApexPredators", "#Wildlife4K", "#ExtremeSurvival", "#NatureDocumentary", "#Wilderness"],
        "visual_themes": ["wildlife_macro_natural", "himalayan_blizzard_cinematic", "deep_forest_shadows"],
        "prompts": [
            "Majestic black panther prowling through dark rainforest night full moon spotlight 4k",
            "Extreme arctic wilderness blizzard survival expedition drone shot 4k",
            "Alpha wolf pack walking through snowy mountain valley 8k",
            "High-contrast lion eyes glowing in dark night savanna cinematic 4k"
        ]
    }
}

USED_COMBINATIONS = set()

def generate_unique_daily_content():
    """
    Picks a random niche, hook, and visual theme combination ensuring
    it has never been used before, returning a complete production package.
    """
    niches = list(UNIQUE_ARCHETYPES.keys())
    selected_niche = random.choice(niches)
    archetype = UNIQUE_ARCHETYPES[selected_niche]

    available_hooks = [h for h in archetype["hooks"] if (selected_niche, h) not in USED_COMBINATIONS]

    if not available_hooks:
        USED_COMBINATIONS.clear()
        available_hooks = archetype["hooks"]

    selected_hook = random.choice(available_hooks)
    selected_theme = random.choice(archetype["visual_themes"])

    USED_COMBINATIONS.add((selected_niche, selected_hook))

    timestamp_id = datetime.now().strftime("%d%H%M%S")
    package = {
        "content_id": f"FILE-{timestamp_id}",
        "niche": selected_niche,
        "title": f"Unsolved Investigation: {selected_hook[:55]}",
        "hook": selected_hook,
        "visual_theme": selected_theme,
        "tags": archetype["tags"] + [f"#{selected_niche.replace('_', '').capitalize()}Files"],
        "prompts": archetype.get("prompts", [
            f"{selected_niche} documentary 4k cinematic",
            f"cinematic high contrast {selected_niche} footage"
        ]),
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    return package

def start_topic_factory():
    """Runs 365 days a year creating fresh, non-repeating content topics and themes."""
    print("[*] Autonomous Topic & Theme Factory Online. Initializing 365-day loop...")

    while True:
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print("\n------------------------------------------")
        print(f"[{current_time}] Generating Fresh Unique Content Topic...")
        print("------------------------------------------")

        topic_package = generate_unique_daily_content()
        print(json.dumps(topic_package, indent=4))

        jitter_delay = random.randint(7200, 18000)
        print(f"\n[*] Topic locked. Entering stealth standby for {jitter_delay // 60} minutes...")
        time.sleep(jitter_delay)

if __name__ == "__main__":
    start_topic_factory()
