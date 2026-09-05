# --- EMPIRE METADATA: CLEAN SOCIAL MEDIA BRANDING & TAGGING v3.0 ---
import re
import random

# Clean social media footers
FOOTERS = [
    "\n\n#Documentary #Science #Space #History #Mystery #Nature",
    "\n\n#DeepDive #Investigation #Uncovered #Explore #World",
    "\n\n#Knowledge #Secrets #Facts #DocumentaryFilm #Discover"
]

# Clean social media headers
HEADERS = [
    "UNCOVERED DOCUMENTARY",
    "EXPLORING THE UNKNOWN",
    "MUST WATCH DEEP DIVE",
    "SECRET HISTORY REVEALED",
    "NEW DOCUMENTARY DROP"
]

def scrub_sensitive_info(text):
    """
    ULTIMATE DATA SCRUBBER: Removes paths, keys, developer jargon, and internal JSON.
    Ensures zero backend leakage in public titles and captions.
    """
    if not text: return ""
    t = str(text)

    # 1. Strip internal JSON artifacts
    if "{" in t and "}" in t:
        try:
            import json
            parsed = json.loads(t)
            if isinstance(parsed, dict):
                t = parsed.get("title") or parsed.get("description") or parsed.get("concept") or t
        except: pass

    # 2. Strip Windows/Unix Paths & Hex IDs
    t = re.sub(r'[A-Za-z]:\\[^ \n]+', '', t)
    t = re.sub(r'/[^ \n]+/[^ \n]+', '', t)
    t = re.sub(r'[a-fA-F0-9]{16,}', '', t)
    t = re.sub(r'\{.*\}', '', t)

    # 3. Strip Backend Developer Keywords
    dev_words = [
        "SOVEREIGN STRIKE:", "SOVEREIGN LIVE STRIKE:", "ALPHA GRID:",
        "SIGNAL ", "SOVEREIGN", "STRIKE", "GRID", "DISCIPLE_",
        "AUTOPILOT_", "MISSION LOG", "SPECTRUM", "BREACH"
    ]
    for dw in dev_words:
        t = re.sub(re.escape(dw), '', t, flags=re.IGNORECASE)

    # 4. Clean up formatting
    t = re.sub(r'\s+', ' ', t).strip()
    return t

def get_full_caption(title, description=None):
    """
    Combines title and description into a clean, professional social media post.
    """
    clean_title = scrub_sensitive_info(title)
    if not clean_title or len(clean_title) < 5:
        clean_title = "Unclassified Documentary Investigation"

    header = random.choice(HEADERS)
    msg = f"{header} | {clean_title}\n\n"

    if description:
        clean_desc = scrub_sensitive_info(description)
        if clean_desc and len(clean_desc) > 5:
            if len(clean_desc) > 300:
                clean_desc = clean_desc[:297] + "..."
            msg += f"{clean_desc}\n\n"

    msg += random.choice(FOOTERS)
    return msg
