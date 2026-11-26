# Automated Documentation Sync Requirements

## Source User Story

As a maintainer of the Mergington High School Activities API, I want API
documentation to stay synchronized with the implemented FastAPI routes so that
contributors and reviewers always receive accurate endpoint information.

## Functional Requirements

1. The synchronizer SHALL discover all public HTTP routes exposed by the FastAPI
   application.
2. The synchronizer SHALL generate a Markdown API table containing the HTTP
   method, route path, and route summary.
3. The synchronizer SHALL replace content between the generated-documentation
   markers in `src/README.md`.
4. If the markers are absent, the synchronizer SHALL append a generated
   documentation section.
5. The synchronizer SHALL support a dry-run/check mode that reports whether
   documentation is out of date without modifying the file.
6. Missing or unreadable documentation files SHALL produce a clear error.
7. The synchronizer SHALL ignore framework infrastructure routes such as static
   mounts and OpenAPI documentation routes.
8. Route names, paths, and summaries SHALL be rendered with Markdown-safe text.

## Non-Functional Requirements

1. The implementation SHALL use Python standard-library-only dependencies.
2. Synchronization SHALL be deterministic and preserve text outside the managed
   section.
3. Unit tests SHALL cover generated output, marker replacement, missing markers,
   dry-run mode, missing files, and Markdown escaping.
4. The command SHALL exit with status `0` when successful and a non-zero status
   for missing inputs or documentation drift in check mode.
5. Secrets, credentials, and environment values SHALL not be read or printed.
6. The implementation SHALL run on supported local and CI Python environments
   with no network access.

## Acceptance Criteria

- Running `python src/documentation_sync.py --check` succeeds when the
  documentation matches the application routes.
- Running the same command without `--check` updates `src/README.md`.
- A missing `src/README.md` returns an explicit error and does not create it.
- Route changes add, remove, or update the generated API table deterministically.
