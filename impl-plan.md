# Implementation Plan

## Dependency-Ordered Tasks

| Priority | Task | Dependency | Status |
| --- | --- | --- | --- |
| 1 | Document source requirements and acceptance criteria | None | Complete |
| 2 | Define architecture and review decisions | Requirements | Complete |
| 3 | Implement Markdown escaping and deterministic route rendering | Architecture | Complete |
| 4 | Implement managed README section replacement | Task 3 | Complete |
| 5 | Implement missing-file and marker error handling | Task 4 | Complete |
| 6 | Implement `--check` CLI behavior | Tasks 3-5 | Complete |
| 7 | Add focused unit tests | Tasks 3-6 | Complete |
| 8 | Run unit and integration verification | Tasks 3-7 | Complete |
| 9 | Generate PR description and changelog | Verification | Complete |
| 10 | Add Copilot instructions, prompt, skill, pre-commit hook, and CI workflow | Tasks 1-9 | Complete |
| 11 | Create branch, commit, push, and open pull request | Task 10 | In progress |

## Blocked Tasks

- PR creation depends on repository write permission and remote authentication.
