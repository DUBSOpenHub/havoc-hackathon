"""Offline reference calculations shared by preflight and skill validation."""

import datetime as dt
import math
from collections import Counter
from itertools import combinations


def select_mode(challenge, explicit=None):
    if explicit is not None:
        if explicit not in {"classic", "tournament", "kiloagent", "metaswarm"}:
            raise ValueError("Unknown explicit mode")
        return explicit
    text = challenge.lower()
    complex_tasks = (
        "architecture", "multi-file feature", "full app", "system design",
        "security audit", "database performance", "performance optimization",
        "migration", "api design", "api gateway", "full rest api",
        "rewrite", "redesign", "full-stack", "cross-repo", "framework evaluation",
    )
    return "tournament" if any(term in text for term in complex_tasks) else "classic"


def bracket_sizes(count):
    if type(count) is not int or count < 0:
        raise ValueError("Model count must be a nonnegative integer")
    if count <= 4:
        return [count] if count else []
    heats = (count + 3) // 4
    base, remainder = divmod(count, heats)
    return [base + (index < remainder) for index in range(heats)]


def classify_votes(votes):
    if not votes:
        raise ValueError("Votes cannot be empty")
    counts = Counter(votes)
    highest = max(counts.values())
    if highest == 1:
        return "UNIQUE"
    if sum(value == highest for value in counts.values()) > 1:
        return "CONFLICT"
    return "CONSENSUS" if highest >= 3 else "PAIR AGREEMENT"


def finite_number(value):
    return type(value) in (int, float) and math.isfinite(value)


def validate_elo_data(data):
    if not isinstance(data, dict) or not isinstance(data.get("models"), dict):
        raise ValueError("Ratings require a models object")
    if not isinstance(data.get("updated"), str):
        raise ValueError("Ratings require an ISO timestamp")
    dt.datetime.fromisoformat(data["updated"].replace("Z", "+00:00"))
    for model, stats in data["models"].items():
        if not isinstance(model, str) or not model or not isinstance(stats, dict):
            raise ValueError("Invalid rating entry")
        if not finite_number(stats.get("elo")):
            raise ValueError("Rating must be finite")
        for field in ("wins", "losses", "total"):
            if type(stats.get(field)) is not int or stats[field] < 0:
                raise ValueError("Rating counts must be nonnegative integers")
        history = stats.get("recent_results", [])
        if not isinstance(history, list) or any(value not in ("win", "loss", "draw") for value in history):
            raise ValueError("Invalid ordered result history")
    receipts = data.get("applied_run_ids", [])
    if (not isinstance(receipts, list) or any(not isinstance(value, str) or not value for value in receipts)
            or len(receipts) != len(set(receipts))):
        raise ValueError("Invalid duplicate-run receipts")
    return data


def elo_updates(ratings, scores):
    if set(ratings) != set(scores):
        raise ValueError("Ratings and scores must identify the same submissions")
    if any(not finite_number(value) for value in [*ratings.values(), *scores.values()]):
        raise ValueError("Ratings and scores must be finite numbers")
    deltas = {model: 0.0 for model in ratings}
    for left, right in combinations(sorted(ratings), 2):
        exponent = max(-300, min(300, (ratings[right] - ratings[left]) / 400))
        expected = 1 / (1 + 10 ** exponent)
        actual = 0.5 if scores[left] == scores[right] else float(scores[left] > scores[right])
        delta = 32 * (actual - expected)
        deltas[left] += delta
        deltas[right] -= delta
    return {model: ratings[model] + deltas[model] for model in ratings}


def sideline_report(records, stage, decision="pending"):
    """Produce a checkpoint from observed receipts, never inferred progress."""
    allowed = {"queued", "running", "completed", "failed", "disqualified", "cancelled"}
    terminal = {"completed", "failed", "disqualified", "cancelled"}
    seen = set()
    rows = []
    for record in records:
        label = record["contestant"]
        status = record["status"]
        if not label or label in seen or status not in allowed:
            raise ValueError("Duplicate contestant or invalid observed status")
        if not record.get("evidence"):
            raise ValueError("Status requires a receipt or observed evidence")
        seen.add(label)
        score = record.get("score")
        if score is not None:
            if (status != "completed" or not finite_number(score) or not 0 <= score <= 50
                    or not record.get("score_evidence")):
                raise ValueError("Score requires completed work and valid judging evidence")
        rows.append({
            "contestant": label,
            "status": status,
            "score": score if score is not None else "pending",
            "strengths": record.get("strengths") or "pending",
            "weaknesses": record.get("weaknesses") or "pending",
            "evidence": record["evidence"],
        })
    finished = sum(row["status"] in terminal for row in rows)
    return {
        "stage": stage,
        "total": len(rows),
        "finished": finished,
        "successful": sum(row["status"] == "completed" for row in rows),
        "remaining": len(rows) - finished,
        "decision": decision,
        "contestants": rows,
    }
