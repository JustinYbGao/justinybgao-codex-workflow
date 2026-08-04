# Grilling protocol

Adapted from the `grilling` skill in [`mattpocock/skills`](https://github.com/mattpocock/skills/tree/main/skills/productivity/grilling), licensed under the MIT License. See the repository's `THIRD_PARTY_NOTICES.md`.

Interview the user rigorously until both sides share the same understanding of the plan, decision, or feature.

The caller must provide an initial question budget. This is a checkpoint, not a total cap. When the checkpoint is reached, summarize the remaining uncertainty and ask whether the user wants to continue; continue only for unresolved decisions that materially affect scope, correctness, security, architecture, or acceptance.

1. Explore the environment first. Look up facts available from files, tools, documentation, or repository history instead of asking the user.
2. Separate facts from decisions. The user owns product and trade-off decisions.
3. Ask one question at a time and wait for the answer before continuing.
4. Include a recommended answer and the reasoning behind it with every question.
5. Resolve prerequisite decisions before dependent decisions.
6. Summarize the resulting requirements, constraints, assumptions, and acceptance criteria.
7. Ask the user to confirm that the shared understanding is complete.

Do not begin implementation until the user explicitly confirms the shared understanding.
