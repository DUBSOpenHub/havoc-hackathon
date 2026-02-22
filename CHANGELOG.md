# 📋 Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.0] - 2026-02-22

### Added
- 🏟️ **Layer 1: Tournament Mode (default)**  -  All available models (up to 12) compete in elimination heats instead of just 3. Elastic brackets auto-size based on model count (12→4×3, 9→3×3, 6→2×3, ≤4→classic). Serpentine ELO-based seeding spreads top models across heats.
- 🧬 **Evolution Brief**  -  After Round 1 judging, orchestrator generates a structured brief from judge scores: winning strategies, top categories, key differentiators. Prepended to Round 2 prompt so finalists can incorporate or beat Round 1's best ideas. Zero extra LLM calls.
- 🗳️ **Ensemble Synthesis**  -  Replaces cherry-pick-from-winner with voting merge across ALL finalists. CONSENSUS (3+ agree, auto-accept), MAJORITY (2 agree, note alternative), UNIQUE (highest scorer wins, flag others). Integrator agent gets explicit merge rules with provenance annotations.
- ⚖️ **Per-heat judge panels**  -  3 judges × N heats dispatched in parallel (up to 12 judge agents in Round 1). Judge model assignments rotate across heats for diverse perspectives.
- 🃏 **Wildcard entry**  -  If an entire heat is DQ'd, the highest-scoring eliminated model from another heat gets a wildcard entry to the finals.
- 🎤 **3 new commentary lines**  -  Heat advance, evolution, and ensemble quips.
- 🏗️ **Tournament bracket recap**  -  Phase 8 closing ceremony shows visual bracket (N models → heats → finalists → champion).
- 📊 **Per-round ELO**  -  ELO adjustments calculated within heats (Round 1) and finals (Round 2) separately, generating more data points per hackathon.
- 🗄️ **`round` column**  -  Added to `hackathon_judge_scores`, `hackathon_consensus`, and `hackathon_results` tables for cross-round analytics.

### Changed
- Default mode changed from 3-model direct competition to tournament elimination with all available models.
- Phase 6 merge option renamed from "Smart merge" to "Ensemble synthesis" with explicit CONSENSUS/MAJORITY/UNIQUE voting rules.
- Agent count per full tournament run: ~8 → ~28.

### Preserved
- Classic Mode via "quick" or "fast" keywords  -  identical 3-model behavior as v1.x.
- Same 9 phases (0-8), same MC energy, same ask_user prompts, same closing ceremony.
- All existing features, commentary lines, and rules preserved (new items are additive only).

## [1.3.1] - 2026-02-21

### Fixed
- 🔧 **Results display before merge prompt**  -  Phase 5 now has explicit numbered checklist of mandatory display items (scoreboard, comparison view, strengths/weaknesses). Phase 6 adds a "Results Gate" requiring results to be displayed before calling `ask_user` for merge options. Removed "proceed immediately" language that caused models to rush past showing results.

## [1.3.0] - 2026-02-20

### Added
- ⏳ **Stall detection**  -  if a contestant produces no output after 180 seconds, asks the user whether to keep waiting (60s extension) or DQ and continue. Auto-DQs on second stall.

## [1.2.0] - 2026-02-20

### Added
- ⚡ **Model tier selection**  -  prompts user to choose Standard or Premium models before each hackathon
- Standard tier defaults: Claude Sonnet 4.6, Codex Max (GPT-5.1), GPT-5.2 (contestants) + Claude Sonnet 4.5, Codex (GPT-5.2), GPT-5.1 (judges)
- Premium tier opt-in via `"run hackathon with premium models"` or explicit model names
- Tier badges (⚡ STANDARD / 👑 PREMIUM) shown in opening ceremony

### Changed
- Default tier changed from Premium to Standard  -  works for all Copilot subscription levels out of the box

### Removed
- 🗑️ **Tag team mode**  -  removed from SKILL.md and agent.md

## [1.1.0] - 2026-02-20

### Added
- 🔥 **Rematch mode**  -  tiebreaker round with user-chosen 6th criterion when margin ≤ 2 points
- 📼 **Replay export**  -  save full hackathon transcript as shareable markdown highlight reel
- 📊 **Post-match analytics**  -  model performance trends, win rates by task type, ASCII charts
- 💾 **Persistent ELO**  -  leaderboard saved to `~/.copilot/hackathon-elo.json` across sessions
- 🧪 Playbooks 7-11 in TESTING.md covering all new features
- ✅ 6 new QA checklist items

## [1.0.1] - 2026-02-20

### Fixed
- 🔧 Added missing `read_agent` and `list_agents` tools to agent.md  -  required for Phase 3 background task polling
- 🔧 Clarified `read_agent` polling in Phase 3 of SKILL.md (both locations)

### Added
- 🚀 CI validation workflow (`.github/workflows/validate.yml`)  -  checks SKILL.md sync and catalog.yml validity on push/PR
- ⚖️ Judge model fallback logic in SKILL.md Phase 4  -  graceful degradation when premium judges are unavailable
- 🛡️ Prompt injection mitigation section in SECURITY.md  -  documents anti-gaming protections and consensus safeguards

### Changed
- 🔐 Updated SECURITY.md security features table to reflect current activation status

## [1.0.0] - 2026-02-19

### Added
- 🏟️ Initial release
- ⚡ Parallel multi-model dispatch via `task` tool
- ⚖️ Sealed panel judging with 3 judge models and median consensus
- 📈 ELO rating system with persistent leaderboard
- 🧬 Intelligent merge with component-level cherry-picking
- 🏆 Full ceremony: ASCII podium, dramatic reveals, color commentary
- 🔄 Adaptive rubrics (auto-detect task type, adjust weights)
- 🚦 Quality gates with automated build/test/lint checks
- 🛡️ Anti-gaming protections (calibration anchors, stuffing detection)
- 📊 Tournament bracket mode for 6+ model competitions
- 🎭 Esports MC personality with contextual commentary
- 📋 4 default scoring rubrics (Code, Design, Review, Branding)
