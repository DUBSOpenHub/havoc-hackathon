#!/usr/bin/env python3
"""Havoc Hackathon — 22-second terminal demo animation.

Matches actual CLI output style: sequential text, emoji, no ANSI art.
github.com/DUBSOpenHub/havoc-hackathon
"""

import sys
import time
import re
import unicodedata

# ── minimal ANSI (terminal defaults only) ────────────────
RST  = "\033[0m"
BOLD = "\033[1m"
DIM  = "\033[2m"
WHT  = "\033[37;1m"
GRAY = "\033[90m"

HIDE = "\033[?25l"
SHOW = "\033[?25h"
CLR  = "\033[2J\033[H"

W = 66  # inner box width


# ── helpers ──────────────────────────────────────────────
def out(s="", end="\n"):
    sys.stdout.write(s + end)
    sys.stdout.flush()


def sl(t):
    time.sleep(t)


def vlen(s):
    """Visible width: strip ANSI, account for wide chars."""
    stripped = re.sub(r"\033\[[^m]*m", "", s)
    width = 0
    for ch in stripped:
        cat = unicodedata.east_asian_width(ch)
        width += 2 if cat in ("W", "F") else 1
    return width


def typer(text, delay=0.018):
    for ch in text:
        out(ch, end="")
        time.sleep(delay)
    out()


# ══════════════════════════════════════════════════════════
# PHASE 1 — BANNER                                  ~1.5 s
# ══════════════════════════════════════════════════════════
def p1_banner():
    out(HIDE, end="")
    out(CLR, end="")
    sl(0.15)
    out("╔══════════════════════════════════════════════════════════════════╗")
    sl(0.06)
    out("║              ⚡  H A V O C   H A C K A T H O N  ⚡              ║")
    sl(0.06)
    out("║                                                                  ║")
    sl(0.06)
    out("║  🏟️  THE ARENA IS READY. THE AI MODELS ARE READY TO COMPETE.  🏟️  ║")
    sl(0.06)
    out("╚══════════════════════════════════════════════════════════════════╝")
    sl(0.5)


# ══════════════════════════════════════════════════════════
# PHASE 2 — ELO LEADERBOARD                         ~3.5 s
# ══════════════════════════════════════════════════════════
def p2_leaderboard():
    out()
    out("📊 Current ELO Leaderboard (13 hackathons of history!)")
    out()
    sl(0.15)

    out(f" {BOLD}Rank   Model                        ELO      W-L     Record{RST}")
    out(f" {'─' * 62}")
    sl(0.1)

    rows = [
        (" 1.",  "GPT-5.5",               "1387",  "7-2",  "🔥 Hot streak"),
        (" 2.",  "Claude Opus 4.7",       "1355", "19-6",  "🔥 Hot streak"),
        (" 3.",  "Claude Sonnet 4.6",     "1286",  "9-4",  "📈 Rising"),
        (" 4.",  "Claude Opus 4.6",       "1262",  "6-2",  "💪 Strong"),
        (" 5.",  "GPT-5.4",               "1254",  "8-3",  "📈 Rising"),
        (" 6.",  "GPT-5.2",               "1251",  "8-5",  "⚡ Solid"),
        (" 7.",  "Claude Opus 4.6 (1M)",  "1248",  "7-5",  "⚡ Solid"),
        (" 8.",  "Claude Opus 4.7 (1M)",  "1210",  "4-2",  "🆕 New"),
        (" 9.",  "Claude Sonnet 4.5",     "1197",  "8-8",  "😐 .500"),
        ("10.",  "Claude Opus 4.5",       "1193",  "2-3",  "🆕 New"),
        ("11.",  "Codex GPT-5.3",         "1153", "6-11",  "📉 Slumping"),
        ("12.",  "Codex GPT-5.2",         "1116",  "1-7",  "🥶 Cold"),
        ("13.",  "Claude Sonnet 4",       "1069",  "0-9",  "💀 Winless"),
    ]

    for rank, model, elo, wl, record in rows:
        out(f" {rank}   {model:<25} {elo}   {wl:>5}   {record}")
        sl(0.2)

    sl(0.3)


# ══════════════════════════════════════════════════════════
# PHASE 3 — TOURNAMENT SETUP                        ~2.5 s
# ══════════════════════════════════════════════════════════
def p3_tournament():
    out()
    typer("🎯 TASK: Build a terminal demo animation", delay=0.015)
    sl(0.1)
    out(f"{DIM}Rubric: creativity · accuracy · style · wow · impact  (50 pts){RST}")
    sl(0.15)
    out()
    out(f"{BOLD}🏟️  TOURNAMENT MODE{RST} — 13 models → 4 heats → 4 finalists → 1 champion")
    sl(0.3)
    out()

    heats = [
        ("Heat 1", "Claude Opus 4.7, GPT-5.2, Codex GPT-5.2, Claude Sonnet 4"),
        ("Heat 2", "GPT-5.5, GPT-5.4, Claude Opus 4.5"),
        ("Heat 3", "Claude Opus 4.6, Claude Sonnet 4.5, Codex GPT-5.3"),
        ("Heat 4", "Claude Sonnet 4.6, Claude Opus 4.6 (1M), Claude Opus 4.7 (1M)"),
    ]
    for heat_name, models in heats:
        out(f"  {BOLD}{heat_name}:{RST} {models}")
        sl(0.18)

    sl(0.15)
    out()
    out("3... 2... 1... GO! 🏁")
    sl(0.4)


# ══════════════════════════════════════════════════════════
# PHASE 4 — HEAT RACES                              ~3.0 s
# ══════════════════════════════════════════════════════════
def p4_heats():
    out()
    out(f"{BOLD}⏱️  ROUND 1 — HEATS{RST}")
    out()

    heat_results = [
        ("Heat 1", [
            ("🔵 Claude Opus 4.7",     "✅  4s", "⚡ Speedrun!"),
            ("🟠 GPT-5.2",             "✅  7s", ""),
            ("🔴 Codex GPT-5.2",       "✅ 12s", ""),
            ("🔴 Claude Sonnet 4",     "✅ 15s", ""),
        ]),
        ("Heat 2", [
            ("🟢 GPT-5.5",             "✅  3s", "⚡"),
            ("🟠 GPT-5.4",             "✅  8s", ""),
            ("🔴 Claude Opus 4.5",     "✅ 14s", ""),
        ]),
        ("Heat 3", [
            ("🟡 Claude Opus 4.6",     "✅  6s", ""),
            ("🟠 Claude Sonnet 4.5",   "✅  9s", ""),
            ("🔴 Codex GPT-5.3",       "✅ 11s", "😬 Still cooking..."),
        ]),
        ("Heat 4", [
            ("🟣 Claude Sonnet 4.6",   "✅  5s", "⚡ Speedrun!"),
            ("🟠 Claude Opus 4.6 (1M)","✅  8s", ""),
            ("🔴 Claude Opus 4.7 (1M)","✅ 15s", ""),
        ]),
    ]

    for heat_name, results in heat_results:
        out(f"  {BOLD}{heat_name}:{RST}")
        sl(0.12)
        for model, time_str, comment in results:
            c = f"  {comment}" if comment else ""
            out(f"    {model:<30} {time_str}{c}")
            sl(0.1)
        winner = results[0][0]
        out(f"    🏅 {BOLD}{winner.split(' ', 1)[1]} wins!{RST}")
        sl(0.15)
        out()

    out("🏅 4 heat winners advance to the Finals!")
    sl(0.3)


# ══════════════════════════════════════════════════════════
# PHASE 5 — FINALS + JUDGING                        ~2.0 s
# ══════════════════════════════════════════════════════════
def p5_finals():
    out()
    out("🧬 Evolution Brief dispatched — finalists learn from Round 1")
    sl(0.2)
    out(f"{BOLD}🏁 ROUND 2 — FINALS{RST}")
    sl(0.15)
    out("  🔵 Claude Opus 4.7         ✅  5s")
    sl(0.1)
    out("  🟢 GPT-5.5                 ✅  4s  ⚡")
    sl(0.1)
    out("  🟡 Claude Opus 4.6         ✅  7s")
    sl(0.1)
    out("  🟣 Claude Sonnet 4.6       ✅  6s")
    sl(0.15)
    out()
    out("⚖️  The panel convenes... 🔒 Submissions anonymized. No favoritism. No mercy.")
    sl(0.2)
    out("   👨‍⚖️ Judges: Claude Opus 4.5 · GPT-5.4 · Codex GPT-5.2")
    sl(0.15)
    out()
    out("🥁 ... 🥁🥁 ... 🥁🥁🥁")
    sl(0.4)


# ══════════════════════════════════════════════════════════
# PHASE 6 — WINNER + PODIUM                         ~2.5 s
# ══════════════════════════════════════════════════════════
def p6_winner():
    out()
    out("🎆🎆🎆 AND THE WINNER IS... 🎆🎆🎆")
    sl(0.6)
    out()
    out("╔══════════════════════════════════════════════════════════════════╗")
    out("║   🏆  CHAMPION:  GPT-5.5                                         ║")
    out("║   SCORE: 46/50  ·  CONSENSUS: STRONG  ·  ALL JUDGES AGREED     ║")
    out("╚══════════════════════════════════════════════════════════════════╝")
    sl(0.35)
    out()
    out(f"{BOLD}🏅 THE PODIUM{RST}")
    out()
    podium = [
        "                🥇",
        "             ┌──────┐",
        "             │ GPT  │",
        "             │ 5.5  │",
        "      🥈     │  46  │     🥉",
        "   ┌──────┐  │      │  ┌──────┐",
        "   │OPUS  │  │      │  │OPUS  │",
        "   │ 4.7  │  │      │  │ 4.6  │",
        "   │  43  │  │      │  │  41  │",
        "   └──────┘  └──────┘  └──────┘",
    ]
    for line in podium:
        out(f"  {line}")
        sl(0.08)
    sl(0.25)


# ══════════════════════════════════════════════════════════
# PHASE 7 — ENSEMBLE SYNTHESIS                      ~2.0 s
# ══════════════════════════════════════════════════════════
def p7_ensemble():
    out()
    out(f"{BOLD}🗳️  ENSEMBLE SYNTHESIS{RST}")
    sl(0.15)
    out()
    out("🧬 How would you like to merge the results?")
    sl(0.12)
    out(f"  > {BOLD}Ensemble synthesis ⭐ (voting merge across all finalists){RST} ← SELECTED")
    sl(0.1)
    out(f"  {DIM}> Winner only (apply winner's changes){RST}")
    sl(0.08)
    out(f"  {DIM}> Custom pick (choose per-file){RST}")
    sl(0.08)
    out(f"  {DIM}> Discard all{RST}")
    sl(0.25)
    out()
    out("✅ Merged! Here's what changed:")
    sl(0.1)
    out("  ✅ CONSENSUS: 3/4 finalists used same architecture — auto-accepted")
    sl(0.1)
    out("  🟡 MAJORITY: 2/4 agreed on naming convention — accepted")
    sl(0.1)
    out(f"  ⚠️  UNIQUE: GPT-5.5 added animation easing — preserved for review")
    sl(0.2)


# ══════════════════════════════════════════════════════════
# PHASE 8 — ELO UPDATE + CLOSING                    ~2.5 s
# ══════════════════════════════════════════════════════════
def p8_elo():
    out()
    out(f"{BOLD}📈 ELO UPDATE{RST}")
    out()
    elo = [
        "  📈 GPT-5.5               1387 → 1419  (+32)  🔥 Hot streak",
        "  📈 Claude Opus 4.7       1355 → 1371  (+16)  📈 Rising",
        "  ➡️  Claude Opus 4.6      1262 → 1262  ( ±0)  💪 Strong",
        "  📉 Claude Sonnet 4.6     1286 → 1270  (-16)  ⚡ Solid",
    ]
    for e in elo:
        out(e)
        sl(0.22)
    sl(0.2)
    out()
    out("╔══════════════════════════════════════════════════════════════════╗")
    out("║                    🏟️  HACKATHON COMPLETE  🏟️                    ║")
    out("╠══════════════════════════════════════════════════════════════════╣")
    out("║  📋 Task:    Terminal demo animation                            ║")
    out("║  🏆 Winner:  GPT-5.5 (46/50)                                    ║")
    out("║  🧬 Merged:  Ensemble synthesis — best of all 4 finalists       ║")
    out("║  📈 ELO:     GPT-5.5 climbs to 1419                             ║")
    out("╚══════════════════════════════════════════════════════════════════╝")
    sl(0.3)
    out()
    out()
    out("📼 Want the highlight reel?")
    sl(0.12)
    out(f"  > {BOLD}Save replay{RST} ← SELECTED")
    sl(0.08)
    out(f"  {DIM}> Skip{RST}")
    sl(0.2)
    out()
    out("📼 Saved → hackathon-replay-20260301.md")
    sl(0.15)
    out()
    out("GG WP! Scores logged. ELOs updated.")
    out("May your diffs be clean and your builds be green. 💚 Until next time... 🫡")
    sl(0.3)


# ══════════════════════════════════════════════════════════
def main():
    start = time.monotonic()
    target = 22.0
    try:
        p1_banner()
        p2_leaderboard()
        p3_tournament()
        p4_heats()
        p5_finals()
        p6_winner()
        p7_ensemble()
        p8_elo()
        remaining = target - (time.monotonic() - start)
        if remaining > 0:
            sl(remaining)
    finally:
        out(RST + SHOW, end="")
        out()


if __name__ == "__main__":
    main()
