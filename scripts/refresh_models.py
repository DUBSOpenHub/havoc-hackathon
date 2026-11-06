#!/usr/bin/env python3
"""Render exact runtime model IDs; use public documentation for discovery only."""

import argparse
import copy
import datetime as dt
import json
import re
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONFIG = ROOT / "config" / "models.json"
RUNTIME = ROOT / "config" / "runtime-models.json"
DOCS_API = (
    "https://docs.github.com/api/article/body"
    "?pathname=/en/copilot/reference/ai-models/supported-models"
)
TARGETS = [
    ROOT / "skills" / "havoc-hackathon" / "SKILL.md",
    ROOT / ".github" / "skills" / "havoc-hackathon" / "SKILL.md",
    ROOT / "agents" / "havoc-hackathon.agent.md",
    ROOT / "README.md",
]
BEGIN = "<!-- BEGIN GENERATED MODEL ROSTER -->"
END = "<!-- END GENERATED MODEL ROSTER -->"


def clean_name(value):
    value = re.sub(r"\[\^[^\]]+\]", "", value)
    return re.sub(r"<[^>]+>", "", value).strip()


def docs_models(markdown):
    heading = "## Supported AI models in Copilot"
    if heading not in markdown:
        raise ValueError("Supported-model section missing; refusing discovery")
    section = markdown.split(heading, 1)[1].split("\n## ", 1)[0]
    names = []
    for line in section.splitlines():
        cells = [clean_name(cell) for cell in line.strip().strip("|").split("|")]
        if line.startswith("|") and len(cells) == 3 and cells[2] in ("GA", "Public preview"):
            names.append(cells[0])
    if not names or any(not name for name in names) or len(names) != len(set(names)):
        raise ValueError("Empty or duplicate supported-model rows")
    return names


def validate_models(models):
    if not isinstance(models, list) or not models:
        raise ValueError("Runtime roster must be a non-empty list")
    ids = set()
    for model in models:
        if not isinstance(model, dict):
            raise ValueError("Model entries must be objects")
        for field in ("name", "id", "provider"):
            value = model.get(field)
            if not isinstance(value, str) or not value.strip() or any(c in value for c in "|\n\r`"):
                raise ValueError(f"Invalid model {field}")
        if model["id"] == "auto" or model["id"] in ids:
            raise ValueError("Duplicate or automatic model ID")
        if model.get("tier") not in ("Standard", "Premium"):
            raise ValueError("Invalid local lineup tier")
        for field in ("max_reasoning", "long_context"):
            if type(model.get(field)) is not bool:
                raise ValueError(f"Invalid capability: {field}")
        ids.add(model["id"])


def validate_config(config):
    validate_models(config["models"])
    dt.date.fromisoformat(config["updated"])
    by_id = {model["id"]: model for model in config["models"]}
    for tier in ("standard", "premium"):
        contestants = config["defaults"][tier + "_contestants"]
        judges = config["defaults"][tier + "_judges"]
        for panel in (contestants, judges):
            if len(panel) != 3 or len(set(panel)) != 3 or any(m not in by_id for m in panel):
                raise ValueError("Defaults require three distinct known model IDs")
            if len({by_id[m]["provider"] for m in panel}) < 2:
                raise ValueError("Default panel requires at least two providers")
        if set(contestants) & set(judges):
            raise ValueError("Default judge/contestant overlap")


def runtime_config(config, runtime):
    validate_models(runtime["models"])
    dt.date.fromisoformat(runtime["observed"])
    result = copy.deepcopy(config)
    result["models"] = sorted(
        runtime["models"], key=lambda item: (item["tier"] != "Premium", item["name"])
    )
    result["updated"] = runtime["observed"]
    result["docs_source"] = "https://docs.github.com/en/copilot/reference/ai-models/supported-models"
    result["source"] = "config/runtime-models.json"
    result["runtime_source"] = runtime["source"]
    validate_config(result)
    return result


def discover(config):
    request = urllib.request.Request(DOCS_API, headers={"User-Agent": "havoc-hackathon-model-refresh"})
    with urllib.request.urlopen(request, timeout=30) as response:
        names = docs_models(response.read().decode("utf-8"))
    known = {model["name"] for model in config["models"]}
    print("Docs-only names (not dispatchable until verified in the runtime schema): "
          + ", ".join(sorted(set(names) - known)))
    return config


def roster_block(config):
    validate_config(config)
    names = {item["id"]: item["name"] for item in config["models"]}
    lines = [
        BEGIN,
        f"_Runtime schema snapshot: {config['updated']} ({len(names)} explicit models). "
        "Recheck the current task schema before dispatch; no live probes implied._",
        "",
        "_Standard/Premium are local lineup labels, not billing categories. "
        "Custom provider IDs are environment-specific._",
        "",
        "| Display Name | Model ID | Tier |",
        "|-------------|----------|------|",
    ]
    lines.extend(
        f"| {item['name']} | `{item['id']}` | {item['tier']} |"
        for item in config["models"]
    )
    for tier, label in (("standard", "Standard"), ("premium", "Premium")):
        for role, noun in (("contestants", "contestants"), ("judges", "judges")):
            values = ", ".join(names[value] for value in config["defaults"][tier + "_" + role])
            lines.append(f"\n**Default {noun} ({label} lineup):** {values}")
    lines.append(END)
    return "\n".join(lines)


def planned_updates(config, targets=None):
    block = roster_block(config)
    updates = {}
    for target in TARGETS if targets is None else targets:
        resolved = target.resolve(strict=True)
        if not resolved.is_relative_to(ROOT.resolve()):
            raise ValueError(f"Roster target escapes project: {target}")
        text = resolved.read_text(encoding="utf-8")
        if text.count(BEGIN) != 1 or text.count(END) != 1 or text.index(BEGIN) > text.index(END):
            raise ValueError(f"Expected exactly one ordered roster marker pair: {target}")
        start, end = text.index(BEGIN), text.index(END) + len(END)
        updates[resolved] = text[:start] + block + text[end:]
    return updates


def render(config, check=False):
    updates = planned_updates(config)
    stale = [str(path.relative_to(ROOT)) for path, text in updates.items()
             if path.read_text(encoding="utf-8") != text]
    if check and stale:
        raise ValueError("Stale generated rosters: " + ", ".join(stale))
    if not check:
        for path, text in updates.items():
            path.write_text(text, encoding="utf-8")
    return updates


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--discover", action="store_true", help="Report public Docs candidates; never invent IDs")
    parser.add_argument("--check", action="store_true", help="Fail on stale generated files without writing")
    parser.add_argument("--runtime-models", type=Path, default=RUNTIME,
                        help="Reviewed snapshot of exact task schema IDs and capabilities")
    args = parser.parse_args()
    old = json.loads(CONFIG.read_text(encoding="utf-8"))
    runtime = json.loads(args.runtime_models.read_text(encoding="utf-8"))
    config = runtime_config(old, runtime)
    if args.discover:
        discover(config)
    updates = planned_updates(config)
    serialized = json.dumps(config, indent=2) + "\n"
    if args.check:
        if CONFIG.read_text(encoding="utf-8") != serialized:
            raise ValueError("Model config differs from runtime snapshot")
        render(config, check=True)
    else:
        # All inputs and marker pairs are validated before the first write.
        for path, text in updates.items():
            path.write_text(text, encoding="utf-8")
        CONFIG.write_text(serialized, encoding="utf-8")


if __name__ == "__main__":
    main()
