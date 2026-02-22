# Demo Animation — Hackathon Prompt

> **Competition prompt used in a Havoc Hackathon to generate `docs/demo/demo.py`.**
> 12 AI models competed in a full tournament (4 heats → finals) to build the best terminal demo animation.

## Task

Build `docs/demo/demo.py` — a self-contained Python 3 script (stdlib only, zero pip dependencies) that simulates a dramatic Havoc Hackathon run in approximately 20 seconds with rich ANSI terminal colors, suitable for recording via VHS into a GIF for the repo README.

## Required Phases (~20s total)

1. **CLEAR + BANNER** (~2s) — Clear screen. Render the Havoc Hackathon banner using box-drawing characters (╔═╗║╚╝) and ANSI colors. Include repo URL.
2. **TASK + CONTESTANTS** (~3s) — Show task description, reveal 3 AI model contestants one by one with colored emoji indicators, display rubric, then countdown "3... 2... 1... GO! 🏁"
3. **RACE** (~4s) — Animated progress bars with braille spinners for each model. Staggered finish times with random noise. Show ✅ when each finishes.
4. **JUDGING** (~2s) — "⚖️ Sealed judging..." with judge names appearing, then escalating drumroll 🥁
5. **WINNER REVEAL** (~1.5s) — "🎆🎆🎆 AND THE WINNER IS... 🎆🎆🎆" with dramatic pause, then champion announcement.
6. **PODIUM** (~3s) — ASCII art podium using ▓░▒ fills with box-drawing characters showing 🥇🥈🥉 and scores.
7. **ELO + CLOSING** (~3s) — Show ELO changes with 📈/➡️/📉 arrows, then final ceremony box with "GG WP! 💚"

## Requirements

- Python 3.8+ stdlib ONLY (sys, time, os, random, re, shutil, unicodedata)
- ANSI escape codes for colors (`\033[...m`). Bold, bright, gold for winner.
- `sys.stdout.write()` + `flush()` for smooth animation
- Terminal width: max 70 columns (GIF-friendly)
- Total runtime: 18–22 seconds
- `random.seed(42)` for determinism
- Cursor hide/show with `try/finally` cleanup
- `time.monotonic()` target timing to guarantee consistent runtime

## Judging Criteria (each /10, max 50)

1. **Visual Impact** — Stunning colors, smooth animations, dramatic reveals
2. **Faithfulness** — All 7 phases present and accurate to a real hackathon run
3. **Code Quality** — Clean, readable, well-structured Python with good abstractions
4. **Timing & Pacing** — ~20s cinematic flow, not rushed or draggy
5. **Polish** — Edge cases handled, no artifacts, clean exit, width constraints met

## Tournament Results

| Place | Model | Heat Score | Finals Score | Notes |
|-------|-------|-----------|-------------|-------|
| 🏆 1st | GPT-5.2 | 46/50 | 46/50 (median) | Unanimous winner — best timing control |
| 🥈 2nd | Claude Opus 4.6 | 44/50 | 42/50 (median) | Best visuals — ▓░▒ podium art |
| 🥉 3rd | Claude Sonnet 4.6 | 41/50 | 32/50 (median) | Good faithfulness, timing overrun |

**Final output:** Smart merge of GPT-5.2's timing control + Opus 4.6's visual elements.
