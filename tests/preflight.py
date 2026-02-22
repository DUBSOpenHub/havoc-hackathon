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

import json
import re
import sqlite3
import sys
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SKILL_PATH = REPO_ROOT / "skills" / "havoc-hackathon" / "SKILL.md"
ELO_PATH = Path.home() / ".copilot" / "hackathon-elo.json"

BRACKET_RULES = {
    14: (4, [4, 4, 3, 3], 4),
    12: (4, [3, 3, 3, 3], 4),
    11: (3, [4, 4, 3], 3),
    10: (3, [4, 3, 3], 3),
    9:  (3, [3, 3, 3], 3),
    8:  (2, [4, 4], 2),
    7:  (2, [4, 3], 2),
    6:  (2, [3, 3], 2),
    5:  (2, [3, 2], 2),
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
            tables = [row[0] for row in cursor.fetchall()]
            conn.close()

            if len(tables) >= 10:
                return True, f"All {len(tables)} tables created successfully: {', '.join(tables)}"
            else:
                return False, f"Only {len(tables)} tables created: {', '.join(tables)}"
    except sqlite3.Error as e:
        return False, f"SQL parse error: {e}"


def check_bracket_math():
    """Verify bracket distribution math is consistent."""
    errors = []
    for n, (heats, dist, finalists) in BRACKET_RULES.items():
        if sum(dist) != n:
            errors.append(f"N={n}: distribution {dist} sums to {sum(dist)}, expected {n}")
        if len(dist) != heats:
            errors.append(f"N={n}: {len(dist)} distributions but {heats} heats declared")
        if finalists != heats:
            errors.append(f"N={n}: {finalists} finalists but {heats} heats (expect 1 per heat)")

    if errors:
        return False, "; ".join(errors)
    return True, f"Bracket math verified for {len(BRACKET_RULES)} model counts (5-14)"


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


def check_elo_file():
    """Validate ELO persistence file format if it exists."""
    if not ELO_PATH.exists():
        return True, "No ELO file yet (fresh start) — OK"

    try:
        data = json.loads(ELO_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        return False, f"ELO file is invalid JSON: {e}"

    if "models" not in data:
        return False, "ELO file missing 'models' key"
    if "updated" not in data:
        return False, "ELO file missing 'updated' key"

    for model_id, stats in data["models"].items():
        for key in ("elo", "wins", "losses", "total"):
            if key not in stats:
                return False, f"Model '{model_id}' missing '{key}' in ELO file"

    return True, f"ELO file valid with {len(data['models'])} models tracked"


def main():
    print("\n🔧 PREFLIGHT CHECK — Havoc Hackathon (Offline)")
    print("=" * 50)

    checks = [
        ("File structure", check_file_structure),
        ("SQL statements", check_sql_statements),
        ("Bracket math", check_bracket_math),
        ("ELO persistence", check_elo_file),
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
        print("  RESULT: ✅ READY — all offline checks passed")
    else:
        print("  RESULT: ❌ ISSUES FOUND — see above")

    print()
    return 0 if all_pass else 1


if __name__ == "__main__":
    sys.exit(main())
