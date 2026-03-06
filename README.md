# 🏟️ Havoc Hackathon

**Pit AI models against each other. Score them sealed. Crown a winner. All built using the GitHub Copilot CLI. ⚡**

[![GitHub](https://img.shields.io/badge/GitHub-Copilot_CLI-blue?logo=github)](https://github.com/features/copilot)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Security Policy](https://img.shields.io/badge/Security-Policy-brightgreen?logo=github)](SECURITY.md)

> ⚡ **Get started fast!** Copy this right into the [Copilot CLI](https://github.com/github/copilot-cli):
> ```
> /skills add DUBSOpenHub/havoc-hackathon
> ```

---

<p align="center">
  <img src="docs/demo/demo.gif" alt="Havoc Hackathon Demo — terminal preview showing ELO leaderboard, tournament heats, ensemble synthesis, and winner reveal" width="700" />
  <br />
  <sub>▲ Preview of a 14-model tournament: ELO leaderboard → 4 heats → finals → ensemble synthesis → winner reveal · <code>python3 docs/demo/demo.py</code> to run locally</sub>
</p>

---

## 🤔 What Is This?

**Havoc Hackathon** is a multi-model orchestration skill for the [Copilot CLI](https://docs.github.com/copilot/concepts/agents/about-copilot-cli) that turns your terminal into a competitive arena. Give it any task, code, copy, design, architecture, naming, anything, and it dispatches up to **14 AI models** in tournament elimination heats, scores them with sealed judge panels, evolves the best ideas between rounds, synthesizes the final output from collective intelligence across all finalists, and tracks persistent ELO ratings so it gets smarter over time. No servers, no API keys, just a skill file and your terminal.

### 💬 The Problem

You ask one AI model and hope for the best. But one model gives you one perspective with unknown quality  -  no baseline, no comparison, no way to know if the output is great or just okay. Havoc Hackathon lets you throw any idea into the arena and see how multiple AIs attack it independently, then find out which approach actually holds up under sealed evaluation.

### ⚡ What Makes It Different

- 🏟️ **Tournament mode** – up to 14 models compete in elimination heats, not just 3
- 🧬 **Evolution between rounds** – Round 2 finalists learn what won Round 1
- 🗳️ **Ensemble synthesis** – voting merge across all finalists (CONSENSUS/MAJORITY/UNIQUE)
- 🔒 **Sealed judging** – judges never see which model wrote what
- ⚖️ **Per-heat judge panels** – 3 judges × N heats running in parallel
- 🔄 **Self-correcting scores** – rubrics adapt when judges disagree
- 📈 **Persistent leaderboard** – tracks which models actually deliver over time
- 🏆 **Full ceremony** – podiums, drumrolls, and dramatic reveals in your terminal
- 📄 **Zero infrastructure** – no servers, no API keys, no build step

---

## 📦 Install (30 seconds)

### Prerequisites

- [GitHub Copilot CLI](https://github.com/github/copilot-cli) installed
- An active [Copilot subscription](https://github.com/features/copilot/plans)

### Add the Skill

#### Instant Install (no clone needed) ⚡

```bash
mkdir -p ~/.copilot/skills/havoc-hackathon ~/.copilot/agents && \
  curl -sL https://raw.githubusercontent.com/DUBSOpenHub/havoc-hackathon/main/skills/havoc-hackathon/SKILL.md \
    -o ~/.copilot/skills/havoc-hackathon/SKILL.md && \
  curl -sL https://raw.githubusercontent.com/DUBSOpenHub/havoc-hackathon/main/agents/havoc-hackathon.agent.md \
    -o ~/.copilot/agents/havoc-hackathon.agent.md && \
  curl -sL https://raw.githubusercontent.com/DUBSOpenHub/havoc-hackathon/main/agents/grid-medic.agent.md \
    -o ~/.copilot/agents/grid-medic.agent.md && \
  echo "✅ Installed! Run /skills reload in Copilot CLI, then say: run hackathon"
```

#### Full Install (clone the repo)

```bash
git clone https://github.com/DUBSOpenHub/havoc-hackathon.git && \
  mkdir -p ~/.copilot/skills ~/.copilot/agents && \
  cp -r havoc-hackathon/skills/havoc-hackathon ~/.copilot/skills/ && \
  cp havoc-hackathon/agents/*.agent.md ~/.copilot/agents/ && \
  echo "✅ Havoc Hackathon installed! Run /skills reload in Copilot CLI."
```

<details>
<summary>Other options</summary>

**Auto-discovery (run from repo):**

```bash
git clone https://github.com/DUBSOpenHub/havoc-hackathon.git
cd havoc-hackathon
copilot
```

The skill at `.github/skills/havoc-hackathon/` is automatically discovered  -  no copy needed.

</details>

---

## 🎮 Run Your First Hackathon

### Run a Hackathon

```
> run hackathon  -  build a REST API for a todo app
```

```
> run hackathon  -  review this PR for security issues
```

```
> run hackathon  -  design a landing page hero section
```

### What Happens

1. **🎬 Opening Ceremony**  -  Arena banner, mode selection (Tournament or Classic), model tier (⚡ Standard or 👑 Premium), contestant lineup, scoring rubric
2. **🏁 Round 1  -  Heats**  -  All models dispatched in parallel across elimination heats with live commentary
3. **⚖️ Per-Heat Judging**  -  3-judge sealed panels score each heat independently (up to 12 judge agents in parallel)
4. **🧬 Evolution Brief**  -  Orchestrator summarizes what strategies won each heat (zero extra LLM calls)
5. **🏁 Round 2  -  Finals**  -  Heat winners compete with Evolution Brief prepended to their prompt
6. **🏆 Winner Reveal**  -  Drumroll → fireworks → ASCII podium → detailed scoreboard
7. **🗳️ Ensemble Synthesis**  -  Voting merge across ALL finalists (CONSENSUS/MAJORITY/UNIQUE)
8. **📈 ELO Update**  -  Per-round leaderboard changes with commentary
9. **🫡 Closing Ceremony**  -  Tournament bracket recap, final stats, optional replay export

### Customize

- Choose model tier: `"run hackathon with premium models"` or `"run hackathon with standard models"`
- Choose specific models: `"hackathon with opus, gemini, and codex"`
- Classic mode (3 models, no heats): `"run hackathon quick"` or `"run hackathon fast"`
- Set custom rubric: `"judge on security, performance, and readability"`
- Preflight check: `"dry run"` or `"preflight"` to validate setup without running a real hackathon
- Show stats: `"show leaderboard"` or `"show stats"` anytime

<details>
<summary><strong>📼 Example Run  -  Full Hackathon Transcript (Premium Tier)</strong></summary>

```
> run hackathon  -  write a Mass Effect themed motivational quote for open source developers

╔══════════════════════════════════════════════════════════════════╗
║              ⚡  H A V O C   H A C K A T H O N  ⚡              ║
║                                                                  ║
║  🏟️  THE ARENA IS READY. THE AI MODELS ARE READY TO COMPETE.  🏟️  ║
╚══════════════════════════════════════════════════════════════════╝

🎯 TASK: Write a Mass Effect themed motivational quote for open source developers

👑 CONTESTANTS:
  🔵 Claude Opus 4.6       (Premium)
  🟢 Codex (GPT-5.3)       (Premium)
  🟡 Gemini 3 Pro          (Premium)

⚖️ RUBRIC: Clarity · Simplicity · Relevance · Inspiration · Memorability (each /10)

3... 2... 1... GO! 🏁

🏁 ALL MODELS CROSSED THE FINISH LINE!
  🔵 Claude Opus 4.6     ✅ 4s ⚡
  🟢 Codex (GPT-5.3)     ✅ 3s ⚡ Speedrun!
  🟡 Gemini 3 Pro        ✅ 10s

⚖️ The panel convenes... 🔒 Submissions anonymized. No favoritism. No mercy.
   👨‍⚖️ Judges: Claude Opus 4.5 · GPT-5.2 · Codex Max (GPT-5.1)

🥁 ... 🥁🥁 ... 🥁🥁🥁

🎆🎆🎆 AND THE WINNER IS... 🎆🎆🎆

╔══════════════════════════════════════════════════════════════════╗
║   🏆  CHAMPION:  Claude Opus 4.6                                ║
║   SCORE: 43/50  ·  CONSENSUS: STRONG  ·  ALL JUDGES AGREED     ║
╚══════════════════════════════════════════════════════════════════╝

🏅 THE PODIUM

                    🥇
                 ┌──────┐
                 │CLAUDE│
                 │ OPUS │
                 │ 4.6  │
          🥈     │  43  │     🥉
       ┌──────┐ │      │ ┌──────┐
       │CODEX │ │      │ │GEMINI│
       │ 5.3  │ │      │ │3 PRO │
       │  37  │ │      │ │  35  │
       └──────┘ └──────┘ └──────┘

📊 DETAILED SCOREBOARD
  Category      🥇 Claude Opus  🥈 Codex 5.3  🥉 Gemini 3 Pro
  Clarity            9              8              7
  Simplicity         8              7              5
  Relevance          9              8              8
  Inspiration        9              7              8
  Memorability       8              7              7
  TOTAL           43/50          37/50          35/50

📈 ELO UPDATE
  📈 Claude Opus 4.6   1532  (+32) ⬆️
  ➡️  Codex (GPT-5.3)   1500  (±0)
  📉 Gemini 3 Pro      1468  (-32) ⬇️

🧬 How would you like to apply the improvements?
  > Smart merge ⭐ (apply high-confidence improvements) ← SELECTED
  > Winner's improvements only
  > Review each individually
  > Discard all

✅ Merged! Here's what changed:
  Applied Claude Opus 4.6's quote with Codex's tighter phrasing

╔══════════════════════════════════════════════════════════════════╗
║                    🏟️  HACKATHON COMPLETE  🏟️                    ║
╠══════════════════════════════════════════════════════════════════╣
║  📋 Task:    Mass Effect motivational quote                     ║
║  🏆 Winner:  Claude Opus 4.6 (43/50)                            ║
║  🧬 Merged:  Smart merge — best of Opus + Codex phrasing        ║
║  📈 ELO:     Opus climbs to 1532                                ║
╚══════════════════════════════════════════════════════════════════╝

📼 Want the highlight reel?
  > Save replay
  > Skip

GG WP! Scores logged. ELOs updated. May your diffs be clean and your builds be green. 💚 Until next time... 🫡
```

</details>

📼 **See a [full real-world run transcript](docs/EXAMPLE-RUN.md)** from a Premium tier hackathon where 3 models competed to design a CLI Skills Marketplace.

---

## 🔧 How It Works

```mermaid
flowchart TD
    USER["👤 User"] --> SKILL["🏟️ SKILL.md<br/>Orchestration rules"]
    SKILL --> MODE{"Mode?"}
    MODE -->|Tournament default| HEATS["⚡ Round 1: Elastic Heats<br/>All models dispatched in parallel"]
    MODE -->|Classic quick/fast| CLASSIC["⚡ Classic: 3 models<br/>Single round"]
    HEATS --> H1["Heat 1: 3 models"]
    HEATS --> H2["Heat 2: 3 models"]
    HEATS --> H3["Heat 3: 3 models"]
    HEATS --> H4["Heat 4: 3 models"]
    H1 --> JP1["⚖️ Judge Panel 1"]
    H2 --> JP2["⚖️ Judge Panel 2"]
    H3 --> JP3["⚖️ Judge Panel 3"]
    H4 --> JP4["⚖️ Judge Panel 4"]
    JP1 --> EVOLUTION["🧬 Evolution Brief<br/>Winning strategies summarized"]
    JP2 --> EVOLUTION
    JP3 --> EVOLUTION
    JP4 --> EVOLUTION
    EVOLUTION --> FINALS["🏁 Round 2: Finals<br/>Heat winners + Evolution Brief"]
    FINALS --> FJUDGE["⚖️ Finals Judge Panel"]
    CLASSIC --> CJUDGE["⚖️ Judge Panel"]
    FJUDGE --> ENSEMBLE["🗳️ Ensemble Synthesis<br/>CONSENSUS / MAJORITY / UNIQUE"]
    CJUDGE --> MERGE["🧬 Smart Merge"]
    ENSEMBLE --> ELO["📈 ELO Update"]
    MERGE --> ELO
    ELO --> CLOSING["🏟️ Closing Ceremony"]
    SKILL --> SQL["🗄️ SQL<br/>ELO & history"]
```

---

## 📁 Project Structure

```
havoc-hackathon/
├── .github/
│   ├── CODEOWNERS                    ← 👑 Code ownership rules
│   ├── ISSUE_TEMPLATE/               ← 🐛 Bug & feature templates
│   ├── PULL_REQUEST_TEMPLATE.md      ← 📝 PR checklist
│   ├── dependabot.yml                ← 🤖 Automated dependency updates
│   ├── workflows/
│   │   └── validate.yml              ← ✅ CI: structural validation + YAML check
│   ├── DISCUSSION_TEMPLATE/
│   │   └── share-your-run.yml       ← 📼 Share your hackathon results
│   └── skills/
│       └── havoc-hackathon/
│           └── SKILL.md              ← 🏟️ Auto-discovered skill
├── agents/
│   ├── havoc-hackathon.agent.md      ← 🤖 Agent config (tournament orchestrator)
│   └── grid-medic.agent.md           ← 🚑 Self-healing agent (recursive improvement loop)
├── docs/
│   ├── TECHNICAL.md                  ← 🔬 Technical deep-dive
│   ├── demo-hackathon-prompt.md      ← 🎯 Competition prompt for demo
│   ├── demo/
│   │   ├── demo.py                   ← 🎬 20s terminal animation (stdlib only)
│   │   ├── demo.tape                 ← 📼 VHS tape for GIF recording
│   │   └── demo.gif                  ← 🖼️ Recorded GIF (after vhs run)
│   └── images/                       ← 📷 Screenshots
├── skills/
│   └── havoc-hackathon/
│       ├── SKILL.md                  ← 🏟️ Canonical skill source
│       └── catalog.yml               ← 📋 Catalog metadata
├── tests/
│   ├── validate_skill.py            ← 🧪 Structural validation (60 checks)
│   ├── preflight.py                 ← 🔧 Offline preflight validator
│   └── dry_run_sim.py               ← 🏟️ Full 9-phase dry-run simulator (69 checks)
├── .gitignore
├── CHANGELOG.md                      ← 📋 Version history
├── CODE_OF_CONDUCT.md                ← 🤝 Contributor Covenant
├── CONTRIBUTING.md                   ← 🛠️ How to contribute
├── GALLERY.md                        ← 🏆 Best hackathon runs showcase
├── LICENSE                           ← 📄 MIT
├── SECURITY.md                       ← 🔒 Security policy
├── TESTING.md                        ← 🧪 Conversation playbooks & QA
└── README.md                         ← 👋 You are here!
```

---

## 🤖 Models

| Display Name | Model ID | Tier |
|-------------|----------|------|
| Claude Opus 4.6 | `claude-opus-4.6` | Premium |
| Claude Opus 4.6 (Fast) | `claude-opus-4.6-fast` | Premium |
| Claude Opus 4.6 (1M) | `claude-opus-4.6-1m` | Premium |
| Claude Opus 4.5 | `claude-opus-4.5` | Premium |
| Codex Max (GPT-5.1) | `gpt-5.1-codex-max` | Standard |
| Gemini 3 Pro | `gemini-3-pro-preview` | Standard |
| Claude Sonnet 4.6 | `claude-sonnet-4.6` | Standard |
| Claude Sonnet 4.5 | `claude-sonnet-4.5` | Standard |
| Claude Sonnet 4 | `claude-sonnet-4` | Standard |
| Codex (GPT-5.3) | `gpt-5.3-codex` | Standard |
| Codex (GPT-5.2) | `gpt-5.2-codex` | Standard |
| Codex (GPT-5.1) | `gpt-5.1-codex` | Standard |
| GPT-5.2 | `gpt-5.2` | Standard |
| GPT-5.1 | `gpt-5.1` | Standard |

**Default contestants (Standard ⚡):** Claude Sonnet 4.6, Codex Max (GPT-5.1), GPT-5.2
**Default contestants (Premium 👑):** Codex (GPT-5.3), Claude Opus 4.6, Gemini 3 Pro
**Default judges (Standard ⚡):** Claude Sonnet 4.5, Codex (GPT-5.2), GPT-5.1
**Default judges (Premium 👑):** Claude Opus 4.5, GPT-5.2, Codex Max (GPT-5.1)

> 💡 **Tip:** Standard models are selected by default. Say `"run hackathon with premium models"` to use the heavy hitters.

---

## 🚑 Grid-Medic: Recursive Self-Improvement

Havoc Hackathon ships with **Grid-Medic**, a self-healing agent that monitors your agent fleet. When it detects an underperforming agent (≤5/10 quality or 3+ critical errors), it **automatically escalates to a Havoc Hackathon**  -  up to 14 models compete to rewrite the broken agent, the best version is merged, and Grid-Medic re-diagnoses to confirm the fix.

```
Grid-Medic diagnoses agent fleet
    ├── Score > 5/10 → surgical fix (validate + apply)
    └── Score ≤ 5/10 → 🚨 ESCALATE
            → Havoc Hackathon: up to 14 models compete to rewrite it
            → Ensemble synthesis merges best parts
            → Grid-Medic re-diagnoses → confirms improvement
```

Install: `cp agents/grid-medic.agent.md ~/.copilot/agents/`

---

## 🏆 Gallery

See the best hackathon runs from the community in [GALLERY.md](GALLERY.md).

**Share your own run!** After a hackathon, choose "Save replay" and post it in [Discussions](https://github.com/DUBSOpenHub/havoc-hackathon/discussions/new?category=show-and-tell).

---

## 🔧 Preflight Check

Not sure if everything is set up correctly? Run a dry-run before your first hackathon:

```
> dry run
```

This runs a **full 9-phase simulation** with mock data — validating SQL tables, bracket math, ELO calculations, judge separation, smart mode detection, scoring logic, ensemble voting, and more — all without burning tokens on a real competition. Then it pings each model to confirm availability.

You can also run the offline validators locally:

```bash
python3 tests/validate_skill.py   # 60 structural checks
python3 tests/preflight.py        # SQL, bracket math, file structure
python3 tests/dry_run_sim.py      # Full 9-phase simulation (69 checks)
```

---

## 🔒 Security

See [SECURITY.md](SECURITY.md) for our security policy and how to report vulnerabilities.

---

## 🤝 Contributing

Got ideas to make the arena even better? 🎨 See [CONTRIBUTING.md](CONTRIBUTING.md) for the full guide!

**Quick ways to help:**
- 🐛 [Report a bug](https://github.com/DUBSOpenHub/havoc-hackathon/issues/new?template=bug_report.md)
- 💡 [Suggest a feature](https://github.com/DUBSOpenHub/havoc-hackathon/issues/new?template=feature_request.md)
- 📼 [Share a hackathon run](https://github.com/DUBSOpenHub/havoc-hackathon/discussions/new?category=show-and-tell)

See [TESTING.md](TESTING.md) for conversation playbooks and QA checklists.

---

## 📄 License

[MIT](LICENSE)  -  use it, share it, remix it! 🎶

---

## 🐙 Created with 💜 by [@DUBSOpenHub](https://github.com/DUBSOpenHub) with the [GitHub Copilot CLI](https://docs.github.com/copilot/concepts/agents/about-copilot-cli).

Let's build! 🚀✨
