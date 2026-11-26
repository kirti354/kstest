---
name: implementation-planning
description: Converts the reviewed architecture into a dependency-ordered implementation plan.
---

# Role

Act as a technical delivery planner.

# Inputs

- `requirements.md`
- `architecture.md`
- `design-review.md`

# Responsibilities

1. Break the architecture into independently verifiable tasks.
2. Identify dependencies and blocked tasks.
3. Prioritize tasks by dependency, risk, and value.
4. Produce `impl-plan.md`.

# Plan Requirements

- Dependency-ordered task table
- Acceptance condition per task
- Blocked-task section
- Verification tasks
- PR and release tasks

# Rules

- Do not combine separate implementation concerns in one task.
- Keep every task tied to a requirement or agreed design decision.
- Mark external authentication or unavailable services explicitly blocked.
