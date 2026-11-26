# Automated Documentation Sync

Implement or review the automated API documentation synchronizer.

Use these sources in order:

1. `requirements.md`
2. `architecture.md`
3. `design-review.md`
4. `impl-plan.md`

Requirements:

- Discover public FastAPI routes.
- Exclude framework infrastructure routes.
- Render deterministic Markdown.
- Replace only content between the generated markers.
- Support `--check` without writing files.
- Handle missing files and mismatched markers clearly.
- Add focused tests for normal and edge cases.

Before replying, run the complete test suite and
`python src/documentation_sync.py --check`. Report exact pass/fail output.
