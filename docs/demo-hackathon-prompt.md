# Demo Animation — Hackathon Prompt

> **Competition prompt used in a Havoc Hackathon to generate `docs/demo/demo.py`.**
> 13 current full-size AI models competed in a full tournament (4 heats → finals) to build the best terminal demo animation.

## Task

Build `docs/demo/demo.py` — a self-contained Python 3 script (stdlib only, zero pip dependencies) that previews a full Havoc Hackathon tournament run in approximately 20 seconds, matching the actual CLI output style. Suitable for recording via VHS into a GIF for the repo README.

## Required Phases (~20s total)

1. **BANNER** (~1.5s) — Clear screen. Render the exact Havoc Hackathon banner from SKILL.md using box-drawing characters (╔═╗║╚╝).
2. **ELO LEADERBOARD** (~3.5s) — Show 13-model leaderboard with columns: Rank, Model, ELO, W-L, Record. Record column uses emoji status labels (🔥 Hot streak, 📈 Rising, 💪 Strong, ⚡ Solid, 😐 .500, 🆕 New, 📉 Slumping, 🥶 Cold, 💀 Winless/Struggling).
3. **TOURNAMENT SETUP** (~2.5s) — Task description, rubric, "TOURNAMENT MODE — 13 models → 4 heats → 4 finalists → 1 champion", heat assignments, countdown "3... 2... 1... GO! 🏁"
4. **HEAT RACES** (~3s) — Show 4 heats with sequential finish-line results per model (✅ time ⚡ commentary). Announce each heat winner with 🏅.
5. **FINALS + JUDGING** (~2s) — Evolution Brief dispatch, Round 2 finalists with finish times, sealed judging announcement with judge names, drumroll 🥁
6. **WINNER + PODIUM** (~2.5s) — "🎆🎆🎆 AND THE WINNER IS..." with champion box, then ASCII podium using ┌──────┐ style with 🥇🥈🥉 and scores.
7. **ELO UPDATE + CLOSING** (~2.5s) — ELO changes with 📈/➡️/📉 arrows and Record labels, closing ceremony recap box with task → winner → merge → ELO summary, "GG WP! 💚"

## Requirements

- Python 3.8+ stdlib ONLY (sys, time, re, unicodedata)
- Minimal ANSI: bold and dim only — no rich color palette. Output should look like natural CLI text with emoji, not a custom TUI app.
- `sys.stdout.write()` + `flush()` for sequential text output
- Terminal width: max 70 columns (GIF-friendly)
- Total runtime: 18–22 seconds
- Cursor hide/show with `try/finally` cleanup
- `time.monotonic()` target timing to guarantee consistent runtime
- Sequential text results (not animated progress bars) to match actual CLI streaming behavior

## Judging Criteria (each /10, max 50)

1. **CLI Fidelity** — Output matches what the actual Havoc Hackathon skill produces in the Copilot CLI
2. **Faithfulness** — All 7 phases present and accurate to a real tournament run
3. **Code Quality** — Clean, readable, well-structured Python with good abstractions
4. **Timing & Pacing** — ~20s cinematic flow, not rushed or draggy
5. **Polish** — Edge cases handled, no artifacts, clean exit, width constraints met

## Tournament Results

| Place | Model | Heat Score | Finals Score | Notes |
|-------|-------|-----------|-------------|-------|
| 🏆 1st | GPT-5.2 | 46/50 | 46/50 (median) | Unanimous winner — best timing control |
| 🥈 2nd | Claude Opus 4.6 | 44/50 | 42/50 (median) | Best visuals — podium art |
| 🥉 3rd | Claude Sonnet 4.6 | 41/50 | 32/50 (median) | Good faithfulness, timing overrun |

**Final output:** Smart merge of GPT-5.2's timing control + Opus 4.6's visual elements, then revised to match actual CLI output style (no ANSI art, sequential text, simple ASCII podium).
