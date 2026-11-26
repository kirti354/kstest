"""Synchronize FastAPI route documentation into src/README.md."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from types import SimpleNamespace
from typing import Iterable


BEGIN_MARKER = "<!-- BEGIN GENERATED API DOCS -->"
END_MARKER = "<!-- END GENERATED API DOCS -->"

IGNORED_PATH_PREFIXES = ("/docs", "/redoc", "/openapi", "/static")


class DocumentationSyncError(Exception):
    """Raised when documentation synchronization cannot be completed safely."""


def escape_markdown(value: object) -> str:
    """Escape text that could alter Markdown table structure."""
    return str(value).replace("\\", "\\\\").replace("|", "\\|").replace("\r", " ").replace("\n", " ").strip()


def get_public_routes(app: object) -> list[tuple[str, str, str]]:
    """Extract and sort public route metadata from a FastAPI-like app."""
    routes = getattr(app, "routes", None)
    if routes is None:
        raise DocumentationSyncError("Application route metadata is missing")

    inventory: set[tuple[str, str, str]] = set()
    for route in routes:
        path = getattr(route, "path", "")
        methods = getattr(route, "methods", None)
        if not path or path.startswith(IGNORED_PATH_PREFIXES):
            continue
        if not methods:
            continue

        summary = getattr(route, "summary", None)
        if not summary:
            summary = getattr(route, "name", None) or "API endpoint"

        for method in methods:
            normalized = str(method).upper()
            if normalized in {"HEAD", "OPTIONS"}:
                continue
            inventory.add((normalized, str(path), str(summary)))

    return sorted(inventory, key=lambda route: (route[1], route[0]))


def generate_api_documentation(app: object) -> str:
    """Render public routes as a deterministic Markdown table."""
    lines = [
        "| Method | Path | Summary |",
        "| --- | --- | --- |",
    ]
    for method, path, summary in get_public_routes(app):
        lines.append(
            f"| {escape_markdown(method)} | `{escape_markdown(path)}` | "
            f"{escape_markdown(summary)} |"
        )
    return "\n".join(lines)


def render_managed_section(app: object) -> str:
    """Render the complete marker-delimited documentation block."""
    table = generate_api_documentation(app)
    return f"{BEGIN_MARKER}\n\n{table}\n\n{END_MARKER}"


def update_managed_section(existing: str, generated: str) -> str:
    """Replace or append the generated section while preserving other content."""
    begin_count = existing.count(BEGIN_MARKER)
    end_count = existing.count(END_MARKER)

    if begin_count == 0 and end_count == 0:
        separator = "" if not existing or existing.endswith("\n") else "\n"
        return f"{existing}{separator}\n{generated}\n"

    if begin_count != 1 or end_count != 1:
        raise DocumentationSyncError("README contains mismatched or duplicate generated markers")

    begin = existing.index(BEGIN_MARKER)
    end = existing.index(END_MARKER, begin)
    if end < begin:
        raise DocumentationSyncError("README generated markers are in the wrong order")

    replacement_end = end + len(END_MARKER)
    return existing[:begin] + generated + existing[replacement_end:]


def sync_documentation(app: object, readme_path: Path, check: bool = False) -> bool:
    """Synchronize a README and report whether its managed section changed."""
    if not readme_path.exists():
        raise DocumentationSyncError(f"README file not found: {readme_path}")
    if not readme_path.is_file():
        raise DocumentationSyncError(f"README path is not a file: {readme_path}")

    try:
        existing = readme_path.read_text(encoding="utf-8")
    except OSError as exc:
        raise DocumentationSyncError(f"Unable to read README: {readme_path}") from exc

    generated = render_managed_section(app)
    try:
        updated = update_managed_section(existing, generated)
    except DocumentationSyncError:
        raise

    changed = updated != existing
    if changed and not check:
        try:
            readme_path.write_text(updated, encoding="utf-8")
        except OSError as exc:
            raise DocumentationSyncError(f"Unable to write README: {readme_path}") from exc
    return changed


def load_app():
    """Load the repository FastAPI app."""
    try:
        from app import app
    except ImportError as exc:
        raise DocumentationSyncError(
            "Unable to import src/app.py. Ensure FastAPI dependencies are installed."
        ) from exc
    return app


def parse_args(argv: Iterable[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Synchronize FastAPI route documentation in src/README.md."
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="report documentation drift without modifying the README",
    )
    parser.add_argument(
        "--readme",
        type=Path,
        default=Path(__file__).resolve().parent / "README.md",
        help="README path to synchronize (defaults to src/README.md)",
    )
    return parser.parse_args(argv)


def main(argv: Iterable[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        app = load_app()
        changed = sync_documentation(app, args.readme, check=args.check)
    except DocumentationSyncError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    if changed and args.check:
        print("Documentation is out of date.")
        return 1
    if changed:
        print(f"Updated documentation in {args.readme}")
    else:
        print("Documentation is already synchronized.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
