#!/usr/bin/env python3
"""Havoc Hackathon — 20-second terminal demo animation.

Smart merge: GPT-5.2 timing control + Opus 4.6 visuals.
github.com/DUBSOpenHub/havoc-hackathon
"""

import sys
import time
import os
import re
import random
import shutil
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


def typer(text, delay=0.020, col=""):
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
    out(f"  {DIM}{'─' * W}{RST}")


def pbar(pct, bw=20):
    filled = int(round((pct / 100.0) * bw))
    return "█" * filled + "░" * (bw - filled)


# ══════════════════════════════════════════════════════════
# PHASE 1 — BANNER                                    ~2 s
# ══════════════════════════════════════════════════════════
def p1_banner():
    out(HIDE, end="")
    out(CLR, end="")
    sl(0.15)
    box_top()
    sl(0.06)
    box_empty()
    sl(0.06)
    box_mid(f"{GOLD}{BOLD}  ⚡  H A V O C   H A C K A T H O N  ⚡  {RST}")
    sl(0.06)
    box_empty()
    sl(0.06)
    box_mid(f"{DIM}github.com/DUBSOpenHub/havoc-hackathon{RST}")
    sl(0.06)
    box_empty()
    sl(0.06)
    box_bot()
    sl(0.45)
    out()
    out(center(f"{MAG}{BOLD}🏟️  THE ARENA IS READY  🏟️{RST}", W + 4))
    sl(0.6)


# ══════════════════════════════════════════════════════════
# PHASE 2 — TASK + CONTESTANTS                        ~3 s
# ══════════════════════════════════════════════════════════
def p2_task():
    out()
    divider()
    out()
    typer("  🎯 TASK: Build a terminal demo animation",
          delay=0.018, col=WHT)
    sl(0.2)
    out()
    w_data = [
        ("🔵", "Claude Opus 4.6",  BLU),
        ("🟢", "Codex (GPT-5.3)",  GRN),
        ("🟡", "Gemini 3 Pro",     GOLD),
    ]
    for icon, name, color in w_data:
        out(f"    {icon}  {color}{BOLD}{name}{RST}")
        sl(0.28)
    out()
    out(f"  {DIM}Rubric: creativity · accuracy · style · wow  (50 pts){RST}")
    sl(0.3)
    out()
    for n in ("3", "2", "1"):
        out(f"    {GOLD}{BOLD}{n}...{RST}", end="")
        sl(0.35)
    out(f"  {RED}{BOLD}GO! 🏁{RST}")
    sl(0.2)


# ══════════════════════════════════════════════════════════
# PHASE 3 — RACE                                      ~4 s
# ══════════════════════════════════════════════════════════
def p3_race():
    out()
    divider()
    out(f"  {CYAN}{BOLD}⏱️  MODELS GENERATING...{RST}")
    out()

    models = [
        {"icon": "🔵", "name": "Claude Opus ", "color": BLU, "finish": 24},
        {"icon": "🟢", "name": "Codex GPT5.3", "color": GRN, "finish": 30},
        {"icon": "🟡", "name": "Gemini 3 Pro", "color": GOLD, "finish": 36},
    ]
    BAR_W = 20
    TOTAL = 38
    done = [False, False, False]

    def render(m, pct, frame, finished):
        b = pbar(pct, BAR_W)
        status = f"{GRN}✅{RST}" if finished else f"{GRAY}{SPIN[frame % 10]}{RST}"
        return (f"  {m['icon']} {m['color']}{m['name']}{RST} "
                f"[{m['color']}{b}{RST}] {pct:3d}% {status}")

    for m in models:
        out(render(m, 0, 0, False))

    for frame in range(1, TOTAL + 1):
        out("\033[3A", end="")
        for i, m in enumerate(models):
            if not done[i]:
                noise = random.uniform(-2, 2)
                pct = int((frame / m["finish"]) * 100 + noise)
                pct = max(1, min(99, pct))
                if frame >= m["finish"]:
                    pct = 100
                    done[i] = True
            else:
                pct = 100
            out(CLRL + render(m, pct, frame, done[i]))
        sl(0.095)

    out()
    out(f"  {DIM}All submissions received. Locking outputs...{RST}")
    sl(0.25)


# ══════════════════════════════════════════════════════════
# PHASE 4 — JUDGING                                   ~2 s
# ══════════════════════════════════════════════════════════
def p4_judging():
    divider()
    out()
    out(f"  {MAG}{BOLD}⚖️  Sealed judging in progress", end="")
    for _ in range(3):
        sl(0.18)
        out(".", end="")
    out(RST)
    sl(0.15)

    judges = [
        f"{BLU}Claude Sonnet 4.5{RST}",
        f"{GRN}GPT-5.2{RST}",
        f"{GOLD}Codex Max{RST}",
    ]
    out(f"  {DIM}Judges:{RST}", end="")
    for j in judges:
        out(f"  👤 {j}", end="")
        sl(0.22)
    out()
    sl(0.15)
    out()
    for d in ("🥁 ", "🥁🥁 ", "🥁🥁🥁"):
        out(f"    {GOLD}{d}{RST}", end="")
        sl(0.32)
    out()
    sl(0.2)


# ══════════════════════════════════════════════════════════
# PHASE 5 — WINNER REVEAL                           ~1.5 s
# ══════════════════════════════════════════════════════════
def p5_winner():
    out()
    out(center(
        f"{RED}{BOLD}🎆🎆🎆  AND THE WINNER IS...  🎆🎆🎆{RST}",
        W + 4))
    sl(0.85)
    out()
    out(center(
        f"{GOLD}{BOLD}🏆  CHAMPION: Claude Opus 4.6 — 43/50  🏆{RST}",
        W + 4))
    sl(0.45)


# ══════════════════════════════════════════════════════════
# PHASE 6 — PODIUM                                    ~3 s
# ══════════════════════════════════════════════════════════
def p6_podium():
    out()
    divider()
    out()

    G, C, Y = GOLD, CYAN, YELL
    podium = [
        f"                {G}{BOLD}🥇{RST}",
        f"            {G}{BOLD}Claude Opus{RST}",
        f"             {G}  43/50{RST}",
        f"          {G}╔═════════════╗{RST}",
        f"          {G}║▓▓▓▓▓▓▓▓▓▓▓▓▓║{RST}   {C}{BOLD}🥈{RST}",
        f"          {G}║▓▓▓▓▓▓▓▓▓▓▓▓▓║{RST} {C}{BOLD}Codex 5.3{RST}",
        f"          {G}║▓▓▓▓▓▓▓▓▓▓▓▓▓║{RST} {C} 37/50{RST}",
        f"          {G}║▓▓▓▓▓▓▓▓▓▓▓▓▓{RST}{C}╠══════════╗{RST}  {Y}{BOLD}🥉{RST}",
        f"          {G}║▓▓▓▓▓▓▓▓▓▓▓▓▓{RST}{C}║░░░░░░░░░░║{RST}{Y}{BOLD} Gemini{RST}",
        f"          {G}║▓▓▓▓▓▓▓▓▓▓▓▓▓{RST}{C}║░░░░░░░░░░║{RST}{Y}  35/50{RST}",
        f"          {G}║▓▓▓▓▓▓▓▓▓▓▓▓▓{RST}{C}║░░░░░░░░░░{RST}{Y}╠═════════╗{RST}",
        f"          {G}║▓▓▓▓▓▓▓▓▓▓▓▓▓{RST}{C}║░░░░░░░░░░{RST}{Y}║▒▒▒▒▒▒▒▒▒║{RST}",
        f"          {G}╚═════════════{RST}{C}╩══════════{RST}{Y}╩═════════╝{RST}",
    ]
    for line in podium:
        out(f"  {line}")
        sl(0.14)
    sl(0.3)


# ══════════════════════════════════════════════════════════
# PHASE 7 — ELO + CLOSING                             ~3 s
# ══════════════════════════════════════════════════════════
def p7_elo():
    out()
    divider()
    out(f"  {WHT}{BOLD}📊 ELO UPDATES{RST}")
    out()
    elo = [
        f"    🔵 Claude Opus 4.6   {GRN}📈 1500 → 1532  (+32){RST}",
        f"    🟢 Codex (GPT-5.3)   {DIM}➡️  1500 → 1500  ( ±0){RST}",
        f"    🟡 Gemini 3 Pro      {RED}📉 1500 → 1468  (-32){RST}",
    ]
    for e in elo:
        out(e)
        sl(0.28)
    sl(0.35)
    out()
    box_top()
    box_empty()
    box_mid(f"{MAG}{BOLD}🏟️  HACKATHON COMPLETE  🏟️{RST}")
    box_empty()
    box_mid(f"{GRN}{BOLD}GG WP! 💚{RST}")
    box_empty()
    box_bot()
    out()
    sl(0.6)


# ══════════════════════════════════════════════════════════
def main():
    start = time.monotonic()
    target = 19.8
    try:
        p1_banner()
        p2_task()
        p3_race()
        p4_judging()
        p5_winner()
        p6_podium()
        p7_elo()
        remaining = target - (time.monotonic() - start)
        if remaining > 0:
            sl(remaining)
    finally:
        out(RST + SHOW, end="")
        out()


if __name__ == "__main__":
    main()
