# Havoc Hackathon skill review

Reviewed November 5, 2026, using Looper. Scope: the complete canonical skill,
installed-only additions, model configuration/refresher, packaging aliases,
offline validators and CI. Existing unfinished model updates were retained.
This is a maintenance review, not a tournament or model-quality benchmark.

## Model upgrade

The active GitHub Copilot CLI 1.0.106 `task` tool schema exposed 27 explicit
model IDs. `config/runtime-models.json` records those exact IDs, providers,
local lineup labels and support for `max` reasoning / long context. The
generated catalog must match that reviewed snapshot. `auto` is not a contestant.

Added missing GPT-5.6 Sol Fast, GPT-6.1 Sol Fast, MAI-Code-2, MAI-Code-2-Flash
and three environment-specific custom-provider models. Claude Opus 4.8, Kimi K3
and Grok 4.5 appeared in the previous catalog but not this runtime schema, so
they are excluded from this snapshot, not declared globally retired.
Standard Classic defaults: Claude Sonnet 5.5, GPT-6.1 Sol Fast, Gemini 4 Argon.
Premium Classic defaults: Claude Opus 5.5, GPT-6.1 Sol, GPT-6.1 Terra.
Judge defaults are disjoint and span multiple providers.

The official supported-model page was checked as a secondary source. It lists
public products, not exact account-specific dispatch enums. The refresher now
reports Docs-only candidates instead of manufacturing IDs from display names.
Refresh `config/runtime-models.json` from the current tool schema before relying
on future availability. Schema eligibility does not prove an account can invoke
a model or that a model has responded. No paid model probes were run.

Source: <https://docs.github.com/en/copilot/reference/ai-models/supported-models>

## Complete section review

| Area | Finding and disposition |
|---|---|
| Metadata / entry point | Version 3.1.0; maintenance requests no longer start an arena or mutate ratings. Metaswarm discoverability restored from installed-only content. |
| Tone / broadcast rules | Preserve the MC style, but explicit boundaries prioritize truth, errors, approvals and user-requested details. No simulated progress presented as live. |
| Phase 0 / leaderboard | Reuse an existing challenge; missing input uses structured elicitation. Preserve old model entries; require ordered history for streak claims. |
| Phase 1 / selection | Current task schema and account policy override stale tables. Exact custom IDs retained. Capability overrides only when requested and supported. Local tiers are not billing claims. |
| Mode priority | Explicit Metaswarm/Kiloagent precede Tournament/Classic; incidental "full" or "go deep" cannot authorize mass spawning. Named lineups no longer erase an explicit mode choice. |
| Brackets / seeding | One ceil(N/4) formula; N=12 corrected to three heats of four. Documented rows are executed against the formula. Capacity-constrained serpentine draft retains each model once. |
| Phase 2 / rubric | Freeze five categories before launch. No post-submission reweighting. Per-category medians sum to /50, with penalties applied once. |
| Phase 3 / deployment | Bounded parallel batches, event-driven completion, isolated worktrees from a common baseline, read-only review contestants. No model-ID-derived branch names. |
| Evolution / CB | Preserve the exact Evolution Brief, use median evidence rather than the most flattering judge, scope queries by run/round/heat; sealed material never goes to contestants. |
| Recovery / stalls | Silence is not a failed agent. Two attempts total, confirmed writer termination before retry/takeover. No polling, fabricated heartbeat or silent prompt simplification. |
| Sideline reporting | Dedicated contract for launch, observed results/blockers, every phase boundary and status requests. Requires finished/successful/remaining counts, evidence-backed scores or pending, concrete findings, decision and outstanding work. |
| Phase 4 / gates | Introduced build/test/required-lint failures are hard gates; baseline and optional style findings distinguished. Required unexecuted checks are not green. |
| Anti-gaming | Equal scores may be legitimate. Invalid judges are replaced to retain three. Regression tests are not tampering; weakened checks are. Quoted injection examples are not automatic DQs. |
| Judge separation | Exclude models in the actual judged batch; cross-heat models may judge another heat in fresh contexts. Require three distinct models and two providers after all substitutions. |
| Shadow scope | Small panel for Classic/Tournament; full L1/L2/L3 counts apply only to full Kiloagent. L2 uses three distinct models across providers rather than three Sonnet opinions. No implied 1,000-agent launch for a simple challenge. |
| Shadow criteria / scoring | Generate 6-9 total criteria including decoys. Persist rationale and derivation, give decoys zero aggregation weight, exclude quarantined packets instead of scoring them zero. |
| Divergence / canaries | Normalize before comparing, exclude missing/decoy scores, report unavailable correlations honestly. Never infer absence of gaming from missing shadow data. |
| Phase 5 / results | Exact ties remain ties; optional rematch is a separate declared event, never a retroactive sixth category. Complete public scoreboard before synthesis. |
| Phase 6 / voting | Two votes are pair agreement, not necessarily a majority. Tied splits are conflicts. Preserve provenance and independent evidence; no vote-count-as-probability claim. |
| Phase 6 / application | Explicit merge choice, target drift check, separate integration worktree and required gates. Declined/failed integration leaves target unchanged and is reported as such. Kiloagent synthesis does not bypass approval. |
| Phase 7 / ELO | Frozen starting ratings eliminate pair-order effects. Ties use 0.5; DQs/solo/simulations excluded. Validate legacy data, preserve history, require run receipts and atomic, drift-checked publication. |
| Phase 8 / closing | Replay and Dark Factory are optional; no automatic extra pipeline. Analytics require actual history; aggregate ratings cannot establish category trends. |
| SQL tables | Parse every documented CREATE statement in SQLite; exclude SQLite's own sequence table from counts. Added round/heat, per-run fields and shadow rationale. Inspect additive migrations; incompatible keys need versioned replacement tables preserving originals. |
| Model refresh | Prevalidate every target and defaults before writing; `--check` is read-only. Preserve tracked aliases and exact IDs including provider paths. Malformed docs, unknown defaults and duplicate IDs fail closed. |
| Dry-run / preflight | Offline temporary state and mock legacy ratings by default; real ratings require explicit read-only `--elo-file`. Validate finite ratings, nonnegative integer counts and unique run receipts. No automatic paid probes or real ELO writes; actual check counts, no live-readiness claim. |
| Metaswarm | Reconciled installed-only commander/SS-250 contracts, capsule mapping and launch proof. External launcher must exist; proxy-only policies respected; partial bundles are not full successes. |
| Kiloagent architecture | 1,000 cell roles plus 31 shadow sidecars before retries; no claim that 1,000 roles equals all calls. Sealed L1 contexts separate from contestant packets. |
| Kiloagent files / resilience | Per-cell ownership, atomic artifacts, actual runtime hooks, bounded retry and ceiling-aware takeover. Optional historical architecture path is not a bundled dependency or proof. |
| Compression / scaling | Preserve lossless artifacts by reference; do not fabricate facts to meet a minimum or request private reasoning. No automatic expansion or silent shrinking of explicit scale. |
| Monitoring | Real heartbeat hooks only; notifications are not heartbeats. Quality/correlation reports require observations. |
| Rules / telemetry | Execution boundaries govern the show. Removed silent opt-out tracking; default off, explicit authorization only. |
| Packaging / docs / CI | Tracked internal symlinks remain intact. Raw installation uses the canonical skill URL rather than downloading a symlink target string. CI includes focused regression tests and generated drift detection. |

## Sideline reporting checks

Classic must report build → judging → synthesis. Tournament must report every
heat, public Evolution Brief highlights, finals, judging and synthesis.
Kiloagent reports wave/CB/shadow boundaries. Metaswarm reports actual commander
launch/partial/completion counts and bundle handoffs. All modes report the
applied/unchanged/failed integration outcome before ratings and closing.

The executable report helper rejects duplicate contestants, unknown statuses,
missing status receipts, premature scores and scores without judging evidence.
It distinguishes successful work from finished failed work and retains pending
scores/findings. Mutation tests ensure removing required reporting handoffs
fails structural validation. During active tool work the skill requires
meaningful updates at least every 60 seconds when supported; when only waiting,
it yields for notifications instead of polling or inventing updates.

## Verification scope and limitations

Offline regression tests exercise calculations and malformed/edge cases.
The preflight extracts documented brackets instead of testing a duplicate table.
Mode simulation now actually classifies the sample tasks rather than adding an
unconditional passing count. Custom-provider roster drift is a failure.

This repository is a conversational orchestration playbook, not an implemented
1,000-agent scheduler, transactional rating engine or complete CI runner.
Policies for isolation, migration, launch receipts, approvals, sealing and
rating publication must be executed by the host assistant and available tools.
Offline checks cannot prove live model response, quality, fairness, sealed
context isolation, external launcher compatibility, cost or successful large
deployment. No such outcome is claimed by this review. Single-file installs
must use the embedded policies if repository helper scripts are unavailable.

Generated files are prevalidated together but are not a multi-file filesystem
transaction: an I/O failure must stop the refresh and be reconciled, not reported
as success. Historical replay/example documents are historical, not the current
roster or operational contract.
