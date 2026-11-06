#!/usr/bin/env python3
"""
Havoc Hackathon — Preflight Validator (offline checks)

Validates everything that can be checked without live model access:
- SQL CREATE TABLE statements parse correctly
- Bracket math is consistent
- File structure is complete
- ELO persistence file format (if exists)

Run with: python3 tests/preflight.py
"""

import argparse
import json
import re
import sqlite3
import sys
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))
from hackathon_rules import bracket_sizes, validate_elo_data

SKILL_PATH = REPO_ROOT / "skills" / "havoc-hackathon" / "SKILL.md"

def documented_brackets(content):
    return {
        int(count): (int(heats), [int(n) for n in distribution.split("-")], int(finalists))
        for count, heats, distribution, finalists in re.findall(
            r"^\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*([\d-]+)\s*\|\s*(\d+)\s*\|",
            content, re.MULTILINE
        )
    }

REQUIRED_FILES = [
    "skills/havoc-hackathon/SKILL.md",
    "agents/havoc-hackathon.agent.md",
    "agents/grid-medic.agent.md",
    ".github/skills/havoc-hackathon/SKILL.md",
    "skills/havoc-hackathon/catalog.yml",
    "README.md",
    "LICENSE",
    "SECURITY.md",
    "TESTING.md",
    "CHANGELOG.md",
    "CONTRIBUTING.md",
    "CODE_OF_CONDUCT.md",
]


def check_sql_statements():
    """Extract and validate all CREATE TABLE statements from SKILL.md."""
    content = SKILL_PATH.read_text(encoding="utf-8")

    # Extract SQL blocks
    sql_blocks = re.findall(r"```sql\n(.*?)```", content, re.DOTALL)
    if not sql_blocks:
        return False, "No SQL code blocks found in SKILL.md"

    all_sql = "\n".join(sql_blocks)
    statements = [s.strip() for s in all_sql.split(";") if s.strip().startswith("CREATE")]

    if len(statements) < 10:
        return False, f"Only {len(statements)} CREATE TABLE statements found (expected 10)"

    # Try executing them in a temp database
    try:
        with tempfile.NamedTemporaryFile(suffix=".db") as tmp:
            conn = sqlite3.connect(tmp.name)
            for stmt in statements:
                conn.execute(stmt + ";")
            conn.commit()

            # Verify tables exist
            cursor = conn.execute(
                "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
            )
            tables = [row[0] for row in cursor.fetchall() if row[0].startswith("hackathon_")]
            conn.close()

            expected = re.findall(r"CREATE TABLE IF NOT EXISTS (hackathon_\w+)", content)
            if set(tables) == set(expected) and len(tables) == len(expected):
                return True, f"All {len(tables)} tables created successfully: {', '.join(tables)}"
            else:
                return False, f"Only {len(tables)} tables created: {', '.join(tables)}"
    except sqlite3.Error as e:
        return False, f"SQL parse error: {e}"


def check_bracket_math():
    """Verify bracket distribution math is consistent."""
    errors = []
    rules = documented_brackets(SKILL_PATH.read_text(encoding="utf-8"))
    if not rules:
        return False, "No documented brackets found"
    for n, (heats, dist, finalists) in rules.items():
        if sum(dist) != n:
            errors.append(f"N={n}: distribution {dist} sums to {sum(dist)}, expected {n}")
        if len(dist) != heats:
            errors.append(f"N={n}: {len(dist)} distributions but {heats} heats declared")
        if finalists != heats:
            errors.append(f"N={n}: {finalists} finalists but {heats} heats (expect 1 per heat)")
        if dist != bracket_sizes(n):
            errors.append(f"N={n}: documented distribution differs from ceil(N/4) rule")

    if errors:
        return False, "; ".join(errors)
    return True, f"Bracket math verified against the skill for {len(rules)} model counts"


def check_file_structure():
    """Verify all required files exist."""
    missing = []
    for rel_path in REQUIRED_FILES:
        full_path = REPO_ROOT / rel_path
        if not full_path.exists():
            missing.append(rel_path)

    if missing:
        return False, f"Missing files: {', '.join(missing)}"
    return True, f"All {len(REQUIRED_FILES)} required files present"


def check_elo_file(path=None):
    """Use a legacy mock by default; real ratings inspection is explicit."""
    try:
        data = json.loads(path.read_text(encoding="utf-8")) if path else {
            "models": {"historical-model": {"elo": 1500, "wins": 2, "losses": 1, "total": 2}},
            "updated": "2026-11-05T00:00:00Z",
        }
        validate_elo_data(data)
    except (ValueError, OSError) as error:
        return False, f"Invalid ELO data: {error}"
    return True, f"{'Explicit read-only file' if path else 'Legacy mock'} valid; real ratings unchanged"


def main():
    parser = argparse.ArgumentParser(description="Offline Havoc Hackathon preflight")
    parser.add_argument("--elo-file", type=Path, help="Explicit read-only inspection; defaults to a mock")
    args = parser.parse_args()
    print("\n🔧 PREFLIGHT CHECK — Havoc Hackathon (Offline)")
    print("=" * 50)

    checks = [
        ("File structure", check_file_structure),
        ("SQL statements", check_sql_statements),
        ("Bracket math", check_bracket_math),
        ("ELO persistence", lambda: check_elo_file(args.elo_file)),
    ]

    all_pass = True
    for name, fn in checks:
        try:
            passed, msg = fn()
        except Exception as e:
            passed, msg = False, f"Unexpected error: {e}"

        icon = "✅" if passed else "❌"
        print(f"  {icon} {name}: {msg}")
        if not passed:
            all_pass = False

    print()
    if all_pass:
        print("  RESULT: ✅ OFFLINE CHECKS PASSED — live model availability not checked")
    else:
        print("  RESULT: ❌ ISSUES FOUND — see above")

    print()
    return 0 if all_pass else 1


if __name__ == "__main__":
    sys.exit(main())
