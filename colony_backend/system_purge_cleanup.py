# --- Owned by Anthony Christopher Maestas | Directed by ARES ---
# --- ARES SYSTEM PURGE & WORKSPACE CLEANUP v1.0 ---
import os
import shutil
from pathlib import Path

def purge_system():
    root = Path(r"C:\Users\willo\OneDrive\Desktop\Anthony_Ai")

    # 🔱 1. TARGETS FOR TOTAL DELETION (Snapshots, Logs, Temp)
    purge_dirs = [
        "dominance_snapshots", "earnapp_snapshots", "geonode_snapshots",
        "ipsos_snapshots", "payout_EARNAPP_snapshots", "payout_FREECASH_snapshots",
        "payout_INBOXDOLLARS_snapshots", "payout_IPSOS_ISAY_snapshots",
        "payout_OBSIDIAN_INGRESS_snapshots", "payout_PAWNS_APP_snapshots",
        "payout_SWAGBUCKS_snapshots", "robinhood_snapshots", "seo_snapshots",
        "obsidian_cloud", "saturn_cloud", "willow_rain_global", "willow_rain_hub",
        "colony_vault", "renders", ".gradle", "build"
    ]

    # 🔱 2. ROOT HTML TO KEEP
    keep_html = {
        "index.html", "obsidian_ai_builder.html", "obsidian_ai_studio.html",
        "obsidian_auth_callback.html", "obsidian_city_dashboard.html",
        "obsidian_city_landing.html", "obsidian_city_marketplace.html", "obsidian_data_sharing.html",
        "obsidian_director_hub.html", "obsidian_domains.html", "obsidian_domain_results.html",
        "obsidian_help_center.html", "obsidian_hosting_landing.html",
        "obsidian_industrial_mesh.html", "obsidian_llc_formation.html",
        "obsidian_llc_intake.html", "obsidian_llc_state.html",
        "obsidian_monetization_hub.html", "obsidian_pay_hub.html",
        "obsidian_register.html", "obsidian_site_builder_landing.html",
        "obsidian_signin.html", "obsidian_vps_hosting.html", "obsidian_vps_configure.html",
        "obsidian_vps_dashboard.html", "obsidian_wordpress_support.html",
        "obsidian_openclaw_hosting.html", "obsidian_nodejs_hosting.html",
        "obsidian_unified_checkout.html", "success.html", "terms.html", "privacy.html",
        "ares_oracle_chat_monitor.html", "obsidian_city_tech.html", "obsidian_web_voyager.html",
        "obsidian_user_profile.html", "obsidian_device_grid.html", "obsidian_ranking_lookup.html",
        "obsidian_premium_domains.html"
    }

    print("🔱 ARES: Initiating Global System Purge...")

    # Purge Directories
    for d in purge_dirs:
        target = root / d
        if target.exists():
            try:
                shutil.rmtree(target)
                print(f"[!] Purged Directory: {d}")
            except Exception as e:
                print(f"[-] Failed to purge {d}: {e}")

    # Purge Root Files (Temp/Irrelevant)
    for f in root.glob("*"):
        if f.is_file():
            # Keep .py, .js, .css, .json, .env, .gitignore, and core HTML
            if f.suffix == ".mp4" or f.suffix == ".log" or f.suffix == ".bat" or f.suffix == ".dmg":
                if f.name not in ["ANTHONY.bat"]: # Keep main launcher
                    f.unlink()
                    print(f"[!] Purged File: {f.name}")
            elif f.suffix == ".html" and f.name not in keep_html:
                f.unlink()
                print(f"[!] Purged Legacy HTML: {f.name}")

    print("\n🔱 SYSTEM PURGE COMPLETE. GRID IS CLEANED.")

if __name__ == "__main__":
    purge_system()