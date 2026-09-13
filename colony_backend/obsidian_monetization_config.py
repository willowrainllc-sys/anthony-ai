# --- Built by Anthony Christopher | Est 12.19.1987 ---
# --- OBSIDIAN EMPIRE: GLOBAL MONETIZATION MATRIX v3.0 ---
import os
from pathlib import Path

# 🔱 CENTRALIZED REVENUE KEYS
MONETIZATION_CONFIG = {
    "AD_NETWORKS": {
        "ADSENSE": {
            "pub_id": "pub-9539640812310468",
            "status": "LIVE_PRODUCTION",
            "type": "DISPLAY_BANNERS"
        },
        "ADMOB": {
            "app_id": "ca-app-pub-9539640812310468~9197828544",
            "header_unit": "ca-app-pub-9539640812310468/8547091855",
            "footer_unit": "ca-app-pub-9539640812310468/8031699492",
            "status": "ACTIVE_MOBILE"
        },
        "PROPELLER_ADS": {
            "tag_id": "TRIAL_ACTIVE_103",
            "type": "PUSH_INTERSTITIAL"
        }
    },
    "CONTEXTUAL_LINKS": {
        "SOVRN": {
            "script_id": "obsidian_sovrn_v29",
            "status": "AUTO_INJECT_READY"
        },
        "INFOLINKS": {
            "publisher_id": "IL_OBS_2026",
            "type": "UNDERLINE_HOVER"
        }
    },
    "AFFILIATE_WIDGETS": {
        "AMAZON": {
            "tag": "flikmobile-20",
            "status": "ACTIVE_EMBED"
        },
        "PRINTFUL": {
            "store_id": "18670114",
            "type": "POD_MERCH"
        }
    },
    "CONTENT_RECOMMENDATIONS": {
        "TABOOLA": {
            "publisher_id": "obsidian-network",
            "placement": "BOTTOM_OF_ARTICLE"
        }
    }
}

def get_monetization_payload():
    """Returns the optimized monetization payload for the frontend handshake."""
    return {
        "adsense_pub": f"ca-{MONETIZATION_CONFIG['AD_NETWORKS']['ADSENSE']['pub_id']}",
        "amazon_tag": MONETIZATION_CONFIG['AFFILIATE_WIDGETS']['AMAZON']['tag'],
        "enabled_features": ["CONTEXTUAL_LINKS", "NATIVE_RECOMMENDATIONS", "HEADER_BIDDING"],
        "status": "ARMORED_FOR_REVENUE"
    }
