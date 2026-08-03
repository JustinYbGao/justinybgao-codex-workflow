---
name: justinybgao-codex-workflow
description: "Use when the user explicitly requests the Justinybgao architecture-led coding workflow for a feature, bug fix, refactor, migration, or release preparation."
---

# Justinybgao Codex Workflow

## Overview

Keep the primary agent responsible for business analysis, architecture, orchestration, and final acceptance. Delegate every project-file modification to `luna_worker`, then require an independent `luna_reviewer` pass before completion or release.

The primary agent keeps the model and reasoning effort selected in the desktop composer. Do not change or restate those settings.

## Compatibility gate

Before any modification, confirm that the spawn tool can:

- select the custom agents `luna_worker` and `luna_reviewer`;
- create a child with `fork_turns: "none"` or the runtime's equivalent fresh-context option; and
- omit spawn-time model and reasoning overrides.

If custom-agent selection or fresh-context spawning is unavailable, stop before any modification and report the missing capability. Never substitute a built-in agent or inherit the primary conversation.

## Workflow

1. Inspect the repository and applicable `AGENTS.md` files without changing project files.
2. Read [references/grilling.md](references/grilling.md) completely and run its Grill decision loop. Do not begin implementation until the user explicitly confirms shared understanding.
3. Produce an implementation packet containing exactly:
   - objective and user-visible outcome;
   - approved decisions and assumptions;
   - in-scope and out-of-scope files or components;
   - constraints and forbidden changes;
   - acceptance criteria; and
   - verification commands or expected evidence.
4. Spawn the custom agent `luna_worker` with that packet and `fork_turns: "none"`. Do not pass `model`. Do not pass `reasoning_effort`. Wait for its final result.
5. Inspect the resulting repository state and diff without editing it. If no implementation result exists, stop.
6. Only after the final implementation result exists, create a review packet containing the approved implementation packet, changed-file list, diff scope, and worker verification evidence.
7. Spawn the custom agent `luna_reviewer` with the review packet and `fork_turns: "none"`. Do not pass `model`. Do not pass `reasoning_effort`.
8. If review fails, send all actionable findings back to the existing `luna_worker`, then request a fresh `luna_reviewer` pass. Stop and ask the user after three repair rounds.
9. When review passes, perform final business and architecture acceptance against the approved packet. Report changed files, tests, review verdict, residual risks, and unverified surfaces.
10. Treat release as a separate phase requiring explicit release authorization in the current conversation. Without it, provide proposed release steps only.

The primary agent must not edit source, tests, configuration, documentation, or generated project files while this workflow is active. `luna_reviewer` must not repair code; all repairs return to `luna_worker`.

## Release gate

Authorization to implement is not authorization to release. Before any `push`, `merge`, `deploy`, `publish`, `tag`, or release creation, state the exact target and action and obtain explicit user approval. After approval, delegate only those authorized release actions to `luna_reviewer` and report exact evidence.

## Quick reference

| Phase | Owner | May modify project files? |
|---|---|---|
| Requirements and architecture | Primary | No |
| Implementation and repairs | `luna_worker` | Yes |
| Review and tests | `luna_reviewer` | No source/test edits |
| Final acceptance | Primary | No |
| Authorized release | `luna_reviewer` | Only the approved release action |

## Common mistakes

- Starting both subagents together: review requires a completed implementation result.
- Passing a model during spawn: the custom-agent TOML owns model selection.
- Sending parent history: send only the self-contained packet.
- Letting the reviewer fix findings: return every code change to `luna_worker`.
- Treating passing tests as release approval: always use the separate release gate.
