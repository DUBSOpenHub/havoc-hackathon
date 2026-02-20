# 🔬 Technical Overview

## The Problem

When you ask one LLM to review code, write a function, or analyze a PR, you get **one perspective with unknown quality**. You have no baseline, no comparison, and no way to know if the output is the model's best work or a mediocre first draft. You're trusting a single stochastic process.

## The Solution

Havoc Hackathon implements **multi-model consensus with blind evaluation**  -  a pattern borrowed from academic peer review and applied to AI-assisted development.

**Architecture:**

```
User prompt → Identical dispatch to N models (parallel)
           → Outputs normalized + anonymized
           → M judge models score blindly (sealed panel)
           → Median consensus scoring (reduces judge bias)
           → Winner + ensemble merge of best components
           → ELO update for long-term model tracking
```

## Why This Is Technically Valuable

### 1. Reduces single-model failure modes

Every model has blind spots. GPT models tend toward verbosity. Claude models can over-qualify. Gemini handles structured data differently. By running 3+ models on the same task, you get **coverage across failure modes**. If two models catch a bug and one misses it, the ensemble surfaces it.

### 2. Blind judging eliminates brand bias

Submissions are anonymized as Contestant-A/B/C before judging. Judge models score on evidence, not reputation. This matters  -  studies show humans (and models) rate outputs higher when they know the source. Sealed panels remove that.

### 3. Median-of-3 consensus is statistically robust

Three judges score independently. Final score = median, not mean. This makes the scoring resistant to one outlier judge being miscalibrated. If stddev > 2.0, the system flags it and can split criteria for re-evaluation.

### 4. ELO tracking reveals model strengths over time

After multiple hackathons, you build empirical data: "Claude Opus wins 70% of review tasks but only 40% of code generation tasks." This turns model selection from vibes into evidence. The data persists across sessions via `~/.copilot/hackathon-elo.json`.

### 5. Component-level merging > winner-take-all

The smart merge doesn't just pick the winner's output. It cherry-picks at the component level  -  maybe Model A had better error handling but Model B had a cleaner API design. You get the best of each.

### 6. Zero infrastructure overhead

No API keys, no orchestration server, no Docker containers. It's two markdown files that leverage Copilot CLI's existing `task` tool for parallel dispatch and `sql` tool for state management. The entire system runs in your terminal.

## When to Use It

| Use Case | Why It Helps |
|----------|-------------|
| **Code review** | 3 models find different bugs; ensemble report shows consensus findings |
| **Architecture decisions** | Compare 3 different approaches side-by-side with blind scoring |
| **Refactoring** | Multiple implementations scored on correctness, clarity, maintainability |
| **Security audits** | Models have different vulnerability detection strengths |
| **Writing (docs, ADRs)** | Reduces single-model tone/style bias |

## What It's Not

It's not a replacement for human review. It's a **force multiplier**  -  you get 3 drafts and a ranked comparison instead of 1 draft and a gut check. The human still decides what ships.
