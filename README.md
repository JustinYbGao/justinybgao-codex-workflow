# Justinybgao Codex Workflow

An opt-in Codex workflow for architecture-led coding. The primary agent stays focused on reasoning and user decisions, while isolated Luna agents handle business-analysis preparation, web research, implementation, and review.

The workflow is designed around one hard rule:

> The primary agent thinks and decides. `luna_worker` writes code. `luna_reviewer` reviews code. Coding and review always run on Luna max.

## What it does

```text
User
  │
  ▼
Primary agent — Sol medium selected in the desktop composer
  │
  ├─ optional: luna_searcher — external facts and sources
  ├─ optional: luna_ba       — requirements and business-analysis packet
  ├─ Grill                   — user-owned decisions, with checkpoints
  ├─ optional design gate    — only for novel or multi-option work
  │
  ▼
luna_worker — Luna max, workspace-write, all project-file changes
  │
  ▼
Diff inspection
  │
  ▼
luna_reviewer — Luna max, independent review and verification
  │
  ├─ if findings: repair through luna_worker, then review again
  └─ if approved: primary performs final business/architecture acceptance
```

Release is a separate phase. Implementation approval never authorizes a push, merge, deploy, publish, tag, or release.

## Model and responsibility policy

The primary model is selected in the desktop composer before the task starts. For the intended setup, choose `gpt-5.6-sol` with `medium` reasoning. This workflow does not override or switch the primary model.

| Agent | Model | Reasoning | Files | Responsibility |
|---|---|---:|---|---|
| Primary | Desktop-selected, intended Sol | Medium | No project-file edits | User decisions, architecture, orchestration, final acceptance |
| `luna_searcher` | `gpt-5.6-luna` | Medium | Read-only | Optional web research and traceable sources |
| `luna_ba` | `gpt-5.6-luna` | Medium | Read-only | Optional requirements and business-analysis preparation |
| `luna_worker` | `gpt-5.6-luna` | Max | `workspace-write` | All source, test, configuration, documentation, and generated-file changes |
| `luna_reviewer` | `gpt-5.6-luna` | Max | `workspace-write` | Independent review, verification, and explicitly authorized release actions |

`luna_worker` and `luna_reviewer` are intentionally fixed at Luna max. Do not downgrade them for ordinary tasks.

## Prerequisites

You need:

- Codex Desktop or Codex CLI with custom-agent selection and fresh-context child support;
- a trusted local checkout of this repository;
- Python 3 for repository checks;
- PyYAML 6.0.3 for the official skill validator.

The workflow is opt-in. It is not a global default and does not edit your global Codex configuration or `AGENTS.md`.

## Installation

From this repository:

```sh
scripts/install.sh --dry-run
scripts/install.sh
```

The installer adds only these paths:

```text
~/.codex/skills/justinybgao-codex-workflow/
~/.codex/agents/luna_ba.toml
~/.codex/agents/luna_searcher.toml
~/.codex/agents/luna_worker.toml
~/.codex/agents/luna_reviewer.toml
```

It does not modify:

- `~/.codex/config.toml`;
- your primary model selection;
- global subagent defaults;
- `~/.codex/AGENTS.md`.

The installer is conflict-safe: an existing different file, directory, or symbolic link stops installation instead of being overwritten. After installation, start a new Codex task so the skill and custom agents are rediscovered.

## How to use it

Invoke the skill explicitly in a new task:

```text
$justinybgao-codex-workflow implement this feature
```

You can also be specific about the goal:

```text
$justinybgao-codex-workflow

Add CSV export for the completed orders view. Keep the existing API shape, add tests, and do not change authentication or deployment configuration.
```

The primary agent must receive enough context to know the intended outcome. It will inspect the repository before asking questions.

## Execution phases

### 1. Repository inspection

The primary agent reads the repository and applicable instructions without editing project files.

### 2. Optional web research

`luna_searcher` runs only when the task needs current, external, or unfamiliar facts, such as:

- a current third-party API or SDK;
- changing framework or platform documentation;
- an external standard, policy, or compatibility requirement;
- a competitor or product comparison;
- a source-backed technical decision.

It returns URLs, dates, supported facts, disagreements, confidence, and remaining unknowns. It does not modify the repository.

### 3. Optional business analysis

`luna_ba` runs only when the requirements are incomplete, ambiguous, or business-heavy. It returns:

- the business goal;
- user-visible outcomes;
- verified facts;
- assumptions and unresolved decisions;
- scope boundaries;
- acceptance-criteria draft;
- dependencies and risks.

It may propose questions, but the primary agent remains the user-facing decision owner. This avoids paying Sol tokens to repeatedly inspect and structure routine requirements.

### 4. Grill decision loop

Grill is for decisions that only the user can make. It is not a generic request to keep asking questions forever.

- Complete, low-risk requirements: skip Grill or ask only the missing confirmation.
- Ordinary task: start with a five-question checkpoint.
- High-risk architecture or migration: start with an eight-question checkpoint.
- At the checkpoint, summarize what is still unknown.
- Continue only if the remaining uncertainty affects scope, correctness, security, architecture, or acceptance.
- Ask one question at a time and include a recommended answer with its reasoning.

The goal is requirement coverage, not a fixed number of questions.

### 5. Optional Superpowers-style design/planning gate

Use this gate only for:

- a novel product or UX flow;
- an architecture with multiple reasonable designs;
- a multi-stage or multi-team implementation;
- a decision where explicit trade-offs prevent likely rework.

Reuse the BA and Grill results. Do not start a second requirements interview. The gate produces two or three approaches, trade-offs, a recommendation, and the user-approved decision. Routine CRUD, small fixes, clear configuration changes, and straightforward refactors skip it.

This is a lightweight process gate, not another permanent agent and not another coding model.

### 6. Implementation packet

Before coding, the primary agent creates a self-contained packet with:

- objective and user-visible outcome;
- approved decisions and assumptions;
- in-scope and out-of-scope files or components;
- constraints and forbidden changes;
- acceptance criteria;
- verification commands or expected evidence.

The packet may include relevant BA findings, research sources, and the approved design decision. It must not include the entire parent conversation or unnecessary raw search output.

### 7. Implementation

The primary agent selects the custom agent `luna_worker` with a fresh context. The spawn request must:

- select `luna_worker` explicitly;
- use the runtime's fresh-context option, currently `fork_turns: "none"`;
- omit spawn-time `model`;
- omit spawn-time `reasoning_effort`.

The worker uses the model and reasoning settings from `~/.codex/agents/luna_worker.toml`. It owns all project-file changes and must run the specified verification.

### 8. Diff inspection and review

After the worker finishes, the primary agent inspects the repository state, `git diff --stat`, and the relevant `git diff`. The diff scope is included in the review packet and made available to the user when the runtime supports it.

The primary then selects `luna_reviewer` with a fresh context, without passing a model or reasoning override. The reviewer checks requirements, correctness, regressions, security, test quality, maintainability, and release risk. It never repairs source or test code.

If review fails, actionable findings return to the existing `luna_worker`; the result is reviewed again from a fresh review packet. The workflow stops for user direction after three repair rounds.

### 9. Final acceptance and release

After review passes, the primary agent performs final business and architecture acceptance and reports:

- changed files;
- diff summary;
- tests and checks;
- review verdict;
- residual risks;
- unverified surfaces.

Before any release action, the primary agent states the exact target and action and obtains explicit authorization in the current conversation. Only then may `luna_reviewer` perform that exact release action.

## Fresh context and model isolation

Every custom agent must start with a fresh context. The workflow sends a self-contained packet instead of inheriting the parent conversation. This prevents:

- accidental parent-history leakage;
- hidden model inheritance;
- worker/reviewer agreeing because they saw the same unfinished reasoning;
- accidental use of a built-in agent when the required custom agent is unavailable.

If the runtime cannot select the required custom agent or create a fresh-context child, the workflow stops before modification.

## Validation

Run the repository contract tests:

```sh
python3 -m unittest -v tests/test_repository.py
```

Run the full validation after installing the pinned validation dependency in an isolated environment:

```sh
python3 -m pip install -r requirements-validation.txt
SKILL_VALIDATOR="$HOME/.codex/skills/.system/skill-creator/scripts/quick_validate.py" scripts/validate.sh
```

Validation includes:

- repository contract tests;
- TOML and installer behavior checks;
- official Codex skill validation;
- conflict and symbolic-link safety checks.

The repository contains a historical read-only behavioral verification in [tests/behavioral-verification.md](tests/behavioral-verification.md). That record verifies fresh-context worker/reviewer sequencing, but it predates the optional BA/search routes, the reviewer max update, and the design/planning gate; treat it as historical evidence rather than a current full-route run.

## Troubleshooting

### The skill does not appear

Run `scripts/install.sh`, then start a new Codex task. Skills and custom agents are discovered when the task starts.

### A custom agent cannot be selected

The active runtime may not support custom agents or fresh-context children. The workflow stops rather than silently using another model. Start a supported Codex task/runtime and retry.

### Installation reports a conflict

The destination already contains a different file, directory, or symbolic link. Inspect it manually and decide whether it is user-owned. The installer never overwrites it automatically.

### Official validation reports missing PyYAML

Install the pinned dependency from `requirements-validation.txt` in an isolated environment, then rerun `scripts/validate.sh`.

### The primary agent uses the wrong model

Before starting a new task, select Sol medium in the desktop composer. The workflow does not change the primary model after the task begins.

## Repository layout

```text
codex/agents/                         Custom-agent TOML files
skills/justinybgao-codex-workflow/    Installed skill and workflow rules
scripts/install.sh                    Conflict-safe installer
scripts/validate.sh                   Repository and official skill validation
tests/test_repository.py              Contract tests
tests/behavioral-verification.md      Historical runtime verification
```

## License

This repository is MIT licensed. The adapted Grill protocol retains its upstream notice in [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).
