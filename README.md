# Justinybgao Codex Workflow / Justinybgao Codex 工作流

A Codex workflow for architecture-led coding. New coding tasks are eligible for implicit invocation, while the explicit starter prompt remains the reliable way to request it. The primary agent stays focused on reasoning and user decisions, while isolated Luna agents handle business-analysis preparation, web research, implementation, and review.

这是一个以架构设计为导向的 Codex 编码工作流。新的编码任务可以被隐式调用，但显式启动提示仍然是请求该工作流的可靠方式。主代理专注于推理和用户决策，隔离运行的 Luna 代理负责业务分析准备、网络研究、实现和评审。

The workflow is designed around one hard rule:

该工作流围绕一条严格规则设计：

> The primary agent thinks and decides. `luna_worker` writes code. `luna_reviewer` reviews code. Coding and review always run on Luna max.
>
> 主代理负责思考与决策；`luna_worker` 负责编写代码；`luna_reviewer` 负责评审代码。编码和评审始终使用 Luna max。

## What it does / 功能概览

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

中文流程对应为：用户 → 主代理（在桌面编辑器中选择 Sol medium）→ 可选的 `luna_searcher`、`luna_ba`、Grill 和设计门禁 → `luna_worker` 执行项目文件变更 → 检查差异 → `luna_reviewer` 独立评审；如果发现问题，就通过 `luna_worker` 修复后再次评审，获批后由主代理完成业务和架构验收。

Release is a separate phase. Implementation approval never authorizes a push, merge, deploy, publish, tag, or release.

发布是独立阶段。批准实现并不等于授权 push、merge、deploy、publish、tag 或创建 release。

## Model and responsibility policy / 模型与职责策略

The primary model is selected in the desktop composer before the task starts. For the intended setup, choose `gpt-5.6-sol` with `medium` reasoning. This workflow does not override or switch the primary model.

主模型应在任务开始前于桌面编辑器中选择。按预期配置，请选择带有 `medium` 推理强度的 `gpt-5.6-sol`。本工作流不会覆盖或切换主模型。

| Agent / 代理 | Model / 模型 | Reasoning / 推理 | Files / 文件 | Responsibility / 职责 |
|---|---|---:|---|---|
| Primary | Desktop-selected, intended Sol | Medium | No project-file edits / 不修改项目文件 | User decisions, architecture, orchestration, final acceptance<br>用户决策、架构设计、流程编排与最终验收 |
| `luna_searcher` | `gpt-5.6-luna` | Medium | Read-only / 只读 | Optional web research and traceable sources<br>可选的网络研究与可追溯来源 |
| `luna_ba` | `gpt-5.6-luna` | Medium | Read-only / 只读 | Optional requirements and business-analysis preparation<br>可选的需求梳理与业务分析准备 |
| `luna_worker` | `gpt-5.6-luna` | Max | `workspace-write` | All source, test, configuration, documentation, and generated-file changes<br>所有源代码、测试、配置、文档和生成文件的变更 |
| `luna_reviewer` | `gpt-5.6-luna` | Max | `workspace-write` | Independent review, verification, and explicitly authorized release actions<br>独立评审、验证，以及获得明确授权后的发布操作 |

`luna_worker` and `luna_reviewer` are intentionally fixed at Luna max. Do not downgrade them for ordinary tasks.

`luna_worker` 和 `luna_reviewer` 特意固定使用 Luna max。对于普通任务，不要降低它们的配置。

## Activation and visibility / 激活与可见性

The skill metadata allows Codex to consider this workflow for a new coding task. That is eligibility, not proof that the skill was loaded. When it is actually active, the first assistant message must begin with:

技能元数据允许 Codex 在新的编码任务中考虑使用该工作流，但这只表示具备调用资格，并不证明技能已经加载。技能真正激活时，助手的第一条消息必须以以下内容开头：

```text
[Justinybgao Workflow · ACTIVE]
Skill: justinybgao-codex-workflow
Primary model: desktop-selected / not exposed
Coding/review route: luna_worker + luna_reviewer — gpt-5.6-luna / max
Phase: inspection
```

The workflow uses concise phase markers for meaningful transitions and ends with `COMPLETE` or `BLOCKED`. If the banner is missing, do not assume this workflow is active; start the task with `$justinybgao-codex-workflow`.

工作流会在重要阶段转换时使用简洁的阶段标记，并以 `COMPLETE` 或 `BLOCKED` 结束。如果缺少上述标记，不要假设工作流已经激活；请用 `$justinybgao-codex-workflow` 启动任务。

## Prerequisites / 前置条件

You need:

你需要：

- Codex Desktop or Codex CLI with custom-agent selection and fresh-context child support;
  支持选择自定义代理和创建新上下文子代理的 Codex Desktop 或 Codex CLI；
- a trusted local checkout of this repository;
  本仓库的可信本地检出副本；
- Python 3 for repository checks;
  用于仓库检查的 Python 3；
- PyYAML 6.0.3 for the official skill validator.
  用于官方技能验证器的 PyYAML 6.0.3。

The workflow does not edit your global Codex configuration or `AGENTS.md`. Implicit invocation is enabled in the skill metadata, but a blank conversation with no coding task cannot be forced to load a task-specific skill by the skill file alone.

该工作流不会修改全局 Codex 配置或 `AGENTS.md`。技能元数据已启用隐式调用，但仅凭技能文件本身，无法强制一个没有编码任务的空白对话加载特定任务技能。

## Installation / 安装

From this repository:

在本仓库中运行：

```sh
scripts/install.sh --dry-run
scripts/install.sh
```

The installer adds only these paths:

安装脚本只会添加以下路径：

```text
~/.codex/skills/justinybgao-codex-workflow/
~/.codex/agents/luna_ba.toml
~/.codex/agents/luna_searcher.toml
~/.codex/agents/luna_worker.toml
~/.codex/agents/luna_reviewer.toml
```

It does not modify:

它不会修改：

- `~/.codex/config.toml`;
  `~/.codex/config.toml`；
- your primary model selection;
  你的主模型选择；
- global subagent defaults;
  全局子代理默认配置；
- `~/.codex/AGENTS.md`.
  `~/.codex/AGENTS.md`。

The installer is conflict-safe: an existing different file, directory, or symbolic link stops installation instead of being overwritten. After installation, start a new Codex task so the skill and custom agents are rediscovered.

安装脚本具有冲突安全性：如果目标位置已有不同的文件、目录或符号链接，安装会停止而不会覆盖它。安装完成后，请启动新的 Codex 任务，以便重新发现技能和自定义代理。

## How to use it / 使用方法

For a guaranteed activation, invoke the skill explicitly in the first message of a new task:

如需确保激活，请在新任务的第一条消息中显式调用该技能：

```text
$justinybgao-codex-workflow implement this feature
```

If the first response does not show `[Justinybgao Workflow · ACTIVE]`, the skill was not loaded and the agent must not claim that it was used.

如果第一条回复没有显示 `[Justinybgao Workflow · ACTIVE]`，说明技能没有加载，代理不得声称使用了该技能。

You can also be specific about the goal:

你也可以明确说明目标：

```text
$justinybgao-codex-workflow

Add CSV export for the completed orders view. Keep the existing API shape, add tests, and do not change authentication or deployment configuration.
```

The primary agent must receive enough context to know the intended outcome. It will inspect the repository before asking questions.

主代理必须获得足够的上下文来了解预期结果，并会在提问前检查仓库。

## Execution phases / 执行阶段

### 1. Repository inspection / 仓库检查

The primary agent reads the repository and applicable instructions without editing project files.

主代理读取仓库和适用的指令，但不编辑项目文件。

### 2. Optional web research / 可选的网络研究

`luna_searcher` runs only when the task needs current, external, or unfamiliar facts, such as:

只有在任务需要最新、外部或不熟悉的事实时，才会运行 `luna_searcher`，例如：

- a current third-party API or SDK;
  当前的第三方 API 或 SDK；
- changing framework or platform documentation;
  正在变化的框架或平台文档；
- an external standard, policy, or compatibility requirement;
  外部标准、政策或兼容性要求；
- a competitor or product comparison;
  竞争对手或产品对比；
- a source-backed technical decision.
  需要来源支持的技术决策。

It returns URLs, dates, supported facts, disagreements, confidence, and remaining unknowns. It does not modify the repository.

它会返回 URL、日期、得到来源支持的事实、分歧、可信度以及仍未知的信息，但不会修改仓库。

### 3. Optional business analysis / 可选的业务分析

`luna_ba` runs only when the requirements are incomplete, ambiguous, or business-heavy. It returns:

只有在需求不完整、存在歧义或业务内容较重时，才会运行 `luna_ba`。它会返回：

- the business goal;
  业务目标；
- user-visible outcomes;
  用户可见的结果；
- verified facts;
  已验证的事实；
- assumptions and unresolved decisions;
  假设和未解决的决策；
- scope boundaries;
  范围边界；
- acceptance-criteria draft;
  验收标准草案；
- dependencies and risks.
  依赖和风险。

It may propose questions, but the primary agent remains the user-facing decision owner. This avoids paying Sol tokens to repeatedly inspect and structure routine requirements.

它可以提出问题，但主代理仍然是面向用户的决策负责人。这样可以避免反复让 Sol 检查并整理常规需求，从而节省 Sol 的 token。

### 4. Grill decision loop / Grill 决策循环

Grill is for decisions that only the user can make. It is not a generic request to keep asking questions forever.

Grill 用于处理只有用户才能做出的决策，并不是让代理无限制地持续提问。

- Complete, low-risk requirements: skip Grill or ask only the missing confirmation.
  对于完整且低风险的需求：跳过 Grill，或只询问缺失的确认信息。
- Ordinary task: start with a five-question checkpoint.
  对于普通任务：从五个问题的检查点开始。
- High-risk architecture or migration: start with an eight-question checkpoint.
  对于高风险架构或迁移：从八个问题的检查点开始。
- At the checkpoint, summarize what is still unknown.
  到达检查点时，总结仍然未知的内容。
- Continue only if the remaining uncertainty affects scope, correctness, security, architecture, or acceptance.
  只有当剩余不确定性影响范围、正确性、安全性、架构或验收时，才继续提问。
- Ask one question at a time and include a recommended answer with its reasoning.
  一次只问一个问题，并给出推荐答案及其理由。

The goal is requirement coverage, not a fixed number of questions.

目标是覆盖需求，而不是达到固定的问题数量。

### 5. Optional Superpowers-style design/planning gate / 可选的 Superpowers 风格设计与规划门禁

Use this gate only for:

仅在以下情况下使用此门禁：

- a novel product or UX flow;
  新颖的产品或 UX 流程；
- an architecture with multiple reasonable designs;
  存在多种合理设计方案的架构；
- a multi-stage or multi-team implementation;
  多阶段或多团队实现；
- a decision where explicit trade-offs prevent likely rework.
  通过明确权衡可以避免可能返工的决策。

Reuse the BA and Grill results. Do not start a second requirements interview. The gate produces two or three approaches, trade-offs, a recommendation, and the user-approved decision. Routine CRUD, small fixes, clear configuration changes, and straightforward refactors skip it.

复用 BA 和 Grill 的结果，不要重新进行第二轮需求访谈。该门禁会产出两到三个方案、权衡、推荐方案以及用户批准的决策。常规 CRUD、小型修复、明确的配置变更和直接的重构应跳过此门禁。

This is a lightweight process gate, not another permanent agent and not another coding model.

这是一个轻量级流程门禁，不是另一个常驻代理，也不是另一个编码模型。

### 6. Implementation packet / 实现任务包

Before coding, the primary agent creates a self-contained packet with:

编码前，主代理会创建一个自包含的任务包，其中包括：

- objective and user-visible outcome;
  目标和用户可见的结果；
- approved decisions and assumptions;
  已批准的决策和假设；
- in-scope and out-of-scope files or components;
  范围内和范围外的文件或组件；
- constraints and forbidden changes;
  约束以及禁止的变更；
- acceptance criteria;
  验收标准；
- verification commands or expected evidence.
  验证命令或预期证据。

The packet may include relevant BA findings, research sources, and the approved design decision. It must not include the entire parent conversation or unnecessary raw search output.

任务包可以包含相关的 BA 结论、研究来源和已批准的设计决策，但不得包含完整的父级对话或不必要的原始搜索输出。

### 7. Implementation / 实现

The primary agent selects the custom agent `luna_worker` with a fresh context. The spawn request must:

主代理会使用新上下文选择自定义代理 `luna_worker`。生成子代理的请求必须：

- select `luna_worker` explicitly;
  显式选择 `luna_worker`；
- use the runtime's fresh-context option, currently `fork_turns: "none"`;
  使用运行时的新上下文选项，目前为 `fork_turns: "none"`；
- omit spawn-time `model`;
  不传入生成时的 `model`；
- omit spawn-time `reasoning_effort`.
  不传入生成时的 `reasoning_effort`。

The worker uses the model and reasoning settings from `~/.codex/agents/luna_worker.toml`. It owns all project-file changes and must run the specified verification.

工作代理使用 `~/.codex/agents/luna_worker.toml` 中的模型和推理设置。它负责所有项目文件变更，并且必须运行指定的验证。

### 8. Diff inspection and review / 差异检查与评审

After the worker finishes, the primary agent inspects the repository state, `git diff --stat`, and the relevant `git diff`. The diff scope is included in the review packet and made available to the user when the runtime supports it.

工作代理完成后，主代理会检查仓库状态、`git diff --stat` 和相关的 `git diff`。差异范围会纳入评审任务包，并在运行时支持时提供给用户。

The primary then selects `luna_reviewer` with a fresh context, without passing a model or reasoning override. The reviewer checks requirements, correctness, regressions, security, test quality, maintainability, and release risk. It never repairs source or test code.

随后，主代理会使用新上下文选择 `luna_reviewer`，且不传入模型或推理覆盖项。评审代理会检查需求、正确性、回归、安全性、测试质量、可维护性和发布风险，但绝不会修复源代码或测试代码。

If review fails, actionable findings return to the existing `luna_worker`; the result is reviewed again from a fresh review packet. The workflow stops for user direction after three repair rounds.

如果评审未通过，可执行的发现会返回给现有的 `luna_worker`；修复结果会根据新的评审任务包再次评审。完成三轮修复后，工作流会停止并等待用户指示。

### 9. Final acceptance and release / 最终验收与发布

After review passes, the primary agent performs final business and architecture acceptance and reports:

评审通过后，主代理会完成最终的业务和架构验收，并报告：

- changed files;
  变更的文件；
- diff summary;
  差异摘要；
- tests and checks;
  测试和检查；
- review verdict;
  评审结论；
- residual risks;
  剩余风险；
- unverified surfaces.
  尚未验证的范围。

Before any release action, the primary agent states the exact target and action and obtains explicit authorization in the current conversation. Only then may `luna_reviewer` perform that exact release action.

在进行任何发布操作前，主代理会说明确切的目标和操作，并在当前对话中取得明确授权。只有这样，`luna_reviewer` 才可以执行该项确切的发布操作。

## Fresh context and model isolation / 新上下文与模型隔离

Every custom agent must start with a fresh context. The workflow sends a self-contained packet instead of inheriting the parent conversation. This prevents:

每个自定义代理都必须以新上下文启动。工作流发送自包含的任务包，而不是继承父级对话，从而避免：

- accidental parent-history leakage;
  意外泄露父级对话历史；
- hidden model inheritance;
  隐式继承模型；
- worker/reviewer agreeing because they saw the same unfinished reasoning;
  工作代理和评审代理因看到相同的未完成推理而达成不独立的结论；
- accidental use of a built-in agent when the required custom agent is unavailable.
  所需自定义代理不可用时意外使用内置代理。

If the runtime cannot select the required custom agent or create a fresh-context child, the workflow stops before modification.

如果运行时无法选择所需的自定义代理或创建新上下文子代理，工作流会在修改前停止。

## Validation / 验证

Run the repository contract tests:

运行仓库契约测试：

```sh
python3 -m unittest -v tests/test_repository.py
```

Run the full validation after installing the pinned validation dependency in an isolated environment:

在隔离环境中安装锁定版本的验证依赖后，运行完整验证：

```sh
python3 -m pip install -r requirements-validation.txt
SKILL_VALIDATOR="$HOME/.codex/skills/.system/skill-creator/scripts/quick_validate.py" scripts/validate.sh
```

Validation includes:

验证包括：

- repository contract tests;
  仓库契约测试；
- TOML and installer behavior checks;
  TOML 和安装脚本行为检查；
- official Codex skill validation;
  官方 Codex 技能验证；
- conflict and symbolic-link safety checks.
  冲突和符号链接安全检查。

The repository contains a historical read-only behavioral verification in [tests/behavioral-verification.md](tests/behavioral-verification.md). That record verifies fresh-context worker/reviewer sequencing, but it predates the optional BA/search routes, the reviewer max update, and the design/planning gate; treat it as historical evidence rather than a current full-route run.

仓库中的 [tests/behavioral-verification.md](tests/behavioral-verification.md) 包含一份历史性的只读行为验证记录。该记录验证了新上下文工作代理/评审代理的顺序，但早于可选的 BA/搜索路径、评审代理的 max 更新以及设计/规划门禁；请将其视为历史证据，而不是当前完整路径的运行记录。

## Troubleshooting / 故障排查

### The skill does not appear / 技能未出现

Run `scripts/install.sh`, then start a new Codex task. Skills and custom agents are discovered when the task starts.

运行 `scripts/install.sh`，然后启动新的 Codex 任务。技能和自定义代理会在任务启动时被发现。

### A custom agent cannot be selected / 无法选择自定义代理

The active runtime may not support custom agents or fresh-context children. The workflow stops rather than silently using another model. Start a supported Codex task/runtime and retry.

当前运行时可能不支持自定义代理或新上下文子代理。工作流会停止，而不是默默使用其他模型。请启动支持这些能力的 Codex 任务或运行时后重试。

### Installation reports a conflict / 安装报告冲突

The destination already contains a different file, directory, or symbolic link. Inspect it manually and decide whether it is user-owned. The installer never overwrites it automatically.

目标位置已经包含不同的文件、目录或符号链接。请手动检查并判断它是否属于用户已有内容。安装脚本绝不会自动覆盖它。

### Official validation reports missing PyYAML / 官方验证报告缺少 PyYAML

Install the pinned dependency from `requirements-validation.txt` in an isolated environment, then rerun `scripts/validate.sh`.

请在隔离环境中从 `requirements-validation.txt` 安装锁定版本的依赖，然后重新运行 `scripts/validate.sh`。

### The primary agent uses the wrong model / 主代理使用了错误的模型

Before starting a new task, select Sol medium in the desktop composer. The workflow does not change the primary model after the task begins.

开始新任务前，请在桌面编辑器中选择 Sol medium。任务开始后，工作流不会更改主模型。

## Repository layout / 仓库布局

```text
codex/agents/                         Custom-agent TOML files
skills/justinybgao-codex-workflow/    Installed skill and workflow rules
scripts/install.sh                    Conflict-safe installer
scripts/validate.sh                   Repository and official skill validation
tests/test_repository.py              Contract tests
tests/behavioral-verification.md      Historical runtime verification
```

中文对应：`codex/agents/` 存放自定义代理 TOML 文件，`skills/justinybgao-codex-workflow/` 存放已安装的技能和工作流规则，`scripts/` 存放安装与验证脚本，`tests/` 存放契约测试和历史运行时验证。

## License / 许可证

This repository is MIT licensed. The adapted Grill protocol retains its upstream notice in [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).

本仓库采用 MIT 许可证。改编后的 Grill 协议在 [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md) 中保留了上游声明。
