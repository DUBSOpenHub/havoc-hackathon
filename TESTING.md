# 🧪 Testing Guide

This document describes how to verify the Havoc Hackathon skill works correctly.

Since this is a conversational AI skill (not traditional code), testing is done through **conversation playbooks**  -  scripted interactions that verify expected behavior.

---

## 🎮 How to Test Locally

1. **Register the skill** in a Copilot CLI session:
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
| 5 | *(results)* | Drumroll → winner reveal → ASCII podium → ELO update |

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

### Playbook 7: Audience Participation

| Step | You Say | Expected Behavior |
|------|---------|-------------------|
| 1 | Run a hackathon to completion | After judging, asked "🎙️ Audience vote!" |
| 2 | Rate each submission 1-10 | Scores stored in `hackathon_audience_scores` |
| 3 | *(results)* | Alignment comparison: "You agreed on X but scored Y higher" |

### Playbook 8: Rematch Mode

| Step | You Say | Expected Behavior |
|------|---------|-------------------|
| 1 | Run a hackathon that finishes close (≤2 pts margin) | Offered "🔥 Want a rematch with a tiebreaker?" |
| 2 | Accept and pick a 6th criterion | Re-judging on new criterion only |
| 3 | *(results)* | Combined scores reveal final winner |

### Playbook 9: Replay Export

| Step | You Say | Expected Behavior |
|------|---------|-------------------|
| 1 | Complete any hackathon | Offered "📼 Want the highlight reel?" |
| 2 | Accept | Markdown file saved with full transcript |
| 3 | *(verify)* | File contains banner, submissions, scores, podium |

### Playbook 10: Post-Match Analytics

| Step | You Say | Expected Behavior |
|------|---------|-------------------|
| 1 | Run 2+ hackathons in one session | Performance data accumulated |
| 2 | `show stats` or `show leaderboard` | Model trends, win rates, ASCII bar charts |
| 3 | *(verify)* | Per-model breakdown by task type shown |

### Playbook 11: Persistent ELO

| Step | You Say | Expected Behavior |
|------|---------|-------------------|
| 1 | Run a hackathon | ELO saved to `~/.copilot/hackathon-elo.json` |
| 2 | Start a new Copilot CLI session | ELO loaded from JSON file into SQL |
| 3 | Run another hackathon | Previous ELO ratings shown in Phase 0 |

### Playbook 12: Model Tier Selection

| Step | You Say | Expected Behavior |
|------|---------|-------------------|
| 1 | `run hackathon  -  write a haiku` | Prompted: "⚡ Model tier? Standard or Premium" |
| 2 | Select "Standard" | Standard contestants and judges used, ⚡ badges shown |
| 3 | `run hackathon with premium models  -  write a haiku` | No tier prompt, premium models used directly, 👑 badges shown |
| 4 | `hackathon with opus and gemini  -  write a haiku` | No tier prompt, named models used directly |

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
- [ ] 🎙️ Audience vote prompt appears after judging
- [ ] 🔥 Rematch offered when margin ≤ 2 points
- [ ] 📼 Replay export saves valid markdown file
- [ ] 📊 Post-match analytics display after 2+ hackathons
- [ ] 💾 ELO persists to ~/.copilot/hackathon-elo.json
- [ ] ⚡ Tier selection prompt appears when no tier specified
- [ ] 👑 Premium models used when explicitly requested
- [ ] 🏷️ Tier badges (⚡/👑) shown in opening ceremony

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
| Audience participation | 7 | 🧪 |
| Rematch mode | 8 | 🧪 |
| Replay export | 9 | 🧪 |
| Post-match analytics | 10 | 🧪 |
| Persistent ELO (cross-session) | 11 | 🧪 |
| Model tier selection | 12 | 🧪 |
| Tournament bracket |  -  | 🧪 |
| Adaptive rubrics |  -  | 🧪 |
