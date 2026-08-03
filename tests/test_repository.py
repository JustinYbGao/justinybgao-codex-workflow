from pathlib import Path
import os
import re
import subprocess
import tempfile
import tomllib
import unittest


ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = ROOT / "skills" / "justinybgao-codex-workflow"


class RepositoryContractTests(unittest.TestCase):
    def read(self, relative_path: str) -> str:
        return (ROOT / relative_path).read_text(encoding="utf-8")

    def load_toml(self, relative_path: str) -> dict:
        with (ROOT / relative_path).open("rb") as handle:
            return tomllib.load(handle)

    def test_skill_has_only_required_frontmatter_fields(self) -> None:
        text = self.read("skills/justinybgao-codex-workflow/SKILL.md")
        match = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
        self.assertIsNotNone(match)
        fields = {
            line.split(":", 1)[0].strip()
            for line in match.group(1).splitlines()
            if ":" in line
        }
        self.assertEqual(fields, {"name", "description"})
        self.assertIn("name: justinybgao-codex-workflow", text)
        self.assertRegex(text, r"description: ['\"]?Use when")

    def test_orchestration_is_sequential_and_fresh(self) -> None:
        text = self.read("skills/justinybgao-codex-workflow/SKILL.md")
        workflow = text.split("## Workflow", 1)[1].split("\n## ", 1)[0]
        grill = workflow.index("Grill")
        worker = workflow.index("Spawn the custom agent `luna_worker`", grill)
        reviewer = workflow.index("Spawn the custom agent `luna_reviewer`", worker)
        self.assertLess(grill, worker)
        self.assertLess(worker, reviewer)
        self.assertIn('fork_turns: "none"', text)
        self.assertIn("Do not pass `model`", text)
        self.assertIn("Do not pass `reasoning_effort`", text)
        self.assertIn("stop before any modification", text)

    def test_skill_requires_independent_review_and_release_authorization(self) -> None:
        text = self.read("skills/justinybgao-codex-workflow/SKILL.md")
        self.assertIn("final implementation result exists", text)
        self.assertIn("three repair rounds", text)
        self.assertIn("explicit release authorization", text)
        for action in ("push", "merge", "deploy", "publish", "tag", "release"):
            self.assertIn(action, text)

    def test_worker_binding(self) -> None:
        agent = self.load_toml("codex/agents/luna_worker.toml")
        self.assertEqual(agent["name"], "luna_worker")
        self.assertEqual(agent["model"], "gpt-5.6-luna")
        self.assertEqual(agent["model_reasoning_effort"], "max")
        self.assertEqual(agent["sandbox_mode"], "workspace-write")
        self.assertIn("all source-code", agent["developer_instructions"])

    def test_reviewer_binding(self) -> None:
        agent = self.load_toml("codex/agents/luna_reviewer.toml")
        self.assertEqual(agent["name"], "luna_reviewer")
        self.assertEqual(agent["model"], "gpt-5.6-luna")
        self.assertEqual(agent["model_reasoning_effort"], "high")
        self.assertEqual(agent["sandbox_mode"], "workspace-write")
        self.assertIn("Never edit source or test code", agent["developer_instructions"])
        self.assertIn("explicit release authorization", agent["developer_instructions"])

    def test_grilling_reference_is_attributed(self) -> None:
        text = self.read("skills/justinybgao-codex-workflow/references/grilling.md")
        self.assertIn("mattpocock/skills", text)
        self.assertIn("MIT", text)
        self.assertIn("one question at a time", text)
        self.assertIn("Do not begin implementation", text)

    def test_ui_metadata_uses_explicit_invocation(self) -> None:
        text = self.read("skills/justinybgao-codex-workflow/agents/openai.yaml")
        self.assertIn('display_name: "Justinybgao Codex Workflow"', text)
        self.assertIn("$justinybgao-codex-workflow", text)
        self.assertIn("allow_implicit_invocation: false", text)

    def test_repository_has_installation_and_license_files(self) -> None:
        for relative_path in (
            "README.md",
            "LICENSE",
            "THIRD_PARTY_NOTICES.md",
            "scripts/install.sh",
            "scripts/validate.sh",
        ):
            self.assertTrue((ROOT / relative_path).is_file(), relative_path)

    def test_installer_is_idempotent_and_refuses_conflicts(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            codex_home = Path(temporary_directory) / "codex-home"
            environment = {**os.environ, "CODEX_HOME": str(codex_home)}
            command = ["sh", str(ROOT / "scripts" / "install.sh")]

            dry_run = subprocess.run(
                [*command, "--dry-run"],
                cwd=ROOT,
                env=environment,
                capture_output=True,
                text=True,
            )
            self.assertEqual(dry_run.returncode, 0, dry_run.stderr)
            self.assertFalse(codex_home.exists())

            first_install = subprocess.run(
                command,
                cwd=ROOT,
                env=environment,
                capture_output=True,
                text=True,
            )
            self.assertEqual(first_install.returncode, 0, first_install.stderr)
            installed_skill = codex_home / "skills" / "justinybgao-codex-workflow"
            self.assertTrue((installed_skill / "SKILL.md").is_file())
            self.assertTrue((codex_home / "agents" / "luna_worker.toml").is_file())
            self.assertTrue((codex_home / "agents" / "luna_reviewer.toml").is_file())
            self.assertFalse((codex_home / "config.toml").exists())
            self.assertFalse((codex_home / "AGENTS.md").exists())

            second_install = subprocess.run(
                command,
                cwd=ROOT,
                env=environment,
                capture_output=True,
                text=True,
            )
            self.assertEqual(second_install.returncode, 0, second_install.stderr)

            worker = codex_home / "agents" / "luna_worker.toml"
            worker.write_text("user-owned conflict\n", encoding="utf-8")
            conflict = subprocess.run(
                command,
                cwd=ROOT,
                env=environment,
                capture_output=True,
                text=True,
            )
            self.assertEqual(conflict.returncode, 2)
            self.assertEqual(worker.read_text(encoding="utf-8"), "user-owned conflict\n")

    def test_installer_rejects_dangling_destination_symlink(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            temporary = Path(temporary_directory)
            codex_home = temporary / "codex-home"
            agents = codex_home / "agents"
            agents.mkdir(parents=True)
            outside_target = temporary / "outside" / "worker.toml"
            (agents / "luna_worker.toml").symlink_to(outside_target)
            environment = {**os.environ, "CODEX_HOME": str(codex_home)}

            result = subprocess.run(
                ["sh", str(ROOT / "scripts" / "install.sh")],
                cwd=ROOT,
                env=environment,
                capture_output=True,
                text=True,
            )

            self.assertEqual(result.returncode, 2)
            self.assertFalse(outside_target.exists())
            self.assertIn("symbolic link", result.stderr)

    def test_installer_rejects_symlinked_destination_directory(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            temporary = Path(temporary_directory)
            codex_home = temporary / "codex-home"
            outside_agents = temporary / "outside-agents"
            outside_agents.mkdir()
            codex_home.mkdir()
            (codex_home / "agents").symlink_to(outside_agents, target_is_directory=True)
            environment = {**os.environ, "CODEX_HOME": str(codex_home)}

            result = subprocess.run(
                ["sh", str(ROOT / "scripts" / "install.sh")],
                cwd=ROOT,
                env=environment,
                capture_output=True,
                text=True,
            )

            self.assertEqual(result.returncode, 2)
            self.assertEqual(list(outside_agents.iterdir()), [])
            self.assertIn("symbolic link", result.stderr)

    def test_validate_requires_official_validator(self) -> None:
        environment = {
            **os.environ,
            "SKILL_VALIDATOR": str(ROOT / "missing-quick-validate.py"),
            "WORKFLOW_SKIP_REPOSITORY_TESTS": "1",
        }
        result = subprocess.run(
            ["sh", str(ROOT / "scripts" / "validate.sh")],
            cwd=ROOT,
            env=environment,
            capture_output=True,
            text=True,
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("official validator", result.stderr.lower())

    def test_behavioral_evidence_is_reproducible(self) -> None:
        text = self.read("tests/behavioral-verification.md")
        self.assertIn("codex-cli 0.146.0-alpha.9.2", text)
        self.assertIn("019fc873-cc27-77e1-85d8-c9c09312c91e", text)
        self.assertIn("--sandbox read-only", text)
        self.assertIn("luna_worker", text)
        self.assertIn("luna_reviewer", text)
        self.assertIn("SHA-256 before", text)
        self.assertIn("SHA-256 after", text)
        self.assertIn('"fork_turns":"none"', text)
        self.assertIn("Neither call contains a `model` or `reasoning_effort` field", text)

    def test_repository_does_not_set_global_subagent_defaults(self) -> None:
        searchable_suffixes = {".md", ".toml", ".yaml", ".sh", ".py"}
        combined = "\n".join(
            path.read_text(encoding="utf-8")
            for path in ROOT.rglob("*")
            if path.is_file()
            and ".git" not in path.parts
            and path.suffix in searchable_suffixes
            and path != Path(__file__)
        )
        self.assertNotIn("default_subagent_model", combined)


if __name__ == "__main__":
    unittest.main()
