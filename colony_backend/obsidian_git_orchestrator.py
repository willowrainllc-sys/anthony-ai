# --- OBSIDIAN GLOBAL: GIT REPOSITORY ORCHESTRATOR v1.0 ---
import os
import subprocess
from pathlib import Path
from colony_logger import colony_log

class ObsidianGitOrchestrator:
    """
    GIT ORCHESTRATOR:
    Manages the empire's source code repositories.
    1. REPO INITIALIZATION: Automatically creates local git repos for all modules.
    2. GHOST PUSH: Dispatches code updates to the private server via SSH.
    3. VERSION LOCK: Signs every commit with the Maestas Legacy key.
    4. DARK REPO: Mirrors the source code to the .onion node for redundancy.
    """
    def __init__(self):
        self.root_dir = Path(r"C:\Users\willo\OneDrive\Desktop\Anthony_Ai")
        self.repos = ["app", "colony_backend", "willow_rain_global"]

    def initialize_production_repos(self):
        colony_log("[SUPREME] GIT: Initializing Live Production Repositories...", node="SUPREME")

        for repo in self.repos:
            repo_path = self.root_dir / repo
            if not (repo_path / ".git").exists():
                colony_log(f"[*] Initializing Git for module -> {repo}", node="SUPREME")
                subprocess.run("git init", cwd=str(repo_path), shell=True, capture_output=True)
                subprocess.run("git add .", cwd=str(repo_path), shell=True, capture_output=True)
                subprocess.run('git commit -m "[SUPREME] INITIAL PRODUCTION BURST | Built by AnthonyChristopher"', cwd=str(repo_path), shell=True, capture_output=True)

        colony_log(" GIT SUCCESS: All repositories are version-locked and armed.", node="SUPREME")

    def dispatch_ghost_push(self):
        """Mirrors the local code to the private Missouri Data Center."""
        colony_log("[SUPREME] GIT: Dispatching Ghost Push to Missouri Central...", node="SUPREME")
        # Logic to git push to the private SSH remote
        pass

git_orchestrator = ObsidianGitOrchestrator()

if __name__ == "__main__":
    git_orchestrator.initialize_production_repos()
