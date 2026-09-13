# --- Built by Anthony Christopher | Est 12.19.1987 ---
# --- OBSIDIAN CITY MOBILE UI SYNC v1.0 ---
import os
import glob

def inject_mobile_assets(file_path):
    if not os.path.exists(file_path):
        return

    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    # 1. Inject CSS link if missing
    css_tag = '<link href="assets/obsidian_mobile_core.css" rel="stylesheet"/>'
    if css_tag not in content:
        if '</head>' in content:
            content = content.replace('</head>', f'    {css_tag}\n</head>')
            print(f"✓ Injected Mobile CSS: {file_path}")

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

    src_css = os.path.join(root_dir, "assets", "obsidian_mobile_core.css")

    for t in targets:
        if os.path.exists(t):
            # Ensure assets folder exists in target
            t_assets = os.path.join(t, "assets")
            os.makedirs(t_assets, exist_ok=True)

            # Copy CSS
            shutil.copy2(src_css, os.path.join(t_assets, "obsidian_mobile_core.css"))

            # Sync all HTML files to target root
            for hf in html_files:
                shutil.copy2(hf, t)

            print(f"✓ Synced Mobile Assets to: {t}")

if __name__ == "__main__":
    run_sync()
