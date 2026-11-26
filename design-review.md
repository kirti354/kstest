# Design Review

## Review Method

The architecture was reviewed for correctness, security, testability,
maintainability, and CI behavior before implementation.

## Findings

| ID | Area | Finding | Decision |
| --- | --- | --- | --- |
| DR-1 | Security | Route metadata may contain Markdown control characters. | Escape pipe characters and line breaks before rendering. |
| DR-2 | Data safety | An update must not overwrite hand-authored content. | Use explicit begin/end markers and validate marker pairing. |
| DR-3 | Correctness | FastAPI includes framework and static routes. | Exclude `/docs`, `/openapi.json`, `/redoc`, `/static`, and `HEAD` only where framework-generated. |
| DR-4 | Determinism | Route iteration order may change. | Sort routes by path, then method. |
| DR-5 | CI usability | CI needs to detect drift without edits. | Add `--check` mode with non-zero exit status on drift. |
| DR-6 | Failure handling | Missing files could be accidentally created. | Treat missing or unreadable input as an error; never create the README. |
| DR-7 | Testability | FastAPI may not be available in every test environment. | Test rendering and update behavior against route-like objects. |
| DR-8 | Scope | External Jira/Confluence integrations are not authorized in this repository. | Keep synchronization local and deterministic; mark integrations out of scope. |

## Agreed Design Decisions

- The README is the synchronization target.
- The generated block is the only file region that may change.
- Route data is discovered from runtime route metadata, not duplicated manually.
- Standard-library implementation avoids dependency or supply-chain changes.
- Missing markers append a new managed block instead of failing.
- One marker marker may be appended or replaced, but mismatched markers will be
  treated as invalid input.
