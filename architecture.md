# Automated Documentation Sync Architecture

## Overview

The documentation synchronizer is a local Python command-line tool. It imports
the FastAPI application, reads its registered routes, generates a deterministic
Markdown block, and safely updates the managed section of `src/README.md`.

## Components

### Route Discovery

Reads the `app.routes` collection and extracts public HTTP methods and paths.
Framework infrastructure routes and static mounts are excluded.

### Documentation Renderer

Converts route metadata into a Markdown table. Markdown-special characters in
route values are escaped to prevent malformed output.

### Managed-Section Updater

Replaces content strictly between `<!-- BEGIN GENERATED API DOCS -->` and
`<!-- END GENERATED API DOCS -->`. If markers are not present, it appends the
section; it never rewrites unrelated documentation.

### CLI

The `documentation_sync.py` entry point accepts `--check` for CI/dry-run usage
and returns a non-zero status for drift or invalid input.

## Data Flow

1. Import `src/app.py`.
2. Enumerate registered FastAPI routes.
3. Filter infrastructure routes and sort methods and paths.
4. Render the generated Markdown block.
5. Read `src/README.md`.
6. Replace or append the managed block.
7. Write only in update mode; in check mode, compare and return a status.

## Technology Choices

- **Python 3.12:** available runtime for the existing application and tooling.
- **FastAPI route metadata:** source of truth for API shape.
- **Standard library `argparse` and `pathlib`:** minimal dependencies.
- **Markdown managed markers:** bounded, auditable documentation updates.

## Error Handling

Missing files, unreadable files, invalid markers, and route metadata failures
produce explicit exceptions or CLI errors. The tool does not silently overwrite
content.
