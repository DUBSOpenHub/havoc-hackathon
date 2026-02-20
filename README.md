# 🏟️ Havoc Hackathon

> **Pit AI models against each other. Score them sealed. Crown a winner.** All from your terminal. ⚡

[![GitHub](https://img.shields.io/badge/GitHub-Copilot_CLI-blue?logo=github)](https://github.com/features/copilot)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Security Policy](https://img.shields.io/badge/Security-Policy-brightgreen?logo=github)](SECURITY.md)

<p align="center">
  <img src="docs/images/hackathon-winner-reveal.png" alt="Havoc Hackathon  -  podium and detailed scoreboard" width="700">
</p>

---

## 🤔 What Is This?

**Havoc Hackathon** is a [Copilot CLI skill](https://docs.github.com/copilot/concepts/agents/about-copilot-cli) that turns your terminal into a competitive arena. Give it any task  -  code, copy, design, architecture, naming, anything  -  and it dispatches multiple AI models to race head-to-head, scores them with a sealed panel of judges, and declares a winner with full ceremony.

### 💡 Why This Exists

I wanted a place to stress-test any idea  -  not just code, but copy, designs, architecture decisions, naming, anything. Instead of asking one model and hoping for the best, Havoc Hackathon lets you throw an idea into the arena and see how multiple AIs attack it independently, then find out which approach actually holds up under sealed evaluation.

### 🧬 Design Philosophy

Under the hood, this is a proper adversarial orchestration harness  -  not just a wrapper around model APIs:

- **Adversarial by design**  -  One model gives you one perspective. Three models competing on the same prompt exposes blind spots, surfaces wildly different approaches, and produces better output through competitive pressure.
- **Sealed judging**  -  Judges never see which model wrote what. Submissions are anonymized, shuffled, and scored independently by three judge models. The final score is the **median consensus**  -  same principle as double-blind peer review, applied to AI.
- **Parallel, not sequential**  -  All contestants race simultaneously. No model sees another's work. No contamination. Fair by construction.
- **CLI-native**  -  No web app, no notebook. Built for the terminal using Copilot CLI's native `task` tool for parallel dispatch, `sql` for ELO tracking, and markdown for the ceremony  -  zero external dependencies.

The result: instead of asking *one* AI and hoping it's good, you force *multiple* AIs to compete, then let a *separate panel* decide who won  -  all without any model knowing who it's up against. The podiums, the drumrolls, the dramatic reveals aren't decoration. They're the point.

### Key Features

- 🏁 **Parallel model dispatch**  -  3+ models race on the same task at the same time
- ⚖️ **Sealed panel judging**  -  3 judges score anonymized submissions  -  no favoritism, no mercy
- 📈 **ELO rating system**  -  persistent leaderboard so you know which models actually deliver
- 🧬 **Intelligent merge**  -  cherry-picks the best pieces from each submission into one output
- 🏆 **Full ceremony**  -  ASCII podiums, drumrolls, fireworks, and play-by-play narration
- ⚡ **Standard / Premium tiers**  -  defaults to standard models, opt into premium when you want the heavy hitters
- 🔄 **Adaptive rubrics**  -  scoring criteria auto-adjust based on task type
- 🎙️ **Audience participation**  -  vote alongside the judges and see if you agree
- 🔥 **Rematch mode**  -  automatic tiebreaker when scores are too close to call
- 📼 **Replay export**  -  save the whole thing as a shareable markdown highlight reel
- 📊 **Post-match analytics**  -  performance trends, win rates, and head-to-head records

---

## 📦 Installation

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
  echo "✅ Installed! Run /skills reload in Copilot CLI, then say: run hackathon"
```

#### Full Install (clone the repo)

```bash
git clone https://github.com/DUBSOpenHub/havoc-hackathon.git && \
  mkdir -p ~/.copilot/skills ~/.copilot/agents && \
  cp -r havoc-hackathon/skills/havoc-hackathon ~/.copilot/skills/ && \
  cp havoc-hackathon/agents/havoc-hackathon.agent.md ~/.copilot/agents/ && \
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

## 🎮 Usage

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

1. **🎬 Opening Ceremony**  -  Arena banner, model tier selection (⚡ Standard or 👑 Premium), contestant lineup, scoring rubric
2. **🏁 The Race**  -  Models dispatched in parallel with live progress commentary
3. **⚖️ Sealed Panel**  -  3 judges score anonymized submissions on 5 criteria (1-10 each)
4. **🏆 Winner Reveal**  -  Drumroll → fireworks → ASCII podium → detailed scoreboard
5. **🧬 Smart Merge**  -  Cherry-pick the best pieces from each submission
6. **📈 ELO Update**  -  Leaderboard changes with commentary
7. **🫡 Closing Ceremony**  -  Final stats, optional report export

### Customize

- Choose model tier: `"run hackathon with premium models"` or `"run hackathon with standard models"`
- Choose specific models: `"hackathon with opus, gemini, and codex"`
- Set custom rubric: `"judge on security, performance, and readability"`
- Tournament mode: `"bracket tournament with 6 models"`
- Show stats: `"show leaderboard"` or `"show stats"` anytime

<details>
<summary><strong>📼 Example Run  -  Full Hackathon Transcript</strong></summary>

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
  🟢 Codex Max (GPT-5.1)   (Premium)
  🟡 Gemini 3 Pro          (Premium)

⚖️ RUBRIC: Clarity · Simplicity · Relevance · Inspiration · Memorability (each /10)

3... 2... 1... GO! 🏁

🏁 ALL MODELS CROSSED THE FINISH LINE!
  🔵 Claude Opus 4.6     ✅ 4s ⚡
  🟢 Codex Max           ✅ 3s ⚡ Speedrun!
  🟡 Gemini 3 Pro        ✅ 10s

⚖️ The panel convenes... 🔒 Submissions anonymized. No favoritism. No mercy.
   👨‍⚖️ Judges: Claude Opus 4.5 · Claude Opus 4.6 Fast · Claude Opus 4.6 1M

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
       │ MAX  │ │      │ │3 PRO │
       │  37  │ │      │ │  35  │
       └──────┘ └──────┘ └──────┘

📊 DETAILED SCOREBOARD
  Category      🥇 Claude Opus  🥈 Codex Max  🥉 Gemini 3 Pro
  Clarity            9              8              7
  Simplicity         8              7              5
  Relevance          9              8              8
  Inspiration        9              7              8
  Memorability       8              7              7
  TOTAL           43/50          37/50          35/50

📈 ELO UPDATE
  📈 Claude Opus 4.6   1532  (+32) ⬆️
  ➡️  Codex Max         1500  (±0)
  📉 Gemini 3 Pro      1468  (-32) ⬇️

GG WP! Scores logged. ELOs updated. 🫡
```

</details>

---

## 🏗️ Architecture

```mermaid
flowchart TD
    USER["👤 User"] --> SKILL["🏟️ SKILL.md<br/>Orchestration rules"]
    SKILL --> DISPATCH["⚡ Parallel Dispatch<br/>task tool + background mode"]
    DISPATCH --> M1["🤖 Model A"]
    DISPATCH --> M2["🤖 Model B"]
    DISPATCH --> M3["🤖 Model C"]
    M1 --> COLLECT["📦 Collect & Normalize"]
    M2 --> COLLECT
    M3 --> COLLECT
    COLLECT --> ANONYMIZE["🔒 Anonymize"]
    ANONYMIZE --> J1["⚖️ Judge 1"]
    ANONYMIZE --> J2["⚖️ Judge 2"]
    ANONYMIZE --> J3["⚖️ Judge 3"]
    J1 --> CONSENSUS["🧑‍⚖️ Median Consensus"]
    J2 --> CONSENSUS
    J3 --> CONSENSUS
    CONSENSUS --> REVEAL["🏆 Winner Reveal"]
    REVEAL --> ELO["📈 ELO Update"]
    ELO --> MERGE["🧬 Smart Merge"]
    SKILL --> SQL["🗄️ SQL<br/>ELO & history"]
```

---

## 🏗️ Project Structure

```
havoc-hackathon/
├── .github/
│   ├── CODEOWNERS                    ← 👑 Code ownership rules
│   ├── ISSUE_TEMPLATE/               ← 🐛 Bug & feature templates
│   ├── PULL_REQUEST_TEMPLATE.md      ← 📝 PR checklist
│   ├── dependabot.yml                ← 🤖 Automated dependency updates
│   ├── workflows/
│   │   └── validate.yml              ← ✅ CI: SKILL.md sync + YAML check
│   └── skills/
│       └── havoc-hackathon/
│           └── SKILL.md              ← 🏟️ Auto-discovered skill
├── agents/
│   └── havoc-hackathon.agent.md      ← 🤖 Agent config (for task tool)
├── docs/
│   ├── TECHNICAL.md                  ← 🔬 Technical deep-dive
│   └── images/                       ← 📷 Screenshots
├── skills/
│   └── havoc-hackathon/
│       ├── SKILL.md                  ← 🏟️ Canonical skill source
│       └── catalog.yml               ← 📋 Catalog metadata
├── .gitignore
├── CHANGELOG.md                      ← 📋 Version history
├── CODE_OF_CONDUCT.md                ← 🤝 Contributor Covenant
├── CONTRIBUTING.md                   ← 🛠️ How to contribute
├── LICENSE                           ← 📄 MIT
├── SECURITY.md                       ← 🔒 Security policy
├── TESTING.md                        ← 🧪 Conversation playbooks & QA
└── README.md                         ← 👋 You are here!
```

---

## 📊 Available Models

| Display Name | Model ID | Tier |
|-------------|----------|------|
| Claude Opus 4.6 | `claude-opus-4.6` | Premium |
| Claude Opus 4.6 (Fast) | `claude-opus-4.6-fast` | Premium |
| Claude Opus 4.6 (1M) | `claude-opus-4.6-1m` | Premium |
| Claude Opus 4.5 | `claude-opus-4.5` | Premium |
| Codex Max (GPT-5.1) | `gpt-5.1-codex-max` | Premium |
| Gemini 3 Pro | `gemini-3-pro-preview` | Premium |
| Claude Sonnet 4.6 | `claude-sonnet-4.6` | Standard |
| Claude Sonnet 4.5 | `claude-sonnet-4.5` | Standard |
| Codex (GPT-5.3) | `gpt-5.3-codex` | Standard |
| Codex (GPT-5.2) | `gpt-5.2-codex` | Standard |
| GPT-5.2 | `gpt-5.2` | Standard |
| GPT-5.1 | `gpt-5.1` | Standard |

**Default contestants (Standard ⚡):** Claude Sonnet 4.6, Codex (GPT-5.3), GPT-5.2
**Default contestants (Premium 👑):** Claude Opus 4.6, Codex Max (GPT-5.1), Gemini 3 Pro
**Default judges (Standard ⚡):** Claude Sonnet 4.5, Codex (GPT-5.2), GPT-5.1
**Default judges (Premium 👑):** Claude Opus 4.5, Claude Opus 4.6 (Fast), Claude Opus 4.6 (1M)

> 💡 **Tip:** Standard models are selected by default. Say `"run hackathon with premium models"` to use the heavy hitters.

---

## 🔒 Security

See [SECURITY.md](SECURITY.md) for our security policy and how to report vulnerabilities.

---

## 🤝 Contributing

Got ideas to make the arena even better? 🎨 See [CONTRIBUTING.md](CONTRIBUTING.md) for the full guide!

**Quick ways to help:**
- 🐛 [Report a bug](https://github.com/DUBSOpenHub/havoc-hackathon/issues/new?template=bug_report.md)
- 💡 [Suggest a feature](https://github.com/DUBSOpenHub/havoc-hackathon/issues/new?template=feature_request.md)

See [TESTING.md](TESTING.md) for conversation playbooks and QA checklists.

---

## 📄 License

[MIT](LICENSE)  -  use it, share it, remix it! 🎶

---

## 🐙 Built with Love

Created with 💜 by [DUBSOpenHub](https://github.com/DUBSOpenHub) to help more people discover the joy of GitHub Copilot CLI.

**Let's build!** 🚀✨
