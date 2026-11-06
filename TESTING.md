# 🧪 Testing Guide

This document describes how to verify the Havoc Hackathon skill works correctly.

Offline regression tests validate the roster, formulas, schemas and instruction
contracts. Conversation playbooks below still require observed live results;
offline success is not proof of model availability or complete orchestration.

```bash
python3 -B -m unittest discover -s tests -p 'test_*.py'
python3 -B scripts/refresh_models.py --check
python3 -B tests/validate_skill.py
python3 -B tests/preflight.py
python3 -B tests/dry_run_sim.py
bash -n quickstart.sh
```

Sideline regressions cover pending scores, failures versus successful work,
evidence-backed scores, duplicate contestants and required handoffs in all modes.
The structural validator rejects missing sideline fields or transitions.
No live probes, telemetry, real rating writes or large-agent launches are part
of these commands. See `docs/SKILL-REVIEW.md` for review scope and limitations.

---

## 🎮 How to Test Locally

1. **Register the skill** in a GitHub Copilot CLI session:
   ```
   /skills add ./
   ```

2. **Run each playbook** below and verify the expected behavior.

3. **Check the QA checklist** at the bottom before submitting a PR.

---

## 📋 Conversation Playbooks

### Playbook 1: Basic Code Hackathon

| Step | You Say | Expected Behavior |
|------|---------|-------------------|
| 1 | `run hackathon  -  write a fizzbuzz function` | Opening ceremony with arena banner, contestants, rubric |
| 2 | *(accept defaults or customize)* | 3 models dispatched in parallel with progress commentary |
| 3 | *(wait for completion)* | All models finish, outputs normalized |
| 4 | *(judging phase)* | Sealed panel scores anonymized submissions |
| 5 | *(results)* | Public scores → podium → approved synthesis/integration → ELO update |

### Playbook 2: Review Mode

| Step | You Say | Expected Behavior |
|------|---------|-------------------|
| 1 | `run hackathon  -  review @src/app.js for security issues` | Detects review mode, adjusts rubric |
| 2 | *(models complete)* | Each model produces structured findings |
| 3 | *(results)* | Ensemble report showing consensus findings |

### Playbook 3: Custom Models

| Step | You Say | Expected Behavior |
|------|---------|-------------------|
| 1 | `hackathon with opus and gemini  -  refactor this function` | Only 2 models dispatched (head-to-head mode) |
| 2 | *(results)* | Head-to-head comparison, no bracket/tournament |

### Playbook 4: Model Failure

| Step | You Say | Expected Behavior |
|------|---------|-------------------|
| 1 | `run hackathon` on a complex task | If a model fails, it retries once |
| 2 | *(second failure)* | Model DQ'd with flair ("💀 ELIMINATED") |
| 3 | *(remaining models)* | Hackathon continues with surviving contestants |

### Playbook 5: ELO Persistence

| Step | You Say | Expected Behavior |
|------|---------|-------------------|
| 1 | Run hackathon #1 | ELO table created, initial ratings set |
| 2 | Run hackathon #2 | ELO from previous run shown, ratings updated |
| 3 | `show leaderboard` | Current ELO rankings displayed |

### Playbook 6: Smart Merge

| Step | You Say | Expected Behavior |
|------|---------|-------------------|
| 1 | Complete a build hackathon | Merge options presented |
| 2 | Select "Smart merge" | Best components cherry-picked from each submission |
| 3 | *(verify)* | Build passes, tests pass after merge |

### Playbook 7: Rematch Mode

| Step | You Say | Expected Behavior |
|------|---------|-------------------|
| 1 | Run a hackathon that finishes close (≤2 pts margin) | Offered "🔥 Want a rematch with a tiebreaker?" |
| 2 | Accept a separate rematch | Declare its rubric before launching; retain original /50 result |
| 3 | *(results)* | Separate rematch result; no retroactive reweighting |

### Playbook 8: Replay Export

| Step | You Say | Expected Behavior |
|------|---------|-------------------|
| 1 | Complete any hackathon | Offered "📼 Want the highlight reel?" |
| 2 | Accept | Markdown file saved with full transcript |
| 3 | *(verify)* | File contains banner, submissions, scores, podium |

### Playbook 9: Post-Match Analytics

| Step | You Say | Expected Behavior |
|------|---------|-------------------|
| 1 | Run 2+ hackathons in one session | Performance data accumulated |
| 2 | `show stats` or `show leaderboard` | Model trends, win rates, ASCII bar charts |
| 3 | *(verify)* | Per-model breakdown by task type shown |

### Playbook 10: Persistent ELO

| Step | You Say | Expected Behavior |
|------|---------|-------------------|
| 1 | Run a hackathon | ELO saved to `~/.copilot/hackathon-elo.json` |
| 2 | Start a new GitHub Copilot CLI session | Validated legacy ELO loaded without deleting historical models |
| 3 | Run another hackathon | Previous ELO ratings shown in Phase 0 |

### Playbook 11: Model Tier Selection

| Step | You Say | Expected Behavior |
|------|---------|-------------------|
| 1 | `run hackathon  -  write a haiku` | Prompted: "⚡ Model tier? Standard or Premium" |
| 2 | Select "Standard" | Standard contestants and judges used, ⚡ badges shown |
| 3 | `run hackathon with premium models  -  write a haiku` | No tier prompt, premium models used directly, 👑 badges shown |
| 4 | `hackathon with opus and gemini  -  write a haiku` | No tier prompt, named models used directly |

### Playbook 12: Stall Detection

| Step | You Say | Expected Behavior |
|------|---------|-------------------|
| 1 | Run a hackathon on a complex task | Models dispatched, progress monitored |
| 2 | *(model stalls for 180s)* | Prompted: "⏳ {Model} has been silent for 3 minutes. Want to keep waiting or DQ?" |
| 3 | Select "Keep waiting (60s more)" | Timer extended by 60 seconds |
| 4 | *(model stalls again)* | Auto-DQ with commentary: "💀 {Model} went AFK. No mercy in this arena." |
| 5 | *(alternative: select "DQ and continue")* | Model DQ'd immediately, hackathon continues with remaining contestants |

### Playbook 13: Tournament Mode (Default)

| Step | You Say | Expected Behavior |
|------|---------|-------------------|
| 1 | `run hackathon  -  refactor this module` | Tournament mode activates by default, all available models enter |
| 2 | *(Round 1)* | Models grouped into heats (elastic brackets based on count). Each heat runs in parallel. |
| 3 | *(heat judging)* | Per-heat judge panels (3 judges each) score independently in parallel |
| 4 | *(heat results)* | Mini-ceremony per heat winner: "🏅 {Model} takes Heat {N}!" |
| 5 | *(Round 2)* | Finalists dispatched with Evolution Brief prepended |
| 6 | *(finals judging + results)* | Full ceremony, tournament bracket recap in closing |

### Playbook 14: Evolution Brief

| Step | You Say | Expected Behavior |
|------|---------|-------------------|
| 1 | Complete Round 1 of a tournament hackathon | Evolution Brief generated from judge scores |
| 2 | *(verify)* | Brief includes: winning strategies per heat, top scoring categories, key differentiators |
| 3 | *(Round 2)* | Finalists receive the brief — commentary: "🧬 Finalists have studied the playbook." |

### Playbook 15: Ensemble Synthesis

| Step | You Say | Expected Behavior |
|------|---------|-------------------|
| 1 | Complete a tournament hackathon (build mode) | Merge options presented with "Ensemble synthesis" as recommended |
| 2 | Select "Ensemble synthesis" | Integrator agent analyzes ALL finalist submissions |
| 3 | *(verify)* | Output shows CONSENSUS/MAJORITY/UNIQUE classifications with provenance annotations |

### Playbook 16: Classic Mode Fallback

| Step | You Say | Expected Behavior |
|------|---------|-------------------|
| 1 | `run hackathon quick  -  write a haiku` | Classic mode: 3 contestants, no heats, single round |
| 2 | *(verify)* | Identical behavior to v1.x — no tournament, no evolution brief |
| 3 | `run hackathon fast  -  name this variable` | Same classic mode behavior |

### Playbook 17: Grid-Medic Escalation

| Step | You Say | Expected Behavior |
|------|---------|-------------------|
| 1 | Run grid-medic `diagnose` on an agent scoring ≤5/10 | Grid-medic detects critical underperformance |
| 2 | *(escalation prompt)* | "🚨 {agent} is critically underperforming. Escalate to Havoc Hackathon?" |
| 3 | Select "Escalate to Hackathon" | Havoc Hackathon triggered to competitively rewrite the agent |
| 4 | *(after hackathon completes)* | Grid-medic re-diagnoses the upgraded agent, logs score delta |

---

## ✅ QA Checklist

Before submitting a PR, verify:

- [ ] 🏁 Opening ceremony displays correctly (banner, contestants, rubric)
- [ ] ⚡ Models dispatch in parallel (not sequentially)
- [ ] 🔒 Submissions are anonymized before judging
- [ ] ⚖️ 3 judges score independently, median taken
- [ ] 🏆 Winner reveal has dramatic ceremony (drumroll, podium)
- [ ] 📈 ELO ratings update correctly after each hackathon
- [ ] 🔄 Failed models retry once, then DQ
- [ ] 🧬 Smart merge produces working code
- [ ] 🎭 MC personality is consistent throughout
- [ ] 🚦 Quality gates catch broken builds/tests
- [ ] 🔥 Rematch offered when margin ≤ 2 points
- [ ] 📼 Replay export saves valid markdown file
- [ ] 📊 Post-match analytics display after 2+ hackathons
- [ ] 💾 ELO persists to ~/.copilot/hackathon-elo.json
- [ ] ⚡ Tier selection prompt appears when no tier specified
- [ ] 👑 Premium models used when explicitly requested
- [ ] 🏷️ Tier badges (⚡/👑) shown in opening ceremony
- [ ] ⏳ Stall detection prompts user after 180s of no output
- [ ] 💀 Auto-DQ on second stall after user-granted extension
- [ ] 🏟️ Classic for simple tasks; Tournament for complex tasks or explicit mode request
- [ ] 🔥 Elastic brackets size heats correctly for model count
- [ ] 🏅 Per-heat judge panels run in parallel (3 judges × N heats)
- [ ] 🧬 Evolution Brief generated between rounds from judge scores
- [ ] 🏁 Round 2 finalists receive Evolution Brief in their prompt
- [ ] 🗳️ Ensemble synthesis shows CONSENSUS/MAJORITY/UNIQUE classifications
- [ ] ⚡ Classic mode ("quick"/"fast") produces same 3-model experience
- [ ] 🚑 Grid-medic escalation triggers hackathon for weak agents

---

## 🔍 YAML/Markdown Validation

Verify catalog metadata:

```bash
# Check YAML syntax
python3 -c "import yaml; yaml.safe_load(open('skills/havoc-hackathon/catalog.yml'))" && echo "✅ YAML valid"

# Check required fields
python3 -c "
import yaml
d = yaml.safe_load(open('skills/havoc-hackathon/catalog.yml'))
required = ['schema_version','id','name','description','emoji','codename','category']
missing = [f for f in required if f not in d]
print('✅ All required fields present' if not missing else f'❌ Missing: {missing}')
"
```

---

## 📊 Coverage Matrix

| Feature | Playbook | Status |
|---------|----------|--------|
| Basic code hackathon | 1 | 🧪 |
| Review mode | 2 | 🧪 |
| Custom model selection | 3 | 🧪 |
| Model failure & DQ | 4 | 🧪 |
| ELO persistence | 5 | 🧪 |
| Smart merge | 6 | 🧪 |
| Rematch mode | 7 | 🧪 |
| Replay export | 8 | 🧪 |
| Post-match analytics | 9 | 🧪 |
| Persistent ELO (cross-session) | 10 | 🧪 |
| Model tier selection | 11 | 🧪 |
| Stall detection | 12 | 🧪 |
| Tournament bracket |  -  | 🧪 |
| Adaptive rubrics |  -  | 🧪 |
| Tournament mode (default) | 13 | 🧪 |
| Evolution brief | 14 | 🧪 |
| Ensemble synthesis | 15 | 🧪 |
| Classic mode fallback | 16 | 🧪 |
| Grid-medic escalation | 17 | 🧪 |
