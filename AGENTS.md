# Agents

## Overview

Havoc Hackathon ships two Copilot CLI agents and one skill. The **skill** (`havoc-hackathon`) is the primary entry point — it orchestrates full multi-model tournaments. The **havoc-hackathon agent** is a standalone agent version of the same capability. The **grid-medic agent** is bundled as a companion for keeping the tournament infrastructure healthy.

## Available Agents

### havoc-hackathon (Skill)

- **Purpose**: Multi-model AI tournament orchestrator. Dispatches up to 14 AI models in elimination heats, scores them with sealed judge panels (judges never know which model wrote what), evolves the best ideas between rounds, synthesizes a final output from all finalists, and maintains persistent ELO ratings across sessions.
- **Usage**: Install via Copilot CLI, then invoke with natural language:
  ```
  run hackathon                        # Full tournament on whatever you describe
  run hackathon express                # Quick single-round version
  /skills add DUBSOpenHub/havoc-hackathon  # Instant install
  ```
- **Model**: Dispatches to all available models in your Copilot CLI session
- **Install**:
  ```bash
  mkdir -p ~/.copilot/skills/havoc-hackathon ~/.copilot/agents && \
    curl -sL https://raw.githubusercontent.com/DUBSOpenHub/havoc-hackathon/main/skills/havoc-hackathon/SKILL.md \
      -o ~/.copilot/skills/havoc-hackathon/SKILL.md
  ```
- **Location**: `skills/havoc-hackathon/SKILL.md`

### havoc-hackathon (Agent)

- **Purpose**: Standalone agent version of the tournament orchestrator. Use when you want the Havoc Hackathon capability as a named agent rather than a skill.
- **Usage**: After installing `~/.copilot/agents/havoc-hackathon.agent.md`, invoke via the agent selector in Copilot CLI.
- **Location**: `agents/havoc-hackathon.agent.md`

### grid-medic

- **Purpose**: Companion agent bundled with Havoc Hackathon. Self-healing meta-agent that monitors and repairs the `.agent.md` files in your fleet — including Havoc Hackathon's own agent files. See [DUBSOpenHub/grid-medic](https://github.com/DUBSOpenHub/grid-medic) for full documentation.
- **Usage**:
  ```
  grid-medic diagnose
  grid-medic improve havoc-hackathon
  ```
- **Location**: `agents/grid-medic.agent.md`

## Configuration

- **No API keys required** — all models are accessed through your active Copilot subscription
- **No servers or infrastructure** — tournament state lives in memory during the session
- **Persistent ELO ratings** — stored locally; each tournament updates model rankings
- **Judge panels**: 3 judges × N heats run in parallel; judges are isolated from model identity
- **Sealed judging**: judges never see which model produced which output — scores are unbiased
- **Evolution between rounds**: Round 2 finalists receive the winning patterns from Round 1
