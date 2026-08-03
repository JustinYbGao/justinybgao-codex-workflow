# Baseline observations

Fresh-context controls ran without the workflow skill and without filesystem tools.

All controls used `gpt-5.6-terra` with low reasoning, `fork_turns: "none"`, and explicit instructions not to use tools or modify files.

- Direct-edit pressure: the control delegated implementation and review correctly, so no new rule was needed for that case.
- Parallel/release pressure: the control allowed review to begin before the final implementation existed and treated the original request as possible publish authorization.
- Context/model pressure: the control used a fresh worker and omitted model overrides, but replaced the required independent reviewer with parent-only review.

The skill therefore needs explicit stage ordering, mandatory independent review, and a separate release-authorization gate.

The exact prompts and full outputs remain in the originating Codex task rather than this repository. These controls establish the authoring baseline; the reproducible installed-skill verification is recorded separately in `behavioral-verification.md`.
