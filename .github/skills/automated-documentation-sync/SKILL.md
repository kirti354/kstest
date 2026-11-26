# Automated Documentation Sync

Use this skill when implementing or verifying the FastAPI README synchronizer.

## Workflow

1. Read the requirements and architecture documents.
2. Inspect `src/app.py` for route metadata.
3. Use `src/documentation_sync.py` as the synchronization entry point.
4. Preserve all README content outside the managed markers.
5. Render routes deterministically and escape Markdown table characters.
6. Implement `--check` as a read-only drift detector.
7. Run tests and documentation verification.

## Completion Check

- Public routes are represented.
- Infrastructure routes are excluded.
- Missing README files fail clearly.
- Duplicate or mismatched markers fail safely.
- Unit and integration tests pass.
