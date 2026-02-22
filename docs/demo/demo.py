#!/usr/bin/env python3
"""Havoc Hackathon — 20-second terminal demo animation.

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
    out("📊 Current ELO Leaderboard (12 hackathons of history!)")
    out()
    sl(0.15)

    out(f" {BOLD}Rank   Model                        ELO      W-L     Record{RST}")
    out(f" {'─' * 62}")
    sl(0.1)

    rows = [
        (" 1.",  "Claude Opus 4.6",        "1355", "19-6",  "🔥 Hot streak"),
        (" 2.",  "Claude Sonnet 4.6",      "1286",  "9-4",  "📈 Rising"),
        (" 3.",  "Claude Opus 4.6 (1M)",   "1262",  "6-2",  "💪 Strong"),
        (" 4.",  "GPT-5.1",               "1254",  "8-3",  "📈 Rising"),
        (" 5.",  "GPT-5.2",               "1251",  "8-5",  "⚡ Solid"),
        (" 6.",  "Claude Opus 4.6 (Fast)", "1248",  "7-5",  "⚡ Solid"),
        (" 7.",  "Claude Sonnet 4.5",      "1197",  "8-8",  "😐 .500"),
        (" 8.",  "Claude Opus 4.5",        "1193",  "2-3",  "🆕 New"),
        (" 9.",  "Codex GPT-5.3",         "1153", "6-11",  "📉 Slumping"),
        ("10.",  "Codex GPT-5.2",         "1116",  "1-7",  "🥶 Cold"),
        ("11.",  "Codex Max GPT-5.1",     "1069",  "0-9",  "💀 Winless"),
        ("12.",  "Gemini 3 Pro",          "1017", "3-17",  "💀 Struggling"),
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
    out(f"{BOLD}🏟️  TOURNAMENT MODE{RST} — 12 models → 4 heats → 4 finalists → 1 champion")
    sl(0.3)
    out()

    heats = [
        ("Heat 1", "Claude Opus 4.6, GPT-5.2, Codex Max GPT-5.1"),
        ("Heat 2", "Claude Sonnet 4.6, GPT-5.1, Codex GPT-5.2"),
        ("Heat 3", "Claude Opus 4.6 (1M), Claude Sonnet 4.5, Gemini 3 Pro"),
        ("Heat 4", "Claude Opus 4.6 (Fast), Claude Opus 4.5, Codex GPT-5.3"),
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
            ("🔵 Claude Opus 4.6",     "✅  4s", "⚡ Speedrun!"),
            ("🟠 GPT-5.2",             "✅  7s", ""),
            ("🔴 Codex Max GPT-5.1",   "✅ 12s", ""),
        ]),
        ("Heat 2", [
            ("🟢 Claude Sonnet 4.6",   "✅  5s", "⚡"),
            ("🟠 GPT-5.1",             "✅  8s", ""),
            ("🔴 Codex GPT-5.2",       "✅ 14s", ""),
        ]),
        ("Heat 3", [
            ("🟡 Claude Opus 4.6 (1M)","✅  6s", ""),
            ("🟠 Claude Sonnet 4.5",   "✅  9s", ""),
            ("🔴 Gemini 3 Pro",        "✅ 11s", "😬 Still cooking..."),
        ]),
        ("Heat 4", [
            ("🟣 Opus 4.6 (Fast)",     "✅  3s", "⚡ Speedrun!"),
            ("🟠 Claude Opus 4.5",     "✅  8s", ""),
            ("🔴 Codex GPT-5.3",       "✅ 15s", ""),
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
    out("  🔵 Claude Opus 4.6         ✅  5s")
    sl(0.1)
    out("  🟢 Claude Sonnet 4.6       ✅  6s")
    sl(0.1)
    out("  🟡 Claude Opus 4.6 (1M)    ✅  7s")
    sl(0.1)
    out("  🟣 Claude Opus 4.6 (Fast)  ✅  4s  ⚡")
    sl(0.15)
    out()
    out("⚖️  The panel convenes... 🔒 Submissions anonymized. No favoritism. No mercy.")
    sl(0.2)
    out("   👨‍⚖️ Judges: Claude Sonnet 4.5 · GPT-5.2 · Codex Max")
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
    out("║   🏆  CHAMPION:  Claude Opus 4.6                                ║")
    out("║   SCORE: 46/50  ·  CONSENSUS: STRONG  ·  ALL JUDGES AGREED     ║")
    out("╚══════════════════════════════════════════════════════════════════╝")
    sl(0.35)
    out()
    out(f"{BOLD}🏅 THE PODIUM{RST}")
    out()
    podium = [
        "                🥇",
        "             ┌──────┐",
        "             │ OPUS │",
        "             │ 4.6  │",
        "      🥈     │  46  │     🥉",
        "   ┌──────┐  │      │  ┌──────┐",
        "   │SON   │  │      │  │OPUS  │",
        "   │ 4.6  │  │      │  │ 1M   │",
        "   │  43  │  │      │  │  41  │",
        "   └──────┘  └──────┘  └──────┘",
    ]
    for line in podium:
        out(f"  {line}")
        sl(0.08)
    sl(0.25)


# ══════════════════════════════════════════════════════════
# PHASE 7 — ELO UPDATE + CLOSING                    ~2.5 s
# ══════════════════════════════════════════════════════════
def p7_elo():
    out()
    out(f"{BOLD}📈 ELO UPDATE{RST}")
    out()
    elo = [
        "  📈 Claude Opus 4.6       1355 → 1387  (+32)  🔥 Hot streak",
        "  📈 Claude Sonnet 4.6     1286 → 1302  (+16)  📈 Rising",
        "  ➡️  Claude Opus 4.6 (1M)  1262 → 1262  ( ±0)  💪 Strong",
        "  📉 Opus 4.6 (Fast)       1248 → 1232  (-16)  ⚡ Solid",
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
    out("║  🏆 Winner:  Claude Opus 4.6 (46/50)                            ║")
    out("║  🧬 Merged:  Ensemble synthesis — best of all 4 finalists       ║")
    out("║  📈 ELO:     Opus climbs to 1387                                ║")
    out("╚══════════════════════════════════════════════════════════════════╝")
    sl(0.3)
    out()
    out("GG WP! Scores logged. ELOs updated.")
    out("May your diffs be clean and your builds be green. 💚 Until next time... 🫡")
    sl(0.5)


# ══════════════════════════════════════════════════════════
def main():
    start = time.monotonic()
    target = 19.8
    try:
        p1_banner()
        p2_leaderboard()
        p3_tournament()
        p4_heats()
        p5_finals()
        p6_winner()
        p7_elo()
        remaining = target - (time.monotonic() - start)
        if remaining > 0:
            sl(remaining)
    finally:
        out(RST + SHOW, end="")
        out()


if __name__ == "__main__":
    main()
