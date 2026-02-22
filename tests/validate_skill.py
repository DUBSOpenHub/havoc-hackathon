#!/usr/bin/env python3
"""
Havoc Hackathon — SKILL.md & Agent Structural Validator

Parses SKILL.md and agent.md to verify structural integrity:
- All 9 phases present (0-8)
- SQL CREATE TABLE statements present and consistent
- Model roster matches between files
- Anti-gaming rules are concrete (not just listed)
- Evolution Brief format spec exists
- Bracket distribution table exists
- Dry-run / preflight section exists
- No stale claims (model counts, agent counts)

Exit code 0 = all checks pass, 1 = failures found.
"""

import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

SKILL_PATH = REPO_ROOT / "skills" / "havoc-hackathon" / "SKILL.md"
AGENT_PATH = REPO_ROOT / "agents" / "havoc-hackathon.agent.md"
SKILL_COPY_PATH = REPO_ROOT / ".github" / "skills" / "havoc-hackathon" / "SKILL.md"
README_PATH = REPO_ROOT / "README.md"
CATALOG_PATH = REPO_ROOT / "skills" / "havoc-hackathon" / "catalog.yml"

REQUIRED_PHASES = [
    "Phase 0", "Phase 1", "Phase 2", "Phase 3",
    "Phase 4", "Phase 5", "Phase 6", "Phase 7", "Phase 8",
]

REQUIRED_SQL_TABLES = [
    "hackathon_model_elo",
    "hackathon_model_perf",
    "hackathon_execution",
    "hackathon_metrics",
    "hackathon_quality_gates",
    "hackathon_integrity_flags",
    "hackathon_judge_scores",
    "hackathon_consensus",
    "hackathon_results",
    "hackathon_tournament",
]

REQUIRED_SECTIONS = [
    "Evolution Brief Format",
    "Bracket Distribution",
    "Anti-gaming",
    "Ensemble Synthesis",
    "Dry-Run",
    "Preflight",
]


class ValidationResult:
    def __init__(self):
        self.passed = []
        self.failed = []
        self.warnings = []

    def ok(self, msg):
        self.passed.append(msg)

    def fail(self, msg):
        self.failed.append(msg)

    def warn(self, msg):
        self.warnings.append(msg)

    @property
    def success(self):
        return len(self.failed) == 0

    def report(self):
        print("\n🧪 Havoc Hackathon — Structural Validation")
        print("=" * 55)

        for msg in self.passed:
            print(f"  ✅ {msg}")
        for msg in self.warnings:
            print(f"  ⚠️  {msg}")
        for msg in self.failed:
            print(f"  ❌ {msg}")

        total = len(self.passed) + len(self.failed)
        print(f"\n  Results: {len(self.passed)}/{total} passed", end="")
        if self.warnings:
            print(f", {len(self.warnings)} warnings", end="")
        print()

        if self.success:
            print("  🎉 All checks passed!\n")
        else:
            print(f"  💥 {len(self.failed)} check(s) failed.\n")

        return self.success


def read_file(path):
    if not path.exists():
        return None
    return path.read_text(encoding="utf-8")


def check_phases(content, filename, result):
    """Verify all 9 phases are present."""
    for phase in REQUIRED_PHASES:
        if phase in content:
            result.ok(f"[{filename}] {phase} present")
        else:
            result.fail(f"[{filename}] {phase} MISSING")


def check_sql_tables(content, filename, result):
    """Verify SQL CREATE TABLE statements for all required tables."""
    has_create = "CREATE TABLE" in content
    if not has_create:
        result.fail(f"[{filename}] No CREATE TABLE statements found")
        return

    result.ok(f"[{filename}] CREATE TABLE statements present")

    for table in REQUIRED_SQL_TABLES:
        if table in content:
            result.ok(f"[{filename}] SQL table '{table}' defined")
        else:
            result.fail(f"[{filename}] SQL table '{table}' MISSING")


def check_required_sections(content, filename, result):
    """Verify key specification sections exist."""
    for section in REQUIRED_SECTIONS:
        if section.lower() in content.lower():
            result.ok(f"[{filename}] Section '{section}' present")
        else:
            result.fail(f"[{filename}] Section '{section}' MISSING")


def check_anti_gaming_concrete(content, filename, result):
    """Verify anti-gaming rules have concrete implementation, not just labels."""
    concrete_markers = [
        "calibration anchor",
        "keyword stuffing",
        "test tampering",
        "prompt injection",
    ]
    action_markers = ["deduct", "DQ", "discard", "flag", "reject", "re-judge"]

    has_concrete = sum(1 for m in concrete_markers if m.lower() in content.lower())
    has_actions = sum(1 for m in action_markers if m.lower() in content.lower())

    if has_concrete >= 3 and has_actions >= 3:
        result.ok(f"[{filename}] Anti-gaming rules are concrete ({has_concrete} checks, {has_actions} actions)")
    elif has_concrete >= 3 and has_actions < 3:
        result.fail(f"[{filename}] Anti-gaming checks listed but lack concrete actions (only {has_actions} action verbs)")
    else:
        result.fail(f"[{filename}] Anti-gaming rules incomplete ({has_concrete}/4 checks)")


def check_model_roster(content, filename, result):
    """Verify model roster is present and has expected model count."""
    model_ids = re.findall(r"`(claude-[a-z0-9.-]+|gpt-[a-z0-9.-]+|gemini-[a-z0-9.-]+)`", content)
    unique_models = set(model_ids)

    if len(unique_models) >= 10:
        result.ok(f"[{filename}] Model roster has {len(unique_models)} unique models")
    else:
        result.warn(f"[{filename}] Model roster has only {len(unique_models)} unique models (expected ≥10)")


def check_model_count_claims(content, filename, result):
    """Detect stale model count claims."""
    # Count models in the Available Models table
    model_table_match = re.findall(r"\| .+ \| `[a-z].*` \| (Premium|Standard) \|", content)
    table_count = len(model_table_match)

    # Check for numeric claims about model counts
    count_claims = re.findall(r"(\d+)\s+models?", content.lower())
    for claim in count_claims:
        claimed = int(claim)
        if claimed > 20 and table_count > 0:
            result.warn(f"[{filename}] Claims '{claimed} models' but table has {table_count}")


def check_files_in_sync(result):
    """Verify SKILL.md copies are identical."""
    skill = read_file(SKILL_PATH)
    copy = read_file(SKILL_COPY_PATH)

    if skill is None:
        result.fail("Canonical SKILL.md not found")
        return
    if copy is None:
        result.fail(".github/skills SKILL.md copy not found")
        return

    if skill == copy:
        result.ok("SKILL.md copies are in sync")
    else:
        result.fail("SKILL.md copies have drifted!")


def check_readme_model_table(result):
    """Verify README model table exists and has reasonable count."""
    readme = read_file(README_PATH)
    if readme is None:
        result.warn("README.md not found")
        return

    readme_models = re.findall(r"\| .+ \| `(claude-[a-z0-9.-]+|gpt-[a-z0-9.-]+|gemini-[a-z0-9.-]+)` \|", readme)
    skill = read_file(SKILL_PATH)
    skill_models = re.findall(r"\| .+ \| `(claude-[a-z0-9.-]+|gpt-[a-z0-9.-]+|gemini-[a-z0-9.-]+)` \|", skill) if skill else []

    if set(readme_models) == set(skill_models):
        result.ok(f"README and SKILL.md model tables match ({len(readme_models)} models)")
    elif abs(len(readme_models) - len(skill_models)) <= 1:
        result.warn(f"README has {len(readme_models)} models, SKILL.md has {len(skill_models)} — close but not exact")
    else:
        result.fail(f"README has {len(readme_models)} models but SKILL.md has {len(skill_models)} — OUT OF SYNC")


def check_bracket_table(content, filename, result):
    """Verify bracket distribution table has entries for key model counts."""
    key_counts = ["14", "12", "9", "7", "5"]
    found = 0
    for count in key_counts:
        pattern = rf"\|\s*{count}\s*\|"
        if re.search(pattern, content):
            found += 1

    if found >= 4:
        result.ok(f"[{filename}] Bracket table covers {found}/{len(key_counts)} key model counts")
    else:
        result.fail(f"[{filename}] Bracket table only covers {found}/{len(key_counts)} key model counts")


def main():
    result = ValidationResult()

    skill = read_file(SKILL_PATH)
    agent = read_file(AGENT_PATH)

    if skill is None:
        result.fail("SKILL.md not found at skills/havoc-hackathon/SKILL.md")
        result.report()
        return 1

    if agent is None:
        result.fail("agent.md not found at agents/havoc-hackathon.agent.md")
        result.report()
        return 1

    # Phase checks
    check_phases(skill, "SKILL.md", result)
    check_phases(agent, "agent.md", result)

    # SQL table checks
    check_sql_tables(skill, "SKILL.md", result)
    check_sql_tables(agent, "agent.md", result)

    # Required sections
    check_required_sections(skill, "SKILL.md", result)
    check_required_sections(agent, "agent.md", result)

    # Anti-gaming concrete checks
    check_anti_gaming_concrete(skill, "SKILL.md", result)
    check_anti_gaming_concrete(agent, "agent.md", result)

    # Model roster
    check_model_roster(skill, "SKILL.md", result)
    check_model_roster(agent, "agent.md", result)

    # Stale claim detection
    check_model_count_claims(skill, "SKILL.md", result)
    check_model_count_claims(agent, "agent.md", result)

    # File sync
    check_files_in_sync(result)

    # README consistency
    check_readme_model_table(result)

    # Bracket table coverage
    check_bracket_table(skill, "SKILL.md", result)
    check_bracket_table(agent, "agent.md", result)

    success = result.report()
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
