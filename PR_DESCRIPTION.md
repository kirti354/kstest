# Summary

This change adds a dependency-light automated documentation synchronizer for
the Mergington High School Activities API. It derives the public endpoint table
from FastAPI route metadata and keeps only a marked README section synchronized,
so API changes are reflected consistently without overwriting authored content.

# Changes Made

- Added `requirements.md` with functional, non-functional, and acceptance criteria.
- Added `architecture.md` and `design-review.md` for the approved implementation design.
- Added `impl-plan.md` with dependency-ordered delivery tasks.
- Added `src/documentation_sync.py` for route discovery, Markdown rendering,
  README synchronization, and CI check mode.
- Added `tests/test_documentation_sync.py` for happy paths and edge cases.
- Added `CHANGELOG.md` and this PR description.
- Added Copilot instructions, prompt, skill, a pre-commit documentation hook,
  and GitHub Actions CI verification.
- Added `code-review.md` documenting the structured peer-review findings.

# Test Evidence

Targeted verification:

```text
11 passed, 1 deprecation warning in 0.50s
```

Documentation verification:

```text
Documentation is already synchronized.
```

# Known Limitations

- Jira and Confluence integrations are out of scope; synchronization is local.
- Static mounts and framework documentation routes are excluded by path convention.
- Existing README content outside the managed markers is preserved unchanged.

# Reviewer Checklist

- [ ] Requirements and acceptance criteria are complete.
- [ ] Architecture matches the implemented synchronization behavior.
- [ ] No secrets or credentials are emitted or persisted.
- [ ] Missing files and marker errors fail clearly.
- [ ] Unit tests cover happy path and missing-field/not-found cases.
- [ ] Documentation check mode produces a non-zero status on drift.
- [ ] Dependencies introduce no known vulnerable or unnecessary packages.
- [ ] Generated Markdown is deterministic and safe.
