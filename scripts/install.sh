#!/bin/sh
set -eu

script_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
repo_root=$(CDPATH= cd -- "$script_dir/.." && pwd)
codex_home=${CODEX_HOME:-"${HOME}/.codex"}
dry_run=false

if [ "${1:-}" = "--dry-run" ]; then
    dry_run=true
    shift
fi

if [ "$#" -ne 0 ]; then
    echo "usage: scripts/install.sh [--dry-run]" >&2
    exit 64
fi

skill_source="$repo_root/skills/justinybgao-codex-workflow"
skill_target="$codex_home/skills/justinybgao-codex-workflow"
agents_source="$repo_root/codex/agents"
agents_target="$codex_home/agents"
conflict=0

check_directory() {
    target_directory=$1

    if [ -L "$target_directory" ]; then
        echo "CONFLICT symbolic link directory $target_directory" >&2
        conflict=1
    elif [ -e "$target_directory" ] && [ ! -d "$target_directory" ]; then
        echo "CONFLICT non-directory path $target_directory" >&2
        conflict=1
    fi
}

check_file() {
    source_file=$1
    target_file=$2

    if [ -L "$target_file" ]; then
        echo "CONFLICT symbolic link file $target_file" >&2
        conflict=1
    elif [ ! -e "$target_file" ]; then
        echo "ADD $target_file"
    elif [ -f "$target_file" ] && cmp -s "$source_file" "$target_file"; then
        echo "OK  $target_file"
    else
        echo "CONFLICT $target_file" >&2
        conflict=1
    fi
}

check_directory "$codex_home"
check_directory "$codex_home/skills"
check_directory "$skill_target"
check_directory "$skill_target/agents"
check_directory "$skill_target/references"
check_directory "$agents_target"
check_file "$skill_source/SKILL.md" "$skill_target/SKILL.md"
check_file "$skill_source/agents/openai.yaml" "$skill_target/agents/openai.yaml"
check_file "$skill_source/references/grilling.md" "$skill_target/references/grilling.md"
check_file "$agents_source/luna_worker.toml" "$agents_target/luna_worker.toml"
check_file "$agents_source/luna_reviewer.toml" "$agents_target/luna_reviewer.toml"

if [ "$conflict" -ne 0 ]; then
    echo "Installation stopped; existing files were not overwritten." >&2
    exit 2
fi

if [ "$dry_run" = true ]; then
    echo "Dry run complete; no files changed."
    exit 0
fi

mkdir -p "$skill_target/agents" "$skill_target/references" "$agents_target"
cp "$skill_source/SKILL.md" "$skill_target/SKILL.md"
cp "$skill_source/agents/openai.yaml" "$skill_target/agents/openai.yaml"
cp "$skill_source/references/grilling.md" "$skill_target/references/grilling.md"
cp "$agents_source/luna_worker.toml" "$agents_target/luna_worker.toml"
cp "$agents_source/luna_reviewer.toml" "$agents_target/luna_reviewer.toml"

echo "Installed Justinybgao Codex Workflow into $codex_home"
echo "Start a new Codex task so the skill and custom agents are rediscovered."
