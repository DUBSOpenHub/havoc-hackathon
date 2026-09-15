#!/usr/bin/env python3
"""Refresh and render the Havoc Hackathon model roster."""

import argparse
import datetime as dt
import json
import re
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONFIG = ROOT / "config" / "models.json"
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
EXCLUDED_NAMES = ("Claude Fable", "nano", "(fast mode)")


def clean_name(value):
    value = re.sub(r"\[\^[^\]]+\]", "", value)
    return re.sub(r"<[^>]+>", "", value).strip()


def model_id(name):
    value = name.lower().replace("gpt-5 mini", "gpt-5-mini")
    value = value.replace("mai-code", "mai-code")
    value = re.sub(r"[^a-z0-9.]+", "-", value).strip("-")
    return value


def infer_tier(name):
    premium_tokens = ("Opus", "GPT-6", "Terra", "GPT-5.5", "GPT-5.4", "Kimi K3", "Grok 4.6")
    return "Premium" if any(token in name for token in premium_tokens) else "Standard"


def docs_models(markdown):
    section = markdown.split("## Supported AI models in Copilot", 1)[1]
    section = section.split("## Supported AI models in Auto model selection", 1)[0]
    names = []
    for line in section.splitlines():
        match = re.match(r"^\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*GA\s*\|$", line)
        if not match:
            continue
        name = clean_name(match.group(1))
        if not name or name == "Model name" or any(token in name for token in EXCLUDED_NAMES):
            continue
        names.append(name)
    return names


def retired_models(markdown, today):
    if "## Model retirement history" not in markdown:
        return set()
    section = markdown.split("## Model retirement history", 1)[1]
    retired = set()
    for line in section.splitlines():
        match = re.match(r"^\|\s*([^|]+?)\s*\|\s*(\d{4}-\d{2}-\d{2})\s*\|", line)
        if match and dt.date.fromisoformat(match.group(2)) <= today:
            retired.add(clean_name(match.group(1)))
    return retired


def discover(config):
    request = urllib.request.Request(DOCS_API, headers={"User-Agent": "havoc-hackathon-model-refresh"})
    with urllib.request.urlopen(request, timeout=30) as response:
        markdown = response.read().decode("utf-8")

    today = dt.date.today()
    retired = retired_models(markdown, today)
    previous = {item["id"]: item for item in config["models"]}
    models = []
    for name in docs_models(markdown):
        if name in retired:
            continue
        identifier = model_id(name)
        old = previous.get(identifier)
        models.append({
            "name": name,
            "id": identifier,
            "tier": old["tier"] if old else infer_tier(name),
        })

    if len(models) < 10:
        raise RuntimeError(f"Refusing to replace roster with only {len(models)} discovered models")

    models.sort(key=lambda item: (item["tier"] != "Premium", item["name"]))
    config["models"] = models
    ids_by_tier = {
        tier: [item["id"] for item in models if item["tier"] == tier]
        for tier in ("Premium", "Standard")
    }
    default_tiers = {
        "standard_contestants": "Standard",
        "premium_contestants": "Premium",
        "standard_judges": "Premium",
        "premium_judges": "Standard",
    }
    for key, tier in default_tiers.items():
        available = ids_by_tier[tier]
        retained = [identifier for identifier in config["defaults"][key] if identifier in available]
        config["defaults"][key] = (retained + [identifier for identifier in available if identifier not in retained])[:3]
    config["updated"] = today.isoformat()
    return config


def render(config):
    names = {item["id"]: item["name"] for item in config["models"]}
    lines = [
        BEGIN,
        f"_Automatically refreshed from GitHub Docs. Last refresh: {config['updated']}._",
        "",
        "| Display Name | Model ID | Tier |",
        "|-------------|----------|------|",
    ]
    lines.extend(
        f"| {item['name']} | `{item['id']}` | {item['tier']} |"
        for item in config["models"]
    )
    defaults = config["defaults"]
    format_names = lambda key: ", ".join(names.get(value, value) for value in defaults[key])
    lines.extend([
        "",
        f"**Default contestants (Standard):** {format_names('standard_contestants')} ← STANDARD ⚡",
        f"**Default contestants (Premium):** {format_names('premium_contestants')} ← PREMIUM 👑",
        f"**Default judges (Standard):** {format_names('standard_judges')} ← STANDARD ⚡",
        f"**Default judges (Premium):** {format_names('premium_judges')} ← PREMIUM 👑",
        END,
    ])
    block = "\n".join(lines)

    for target in TARGETS:
        text = target.read_text(encoding="utf-8")
        pattern = re.compile(re.escape(BEGIN) + r".*?" + re.escape(END), re.DOTALL)
        if not pattern.search(text):
            raise RuntimeError(f"Generated model roster markers missing in {target}")
        target.write_text(pattern.sub(block, text), encoding="utf-8")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--discover", action="store_true", help="Refresh config from GitHub Docs")
    args = parser.parse_args()

    config = json.loads(CONFIG.read_text(encoding="utf-8"))
    if args.discover:
        config = discover(config)
        CONFIG.write_text(json.dumps(config, indent=2) + "\n", encoding="utf-8")
    render(config)


if __name__ == "__main__":
    main()
