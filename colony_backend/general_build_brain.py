# --- ANTHONY'S CENTRAL BRAIN: UNIVERSAL AUTONOMOUS BUILD BRAIN v5.0 ---
import os
import sys
import json
import uuid
import time
import asyncio
import re
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from pathlib import Path

from colony_logger import colony_log
from colony_persistence import db
from dotenv import load_dotenv

load_dotenv(dotenv_path=Path(__file__).resolve().parent.parent / ".env")

SECURE_DIR = Path(r"D:\ObsidianAi_Colony\Secure_Assets")
BUILD_VAULT = SECURE_DIR / "project_builds"
SYSTEM_MEMORY_VAULT = SECURE_DIR / "system_memory"
BUILD_VAULT.mkdir(parents=True, exist_ok=True)
SYSTEM_MEMORY_VAULT.mkdir(parents=True, exist_ok=True)

# ============================================================
# 1. UNIVERSAL BUILD STATE & CONTRACT SCHEMAS
# ============================================================

class TaskItem(BaseModel):
    task_id: str
    description: str
    assigned_agent: str
    status: str = "negotiating"   # "negotiating", "in_progress", "completed", "failed"
    result: Optional[Dict[str, Any]] = None

class BuildState(BaseModel):
    project_id: str
    objective: str
    domain_type: str          # "video_gen", "marketplace", "game", "data_analysis", "web_app", "code_fix"
    requirements: List[str] = Field(default_factory=list)
    constraints: List[str] = Field(default_factory=list)
    files_affected: List[str] = Field(default_factory=list)
    architecture: Dict[str, Any] = Field(default_factory=dict)
    tasks: List[TaskItem] = Field(default_factory=list)
    agents_allocated: List[str] = Field(default_factory=list)
    tool_calls: List[Dict[str, Any]] = Field(default_factory=list)
    tests: List[Dict[str, Any]] = Field(default_factory=list)
    errors: List[Dict[str, Any]] = Field(default_factory=list)
    decisions: List[str] = Field(default_factory=list)
    artifacts: List[str] = Field(default_factory=list)
    qa_report: Dict[str, Any] = Field(default_factory=dict)
    status: str = "planning"   # "planning", "executing", "testing", "completed", "escalated"

# ============================================================
# 2. DOMAIN-SPECIFIC AGENT COLONY SELECTOR
# ============================================================

DOMAIN_COLONY_ROSTER = {
    "video_gen": ["StoryDirectorV2", "VisualDirectorV4", "PipelineAssembler", "YouTubePublisher"],
    "marketplace": ["SquareGateway", "CommerceCore", "PrintfulSync", "AffiliateSniper"],
    "game": ["GameRewardsBot", "HumanStealthHelper", "CookieMonsterVault"],
    "data_analysis": ["TauricResearchEngine", "MasterScraper", "AnalyticsNode"],
    "web_app": ["VercelDeployer", "FastMCPGateway", "SupabaseStorage"],
    "code_fix": ["SelfHealer", "QualityGate", "PipelineAssembler"]
}

class UniversalBuildBrain:
    """
    ANTHONY'S CENTRAL BUILD BRAIN v5.0:
    Project-Agnostic Autonomous Orchestrator that takes ANY project idea,
    analyzes intent, selects the agent colony, manages build_state, executes, tests,
    and escalates to OpenRouter 70B if local retries fail.
    """
    def classify_intent(self, user_goal: str) -> str:
        """Categorizes user intent into domain type."""
        goal_lower = user_goal.lower()
        if "video" in goal_lower or "movie" in goal_lower or "short" in goal_lower or "story" in goal_lower:
            return "video_gen"
        elif "store" in goal_lower or "shop" in goal_lower or "product" in goal_lower or "square" in goal_lower or "pay" in goal_lower:
            return "marketplace"
        elif "game" in goal_lower or "reward" in goal_lower or "survey" in goal_lower:
            return "game"
        elif "data" in goal_lower or "trade" in goal_lower or "crypto" in goal_lower or "market" in goal_lower:
            return "data_analysis"
        elif "site" in goal_lower or "web" in goal_lower or "app" in goal_lower or "portal" in goal_lower:
            return "web_app"
        else:
            return "code_fix"

    def create_project_build(self, user_goal: str) -> BuildState:
        project_id = f"build_{uuid.uuid4().hex[:8]}"
        domain = self.classify_intent(user_goal)
        colony_agents = DOMAIN_COLONY_ROSTER.get(domain, DOMAIN_COLONY_ROSTER["code_fix"])

        colony_log(f"BUILD_BRAIN: Analyzing objective [{user_goal[:35]}...] -> Domain: [{domain.upper()}]", node="BUILD_BRAIN")

        t1 = TaskItem(task_id="t1_research", description="Analyze requirements and local file context", assigned_agent=colony_agents[0])
        t2 = TaskItem(task_id="t2_execute", description="Execute core build & code modifications", assigned_agent=colony_agents[1] if len(colony_agents) > 1 else colony_agents[0])
        t3 = TaskItem(task_id="t3_test_qa", description="Run automated tests and QA validation gate", assigned_agent="QualityGate")

        state = BuildState(
            project_id=project_id,
            objective=user_goal,
            domain_type=domain,
            requirements=[f"Build {domain} solution matching user intent"],
            agents_allocated=colony_agents,
            tasks=[t1, t2, t3],
            decisions=[f"Allocated agent colony: {', '.join(colony_agents)}"],
            status="planning"
        )

        # Save Project State
        out_file = BUILD_VAULT / f"{project_id}.json"
        with open(out_file, "w") as f:
            f.write(state.model_dump_json(indent=4))

        db.log_event("BUILD_BRAIN", "PROJECT_BUILD_CREATED", {
            "project_id": project_id,
            "domain": domain,
            "agents_allocated": colony_agents,
            "vault_path": str(out_file)
        })

        colony_log(f" BUILD_BRAIN SUCCESS: Project [{project_id}] created for domain [{domain}]!", node="BUILD_BRAIN")
        return state

    def translate_to_human_explanation(self, state: BuildState) -> str:
        """Translates internal structured build_state into warm, natural human explanation for user."""
        return (
            f"I analyzed your request and set up a custom build plan for **{state.objective}**.\n\n"
            f" **Domain Category:** {state.domain_type.upper().replace('_', ' ')}\n"
            f" **Allocated Agent Colony:** {', '.join(state.agents_allocated)}\n"
            f" **Active Tasks:** {len(state.tasks)} steps queued for execution and testing.\n\n"
            f"The team is ready to execute and test the build automatically!"
        )

build_brain = UniversalBuildBrain()

if __name__ == "__main__":
    b1 = build_brain.create_project_build("Build me an AI video generator")
    print(build_brain.translate_to_human_explanation(b1))
    print("\n---")
    b2 = build_brain.create_project_build("Fix this broken Python backend")
    print(build_brain.translate_to_human_explanation(b2))
