# 🧪 Testing Guide

This document describes how to verify the Havoc Hackathon skill works correctly.

Since this is a conversational AI skill (not traditional code), testing is done through **conversation playbooks** — scripted interactions that verify expected behavior.

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
| 1 | `run hackathon — write a fizzbuzz function` | Opening ceremony with arena banner, contestants, rubric |
| 2 | *(accept defaults or customize)* | 3 models dispatched in parallel with progress commentary |
| 3 | *(wait for completion)* | All models finish, outputs normalized |
| 4 | *(judging phase)* | Sealed panel scores anonymized submissions |
| 5 | *(results)* | Drumroll → winner reveal → ASCII podium → ELO update |

### Playbook 2: Review Mode

| Step | You Say | Expected Behavior |
|------|---------|-------------------|
| 1 | `run hackathon — review @src/app.js for security issues` | Detects review mode, adjusts rubric |
| 2 | *(models complete)* | Each model produces structured findings |
| 3 | *(results)* | Ensemble report showing consensus findings |

### Playbook 3: Custom Models

| Step | You Say | Expected Behavior |
|------|---------|-------------------|
| 1 | `hackathon with opus and gemini — refactor this function` | Only 2 models dispatched (head-to-head mode) |
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
| Tournament bracket | — | 🧪 |
| Adaptive rubrics | — | 🧪 |
