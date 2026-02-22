# 🔬 Technical Overview

## The Problem

When you ask one LLM to review code, write a function, or analyze a PR, you get **one perspective with unknown quality**. You have no baseline, no comparison, and no way to know if the output is the model's best work or a mediocre first draft. You're trusting a single stochastic process.

## The Solution

Havoc Hackathon implements **Layer 1 multi-model consensus with tournament elimination, evolutionary pressure, and ensemble synthesis**  -  a pattern borrowed from academic peer review and tournament theory, applied to AI-assisted development.

**Architecture:**

```
User prompt → Tournament Mode (default): all available models enter
           → Round 1: Elastic heats (auto-sized by model count)
           → Per-heat judge panels score sealed (3 judges × N heats, parallel)
           → Heat winners advance
           → Evolution Brief: orchestrator summarizes winning strategies
           → Round 2: Finalists compete with Evolution Brief prepended
           → Finals judge panel scores sealed
           → Ensemble synthesis: CONSENSUS/MAJORITY/UNIQUE voting merge
           → ELO update (per-round, per-heat) for long-term model tracking
```

## Why This Is Technically Valuable

### 1. Reduces single-model failure modes

Every model has blind spots. GPT models tend toward verbosity. Claude models can over-qualify. Gemini handles structured data differently. By running **all available models** in tournament heats, you get **maximum coverage across failure modes**. The elimination tournament ensures only the strongest approaches survive to the finals.

### 2. Evolution between rounds compounds quality

Round 2 finalists receive an Evolution Brief  -  a structured summary of what strategies won each heat, which scoring categories drove the wins, and key differentiators. Finalists can incorporate or beat those ideas. This means Round 2 output is strictly better than Round 1, creating evolutionary pressure that a single-round competition can't match.

### 2. Sealed judging eliminates brand bias

Submissions are anonymized as Contestant-A/B/C before judging. Judge models score on evidence, not reputation. This matters  -  studies show humans (and models) rate outputs higher when they know the source. Sealed panels remove that.

### 3. Median-of-3 consensus is statistically robust

Three judges score independently. Final score = median, not mean. This makes the scoring resistant to one outlier judge being miscalibrated. If stddev > 2.0, the system flags it and can split criteria for re-evaluation.

### 4. ELO tracking reveals model strengths over time

After multiple hackathons, you build empirical data: "Claude Opus wins 70% of review tasks but only 40% of code generation tasks." This turns model selection from vibes into evidence. The data persists across sessions via `~/.copilot/hackathon-elo.json`.

### 5. Ensemble synthesis > winner-take-all

The ensemble synthesis doesn't just pick the winner's output. It uses a **voting merge across ALL finalists**: if 3+ models solved something the same way (CONSENSUS), that approach auto-wins. If 2 agree (MAJORITY), that's accepted with the alternative noted. If all differ (UNIQUE), the highest scorer's approach wins. Unique innovations from any finalist are preserved and flagged for review. The result is collective intelligence no single model could produce.

### 6. Zero infrastructure overhead

No API keys, no orchestration server, no Docker containers. It's three markdown files (SKILL.md + two .agent.md files) that leverage Copilot CLI's existing `task` tool for parallel dispatch and `sql` tool for state management. The entire system runs in your terminal.

## When to Use It

| Use Case | Why It Helps |
|----------|-------------|
| **Code review** | 3 models find different bugs; ensemble report shows consensus findings |
| **Architecture decisions** | Compare 3 different approaches side-by-side with sealed scoring |
| **Refactoring** | Multiple implementations scored on correctness, clarity, maintainability |
| **Security audits** | Models have different vulnerability detection strengths |
| **Writing (docs, ADRs)** | Reduces single-model tone/style bias |

## What It's Not

It's not a replacement for human review. It's a **force multiplier**  -  you get 3 drafts and a ranked comparison instead of 1 draft and a gut check. The human still decides what ships.
