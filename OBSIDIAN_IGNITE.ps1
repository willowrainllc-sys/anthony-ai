# --- OBSIDIAN GLOBAL: THE SOVEREIGN BURST STRING v1.0 ---
# Paste this into ANY PowerShell terminal to reactivate the empire.

$Host.UI.RawUI.WindowTitle = "🔱 OBSIDIAN GLOBAL: SYSTEM IGNITION 🔱"

Write-Host "====================================================" -ForegroundColor Blue
Write-Host "   🔱 OBSIDIAN GLOBAL: AUTOMATIC RE-BIRTH 🔱" -ForegroundColor Blue
Write-Host "===================================================="

# 1. Sync the Mind (Anthony ASI)
Write-Host "[*] Syncing Supreme Intelligence..."
if (!(Get-Command ollama -ErrorAction SilentlyContinue)) {
    Write-Host "[!] Ollama not found. Aborting Burst." -ForegroundColor Red
    exit
}
start-process ollama -ArgumentList "run anthony `"hello`"" -NoNewWindow

# 2. Ignite the Core (Command OS)
Write-Host "[*] Launching Obsidian-OS Kernel..."
start-process python -ArgumentList "C:\Users\willo\OneDrive\Desktop\Anthony_Ai\colony_backend\anthony_command_os.py" -NoNewWindow

# 3. Open the Portals
Write-Host "[*] Displaying Master Universe Dashboard..."
start "C:\Users\willo\OneDrive\Desktop\Anthony_Ai\obsidian_cloud\dashboard_ui\index.html"

Write-Host "===================================================="
Write-Host "  🔱 SUCCESS: EMPIRE IS ACTIVE AND ATTACKING. 🔱" -ForegroundColor Green
Write-Host "===================================================="
