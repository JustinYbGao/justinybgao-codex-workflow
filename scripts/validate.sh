#!/bin/sh
set -eu

script_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
repo_root=$(CDPATH= cd -- "$script_dir/.." && pwd)
skill_dir="$repo_root/skills/justinybgao-codex-workflow"

cd "$repo_root"
if [ "${WORKFLOW_SKIP_REPOSITORY_TESTS:-0}" != "1" ]; then
    python3 -m unittest -v tests/test_repository.py
fi

default_validator=${CODEX_HOME:-"${HOME}/.codex"}/skills/.system/skill-creator/scripts/quick_validate.py
validator=${SKILL_VALIDATOR:-$default_validator}

if [ ! -f "$validator" ]; then
    echo "Official validator not found: $validator" >&2
    exit 3
fi

if ! python3 -c 'import yaml' >/dev/null 2>&1; then
    echo "Official validator requires PyYAML. Install requirements-validation.txt in an isolated environment." >&2
    exit 3
fi

python3 "$validator" "$skill_dir"
