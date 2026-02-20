# 📋 Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.1] - 2026-02-20

### Fixed
- 🔧 Added missing `read_agent` and `list_agents` tools to agent.md — required for Phase 3 background task polling
- 🔧 Clarified `read_agent` polling in Phase 3 of SKILL.md (both locations)

### Added
- 🚀 CI validation workflow (`.github/workflows/validate.yml`) — checks SKILL.md sync and catalog.yml validity on push/PR
- ⚖️ Judge model fallback logic in SKILL.md Phase 4 — graceful degradation when premium judges are unavailable
- 🛡️ Prompt injection mitigation section in SECURITY.md — documents anti-gaming protections and consensus safeguards

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
