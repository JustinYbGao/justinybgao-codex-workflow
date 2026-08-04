---
name: justinybgao-codex-workflow
description: "Use when starting a new Codex coding task or when the user asks for architecture-led planning, implementation, review, refactoring, migration, or release preparation."
---

# Justinybgao Codex Workflow

## Overview

Keep the primary agent on the model and reasoning effort selected in the desktop composer. It owns user-facing decisions, architecture, orchestration, and final acceptance. Use `luna_ba` only when the task needs business-analysis preparation, and use `luna_searcher` only when the task needs external facts. Delegate every project-file modification to `luna_worker`, then require an independent `luna_reviewer` pass before completion or release.

For the intended setup, select Sol medium (`gpt-5.6-sol` with `medium` reasoning) in the desktop composer before starting the task. The primary agent does not override or switch that model within a task. The optional BA and search agents are separate fresh-context children whose lower-cost Luna settings keep routine fact-finding out of the primary Sol context. Explicit custom-agent spawn is authoritative; do not rely on a global `AGENTS.md` default or global subagent defaults for routing.

## Activation handshake (mandatory)

When this skill is actually loaded for a task, the first assistant message must begin with this exact marker:

`[Justinybgao Workflow · ACTIVE]`

Immediately below it, report:

- Skill: `justinybgao-codex-workflow`;
- Primary model: the model and reasoning effort selected in the desktop composer, or `desktop-selected / not exposed` when the runtime does not expose them;
- Coding/review route: `luna_worker` and `luna_reviewer`, both fixed at `gpt-5.6-luna / max`;
- Phase: `inspection`.

Only print `ACTIVE` after this skill has actually been loaded. Do not claim activation because the skill is installed, listed, mentioned, or merely eligible for implicit invocation. If the user explicitly requests this workflow but it is unavailable, state `[Justinybgao Workflow · NOT ACTIVE]` and stop before modification. At meaningful phase changes, use a concise marker such as `[Justinybgao Workflow · PHASE: worker]`; do not repeat status on every turn. The final response must include `[Justinybgao Workflow · COMPLETE]` or `[Justinybgao Workflow · BLOCKED]`.

## Compatibility gate

Before any modification, confirm that the spawn tool can:

- select any needed custom agents from `luna_ba`, `luna_searcher`, `luna_worker`, and `luna_reviewer`;
- create a child with `fork_turns: "none"` or the runtime's equivalent fresh-context option; and
- omit spawn-time model and reasoning overrides.

If custom-agent selection or fresh-context spawning is unavailable, stop before any modification and report the missing capability. Never substitute a built-in agent or inherit the primary conversation.

## Workflow

1. Inspect the repository and applicable `AGENTS.md` files without changing project files.
2. Decide whether the task needs current, external, or unfamiliar facts. If it does, spawn the custom agent `luna_searcher` with a self-contained research packet and `fork_turns: "none"`; do not pass `model` or `reasoning_effort`; wait for its source-backed result. Skip it when no external facts are needed.
3. Decide whether the requirements are complete enough to implement. If they are not, spawn the custom agent `luna_ba` with the request, repository facts, and any research result, using `fork_turns: "none"`; do not pass `model` or `reasoning_effort`; wait for its requirements packet. Skip it when the requirements are already complete. `luna_ba` may propose questions but the primary agent remains the user-facing decision owner.
4. Read [references/grilling.md](references/grilling.md) completely and run only the remaining decision loop. Skip Grill when the requirements are already complete. Otherwise use an initial budget of five questions for ordinary tasks and an initial budget of eight questions for high-risk architecture or migration tasks. This is a checkpoint, not a total cap: summarize unresolved decisions at the checkpoint and ask whether to continue only when an unresolved item affects scope, correctness, security, architecture, or acceptance. Do not begin implementation until the user explicitly confirms shared understanding.
5. Use the optional Superpowers-style design/planning gate only for novel product or UX work, multi-option architecture, or multi-stage implementation. Reuse the BA and Grill results; do not run a second requirements interview. Produce two or three approaches, trade-offs, a recommendation, and the user-approved decision. Skip it for routine tasks. This gate must not modify project files or create a separate user-facing task.
6. Produce an implementation packet containing exactly:
   - objective and user-visible outcome;
   - approved decisions and assumptions;
   - in-scope and out-of-scope files or components;
   - constraints and forbidden changes;
   - acceptance criteria; and
   - verification commands or expected evidence.
7. Spawn the custom agent `luna_worker` with that packet and `fork_turns: "none"`. Do not pass `model`. Do not pass `reasoning_effort`. Wait for its final result.
8. Inspect the resulting repository state and diff without editing it. Review `git diff --stat` and the relevant `git diff`, make the diff available to the user when the runtime supports it, and stop if no implementation result exists.
9. Only after the final implementation result exists, create a review packet containing the approved implementation packet, design decision if used, changed-file list, diff scope, and worker verification evidence.
10. Spawn the custom agent `luna_reviewer` with the review packet and `fork_turns: "none"`. Do not pass `model`. Do not pass `reasoning_effort`.
11. If review fails, send all actionable findings back to the existing `luna_worker`, then request a fresh `luna_reviewer` pass. Stop and ask the user after three repair rounds.
12. When review passes, perform final business and architecture acceptance against the approved packet. Report changed files, diff summary, tests, review verdict, residual risks, and unverified surfaces.
13. Treat release as a separate phase requiring explicit release authorization in the current conversation. Without it, provide proposed release steps only.

The primary agent, `luna_ba`, and `luna_searcher` must not edit source, tests, configuration, documentation, or generated project files while this workflow is active. `luna_reviewer` must not repair code; all repairs return to `luna_worker`.

## Release gate

Authorization to implement is not authorization to release. Before any `push`, `merge`, `deploy`, `publish`, `tag`, or release creation, state the exact target and action and obtain explicit user approval. After approval, delegate only those authorized release actions to `luna_reviewer` and report exact evidence.

## Quick reference

| Phase | Owner | May modify project files? |
|---|---|---|
| Optional web research | `luna_searcher` | No |
| Optional BA preparation | `luna_ba` | No |
| Optional Superpowers design/planning | Primary | No |
| Requirements and architecture | Primary | No |
| Implementation and repairs | `luna_worker` | Yes |
| Review and tests | `luna_reviewer` | No source/test edits |
| Final acceptance | Primary | No |
| Authorized release | `luna_reviewer` | Only the approved release action |

## Common mistakes

- Starting both subagents together: review requires a completed implementation result.
- Starting optional BA or search agents when their inputs are not needed: keep both routes conditional to control token use.
- Running the design/planning gate for routine work: use it only when alternatives or a multi-stage plan materially reduce risk.
- Running a second requirements interview after BA: reuse the BA packet and ask only user-owned decisions in Grill.
- Passing a model during spawn: the custom-agent TOML owns model selection.
- Sending parent history: send only the self-contained packet.
- Downgrading coding or review agents: `luna_worker` and `luna_reviewer` are always fixed at Luna max.
- Letting the reviewer fix findings: return every code change to `luna_worker`.
- Treating passing tests as release approval: always use the separate release gate.
