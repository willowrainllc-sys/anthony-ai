# --- Built by Anthony Christopher | Est 12.19.1987 ---
# --- OBSIDIAN CITY MOBILE UI SYNC v1.0 ---
import os
import glob

def inject_mobile_assets(file_path):
    if not os.path.exists(file_path):
        return

    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    # 1. Inject CSS & JS links if missing
    css_mobile = '<link href="assets/obsidian_mobile_core.css" rel="stylesheet"/>'
    css_aura = '<link href="assets/obsidian_aura_ui.css" rel="stylesheet"/>'
    js_aura = '<script src="assets/obsidian_aura_engine.js"></script>'

    if css_mobile not in content:
        content = content.replace('</head>', f'    {css_mobile}\n</head>')
    if css_aura not in content:
        content = content.replace('</head>', f'    {css_aura}\n</head>')
    if js_aura not in content:
        content = content.replace('</body>', f'    {js_aura}\n</body>')

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

def run_sync():
    root_dir = r"C:\Users\willo\OneDrive\Desktop\Anthony_Ai"

    # 1. Target all HTML files in root
    html_files = glob.glob(os.path.join(root_dir, "*.html"))
    for hf in html_files:
        inject_mobile_assets(hf)

    # 2. Sync assets directory to app and edge
    import shutil
    targets = [
        os.path.join(root_dir, "app", "src", "main", "assets"),
        os.path.join(root_dir, "obsidian_edge_root")
    ]

    src_css_mobile = os.path.join(root_dir, "assets", "obsidian_mobile_core.css")
    src_css_aura = os.path.join(root_dir, "assets", "obsidian_aura_ui.css")
    src_js_aura = os.path.join(root_dir, "assets", "obsidian_aura_engine.js")

    for t in targets:
        if os.path.exists(t):
            # Ensure assets folder exists in target
            t_assets = os.path.join(t, "assets")
            os.makedirs(t_assets, exist_ok=True)

            # Copy Assets
            shutil.copy2(src_css_mobile, os.path.join(t_assets, "obsidian_mobile_core.css"))
            shutil.copy2(src_css_aura, os.path.join(t_assets, "obsidian_aura_ui.css"))
            shutil.copy2(src_js_aura, os.path.join(t_assets, "obsidian_aura_engine.js"))

            # Sync all HTML files to target root
            for hf in html_files:
                shutil.copy2(hf, t)

            print(f"[+] Synced Mobile Assets to: {t}")

if __name__ == "__main__":
    run_sync()
