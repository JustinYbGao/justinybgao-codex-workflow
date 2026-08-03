# justinybgao-codex-workflow

An opt-in Codex workflow that keeps the primary agent on the desktop-selected model and reasoning effort while separating architecture, implementation, independent review, and release authorization.

## Roles

- Primary agent: business analysis, architecture, orchestration, and final acceptance.
- `luna_worker`: all project-file changes with `gpt-5.6-luna`, `max`, and `workspace-write`.
- `luna_reviewer`: independent review, testing, and explicitly authorized release actions with `gpt-5.6-luna`, `high`, and `workspace-write`.

Both subagents must start with fresh context. Their model and reasoning settings come from their custom-agent TOML files, not spawn-time arguments.

## Install

```sh
scripts/install.sh --dry-run
scripts/install.sh
```

The installer adds only:

```text
~/.codex/skills/justinybgao-codex-workflow/
~/.codex/agents/luna_worker.toml
~/.codex/agents/luna_reviewer.toml
```

It does not edit `~/.codex/config.toml`, `~/.codex/AGENTS.md`, the primary model, or global subagent defaults. Existing different files cause a conflict exit instead of being overwritten. Start a new Codex task after installation.

## Use

Invoke the skill explicitly:

```text
$justinybgao-codex-workflow implement this feature
```

The primary agent first runs a one-question-at-a-time Grill session. After requirements are confirmed, it delegates implementation to `luna_worker`, then delegates review to `luna_reviewer`. Code repairs return to the worker. Release remains a separate user-authorized phase.

If the active Codex runtime cannot select custom agents or create fresh-context children, the workflow stops before modification instead of silently using another model or inherited history.

## Validate

```sh
python3 -m pip install -r requirements-validation.txt
SKILL_VALIDATOR="$HOME/.codex/skills/.system/skill-creator/scripts/quick_validate.py" scripts/validate.sh
```

Validation fails if Codex's official validator or its pinned PyYAML dependency is unavailable; it never reports success after skipping that check.

The repository includes the result of a fresh-session, read-only, sequential custom-agent verification in [tests/behavioral-verification.md](tests/behavioral-verification.md).

## License

This repository is MIT licensed. The adapted Grill protocol retains its upstream notice in [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).
