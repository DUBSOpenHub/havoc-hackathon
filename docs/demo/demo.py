#!/usr/bin/env python3
"""Havoc Hackathon — 20-second terminal demo animation.

Tournament mode with ELO leaderboard, 4 heats, finals.
github.com/DUBSOpenHub/havoc-hackathon
"""

import sys
import time
import re
import random
import unicodedata

random.seed(42)

# ── ANSI palette ─────────────────────────────────────────
RST  = "\033[0m"
BOLD = "\033[1m"
DIM  = "\033[2m"
CYAN = "\033[36;1m"
GOLD = "\033[33;1m"
GRN  = "\033[32;1m"
RED  = "\033[31;1m"
BLU  = "\033[34;1m"
MAG  = "\033[35;1m"
WHT  = "\033[37;1m"
GRAY = "\033[90m"
YELL = "\033[33m"

HIDE = "\033[?25l"
SHOW = "\033[?25h"
CLR  = "\033[2J\033[H"
CLRL = "\033[K"
SPIN = "⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏"

W = 56  # inner box width


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


def center(text, w=W):
    pad = max(0, (w - vlen(text)) // 2)
    return " " * pad + text


def typer(text, delay=0.018, col=""):
    for ch in text:
        out(f"{col}{ch}{RST}", end="")
        time.sleep(delay)
    out()


def box_top(w=W):
    out(f"  {CYAN}╔{'═' * w}╗{RST}")


def box_bot(w=W):
    out(f"  {CYAN}╚{'═' * w}╝{RST}")


def box_mid(text="", w=W):
    vl = vlen(text)
    pad = max(0, w - vl)
    left = pad // 2
    right = pad - left
    out(f"  {CYAN}║{RST}{' ' * left}{text}{' ' * right}{CYAN}║{RST}")


def box_empty(w=W):
    out(f"  {CYAN}║{' ' * w}║{RST}")


def divider():
    out(f"  {DIM}{'─' * 62}{RST}")


def pbar(pct, bw=16):
    filled = int(round((pct / 100.0) * bw))
    return "█" * filled + "░" * (bw - filled)


# ══════════════════════════════════════════════════════════
# PHASE 1 — BANNER                                  ~1.5 s
# ══════════════════════════════════════════════════════════
def p1_banner():
    out(HIDE, end="")
    out(CLR, end="")
    sl(0.1)
    box_top()
    sl(0.04)
    box_empty()
    sl(0.04)
    box_mid(f"{GOLD}{BOLD}  ⚡  H A V O C   H A C K A T H O N  ⚡  {RST}")
    sl(0.04)
    box_empty()
    sl(0.04)
    box_mid(f"🏟️  {DIM}THE ARENA IS READY. THE AI MODELS ARE READY TO COMPETE.{RST}  🏟️")
    sl(0.04)
    box_empty()
    sl(0.04)
    box_bot()
    sl(0.5)


# ══════════════════════════════════════════════════════════
# PHASE 2 — ELO LEADERBOARD                         ~3.5 s
# ══════════════════════════════════════════════════════════
def p2_leaderboard():
    out()
    out(f"  {WHT}{BOLD}📊 Current ELO Leaderboard (12 hackathons of history!){RST}")
    out()
    sl(0.15)

    out(f"  {DIM} Rank   Model                        ELO      W-L     Record{RST}")
    out(f"  {DIM} {'─' * 62}{RST}")
    sl(0.1)

    rows = [
        ("1.",  "Claude Opus 4.6",        "1355", "19-6",  "🔥", "Hot streak"),
        ("2.",  "Claude Sonnet 4.6",      "1286",  "9-4",  "📈", "Rising"),
        ("3.",  "Claude Opus 4.6 (1M)",   "1262",  "6-2",  "💪", "Strong"),
        ("4.",  "GPT-5.1",               "1254",  "8-3",  "📈", "Rising"),
        ("5.",  "GPT-5.2",               "1251",  "8-5",  "⚡", "Solid"),
        ("6.",  "Claude Opus 4.6 (Fast)", "1248",  "7-5",  "⚡", "Solid"),
        ("7.",  "Claude Sonnet 4.5",      "1197",  "8-8",  "😐", ".500"),
        ("8.",  "Claude Opus 4.5",        "1193",  "2-3",  "🆕", "New"),
        ("9.",  "Codex GPT-5.3",         "1153", "6-11",  "📉", "Slumping"),
        ("10.", "Codex GPT-5.2",         "1116",  "1-7",  "🥶", "Cold"),
        ("11.", "Codex Max GPT-5.1",     "1069",  "0-9",  "💀", "Winless"),
        ("12.", "Gemini 3 Pro",          "1017", "3-17",  "💀", "Struggling"),
    ]

    for rank, model, elo, wl, emoji, label in rows:
        out(f"   {WHT}{rank:>3}{RST}   {model:<25} {GOLD}{elo}{RST}   {wl:>5}   {emoji} {label}")
        sl(0.2)

    sl(0.3)


# ══════════════════════════════════════════════════════════
# PHASE 3 — TOURNAMENT SETUP                        ~2.5 s
# ══════════════════════════════════════════════════════════
def p3_tournament():
    out()
    divider()
    out()
    typer("  🎯 TASK: Build a terminal demo animation",
          delay=0.015, col=WHT)
    sl(0.1)
    out(f"  {DIM}Rubric: creativity · accuracy · style · wow · impact  (50 pts){RST}")
    sl(0.15)
    out()
    out(f"  {MAG}{BOLD}🏟️  TOURNAMENT MODE{RST}"
        f"{DIM} — 12 models → 4 heats → 4 finalists → 1 champion{RST}")
    sl(0.3)
    out()

    heats = [
        ("Heat 1", "Claude Opus 4.6, GPT-5.2, Codex Max GPT-5.1"),
        ("Heat 2", "Claude Sonnet 4.6, GPT-5.1, Codex GPT-5.2"),
        ("Heat 3", "Claude Opus 4.6 (1M), Claude Sonnet 4.5, Gemini 3 Pro"),
        ("Heat 4", "Claude Opus 4.6 (Fast), Claude Opus 4.5, Codex GPT-5.3"),
    ]
    for heat_name, models in heats:
        out(f"    {CYAN}{BOLD}{heat_name}:{RST} {DIM}{models}{RST}")
        sl(0.18)

    sl(0.15)
    out()
    for n in ("3", "2", "1"):
        out(f"    {GOLD}{BOLD}{n}...{RST}", end="")
        sl(0.28)
    out(f"  {RED}{BOLD}GO! 🏁{RST}")
    sl(0.15)


# ══════════════════════════════════════════════════════════
# PHASE 4 — HEAT RACES                              ~3.0 s
# ══════════════════════════════════════════════════════════
def p4_heats():
    out()
    divider()
    out(f"  {CYAN}{BOLD}⏱️  ROUND 1 — HEATS IN PROGRESS...{RST}")
    out()

    heat_data = [
        {"name": "Heat 1", "color": BLU,  "finish": 18,
         "winner": "Claude Opus 4.6"},
        {"name": "Heat 2", "color": GRN,  "finish": 24,
         "winner": "Claude Sonnet 4.6"},
        {"name": "Heat 3", "color": GOLD, "finish": 20,
         "winner": "Claude Opus 4.6 (1M)"},
        {"name": "Heat 4", "color": MAG,  "finish": 26,
         "winner": "Opus 4.6 (Fast)"},
    ]
    BAR_W = 16
    TOTAL = 28
    done = [False] * 4

    def render(h, pct, frame, finished):
        b = pbar(pct, BAR_W)
        sp = SPIN[frame % 10]
        status = f"{GRN}✅{RST}" if finished else f"{GRAY}{sp}{RST}"
        tag = f" 🏅 {GRN}{h['winner']}{RST}" if finished else ""
        return (f"  {h['color']}{BOLD}{h['name']}{RST} "
                f"[{h['color']}{b}{RST}] {pct:3d}% {status}{tag}")

    for h in heat_data:
        out(render(h, 0, 0, False))

    for frame in range(1, TOTAL + 1):
        out(f"\033[{len(heat_data)}A", end="")
        for i, h in enumerate(heat_data):
            if not done[i]:
                noise = random.uniform(-2, 2)
                pct = int((frame / h["finish"]) * 100 + noise)
                pct = max(1, min(99, pct))
                if frame >= h["finish"]:
                    pct = 100
                    done[i] = True
            else:
                pct = 100
            out(CLRL + render(h, pct, frame, done[i]))
        sl(0.085)

    out()
    out(f"  {GRN}{BOLD}🏅 4 heat winners advance to the Finals!{RST}")
    sl(0.35)


# ══════════════════════════════════════════════════════════
# PHASE 5 — FINALS + JUDGING                        ~2.5 s
# ══════════════════════════════════════════════════════════
def p5_finals():
    out()
    divider()
    out(f"  {MAG}{BOLD}🧬 Evolution Brief dispatched — finalists learn from Round 1{RST}")
    sl(0.25)
    out(f"  {CYAN}{BOLD}🏁 ROUND 2 — FINALS{RST}")
    sl(0.2)

    finalists = [
        ("🔵", "Claude Opus 4.6",        BLU),
        ("🟢", "Claude Sonnet 4.6",      GRN),
        ("🟡", "Claude Opus 4.6 (1M)",   GOLD),
        ("🟣", "Claude Opus 4.6 (Fast)", MAG),
    ]
    for icon, name, color in finalists:
        out(f"    {icon}  {color}{BOLD}{name}{RST} {GRN}✅{RST}")
        sl(0.12)

    sl(0.1)
    out()
    out(f"  {MAG}{BOLD}⚖️  Sealed judging in progress", end="")
    for _ in range(3):
        sl(0.12)
        out(".", end="")
    out(RST)
    sl(0.1)
    out()
    for d in ("🥁 ", "🥁🥁 ", "🥁🥁🥁"):
        out(f"    {GOLD}{d}{RST}", end="")
        sl(0.22)
    out()
    sl(0.15)


# ══════════════════════════════════════════════════════════
# PHASE 6 — WINNER + PODIUM                         ~2.0 s
# ══════════════════════════════════════════════════════════
def p6_winner():
    out()
    out(center(
        f"{RED}{BOLD}🎆🎆🎆  AND THE WINNER IS...  🎆🎆🎆{RST}",
        W + 4))
    sl(0.6)
    out()
    box_top()
    box_mid(f"{GOLD}{BOLD}🏆  CHAMPION: Claude Opus 4.6 — 46/50  🏆{RST}")
    box_bot()
    sl(0.3)
    out()

    G, C, Y = GOLD, CYAN, YELL
    podium = [
        f"            {G}{BOLD}🥇{RST}          {C}{BOLD}🥈{RST}        {Y}{BOLD}🥉{RST}",
        f"        {G}╔═════════╗{RST}  {C}╔════════╗{RST} {Y}╔════════╗{RST}",
        f"        {G}║ Opus4.6 ║{RST}  {C}║Son 4.6 ║{RST} {Y}║Opus 1M ║{RST}",
        f"        {G}║  46/50  ║{RST}  {C}║ 43/50  ║{RST} {Y}║ 41/50  ║{RST}",
        f"        {G}╚═════════╝{RST}  {C}╚════════╝{RST} {Y}╚════════╝{RST}",
    ]
    for line in podium:
        out(f"  {line}")
        sl(0.09)
    sl(0.2)


# ══════════════════════════════════════════════════════════
# PHASE 7 — ELO UPDATE + CLOSING                    ~2.5 s
# ══════════════════════════════════════════════════════════
def p7_elo():
    out()
    divider()
    out(f"  {WHT}{BOLD}📈 ELO UPDATE{RST}")
    out()
    elo = [
        f"    🔵 Claude Opus 4.6       {GRN}📈 1355 → 1387  (+32)"
        f"  🔥 Hot streak{RST}",
        f"    🟢 Claude Sonnet 4.6     {GRN}📈 1286 → 1302  (+16)"
        f"  📈 Rising{RST}",
        f"    🟡 Claude Opus 4.6 (1M)  {DIM}➡️  1262 → 1262  ( ±0)"
        f"  💪 Strong{RST}",
        f"    🟣 Opus 4.6 (Fast)       {RED}📉 1248 → 1232  (-16)"
        f"  ⚡ Solid{RST}",
    ]
    for e in elo:
        out(e)
        sl(0.22)
    sl(0.2)
    out()
    box_top()
    box_empty()
    box_mid(f"{MAG}{BOLD}🏟️  HACKATHON COMPLETE  🏟️{RST}")
    box_empty()
    box_mid(f"{DIM}12 models · 4 heats · 2 rounds · 1 champion{RST}")
    box_empty()
    box_mid(f"{GRN}{BOLD}GG WP! 💚{RST}")
    box_empty()
    box_bot()
    out()
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
