# Copilot Instructions for Automated Documentation Sync

## Delivery Rules

- Follow `requirements.md`, `architecture.md`, `design-review.md`, and
  `impl-plan.md`.
- Keep `src/documentation_sync.py` dependency-light and Python standard-library
  based.
- Never print or persist secrets, credentials, environment values, or access
  tokens.
- Preserve README content outside the generated begin/end markers.
- Add or update tests for every behavior change.
- In documentation check mode, detect drift without modifying files.
- Keep route discovery deterministic: sort by path and HTTP method.

## Verification

Run before completion:

```text
python -m pytest -q
python src/documentation_sync.py --check
```

The implementation is complete only if every test passes and documentation check
mode reports no drift.
