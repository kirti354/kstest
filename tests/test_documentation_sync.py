from pathlib import Path
from types import SimpleNamespace

import pytest

from src.documentation_sync import (
    BEGIN_MARKER,
    END_MARKER,
    DocumentationSyncError,
    generate_api_documentation,
    sync_documentation,
    update_managed_section,
)


def fake_app():
    return SimpleNamespace(
        routes=[
            SimpleNamespace(
                path="/activities",
                methods={"GET"},
                summary="List activities",
                name="get_activities",
            ),
            SimpleNamespace(
                path="/activities/{activity_name}",
                methods={"POST"},
                summary="Sign up",
                name="signup",
            ),
            SimpleNamespace(path="/docs", methods={"GET"}, name="docs"),
            SimpleNamespace(path="/openapi.json", methods={"GET"}, name="openapi"),
        ]
    )


def test_generate_api_documentation_is_sorted_and_filters_infrastructure():
    output = generate_api_documentation(fake_app())

    assert "| GET | `/activities` | List activities |" in output
    assert "| POST | `/activities/{activity_name}` | Sign up |" in output
    assert "/docs" not in output
    assert "/openapi.json" not in output
    assert output.index("/activities`") < output.index("/activities/{activity_name}")


def test_update_managed_section_replaces_only_managed_content():
    existing = (
        "# Title\n\n"
        f"{BEGIN_MARKER}\nOld docs\n{END_MARKER}\n\n"
        "Hand-authored footer.\n"
    )

    updated = update_managed_section(existing, f"{BEGIN_MARKER}\nNew docs\n{END_MARKER}")

    assert "# Title" in updated
    assert "Hand-authored footer." in updated
    assert "Old docs" not in updated
    assert "New docs" in updated


def test_update_managed_section_appends_when_markers_are_missing():
    updated = update_managed_section("# Title\n", f"{BEGIN_MARKER}\nDocs\n{END_MARKER}")

    assert updated.startswith("# Title\n")
    assert BEGIN_MARKER in updated
    assert "Docs" in updated


def test_mismatched_markers_raise_clear_error():
    with pytest.raises(DocumentationSyncError, match="mismatched"):
        update_managed_section(
            f"# Title\n{BEGIN_MARKER}\nDocs",
            f"{BEGIN_MARKER}\nNew docs\n{END_MARKER}",
        )


def test_markdown_special_characters_are_escaped():
    app = SimpleNamespace(
        routes=[
            SimpleNamespace(
                path="/items|special",
                methods={"GET"},
                summary="Get A | B\nnotes",
                name="get_items",
            )
        ]
    )

    output = generate_api_documentation(app)

    assert "/items\\|special" in output
    assert "Get A \\| B notes" in output


def test_check_mode_reports_drift_without_writing(tmp_path: Path):
    readme = tmp_path / "README.md"
    readme.write_text("# Existing\n", encoding="utf-8")

    changed = sync_documentation(fake_app(), readme, check=True)

    assert changed is True
    assert readme.read_text(encoding="utf-8") == "# Existing\n"


def test_sync_updates_readme(tmp_path: Path):
    readme = tmp_path / "README.md"
    readme.write_text("# Existing\n", encoding="utf-8")

    changed = sync_documentation(fake_app(), readme)

    assert changed is True
    content = readme.read_text(encoding="utf-8")
    assert BEGIN_MARKER in content
    assert "| GET | `/activities` | List activities |" in content
    assert "# Existing" in content


def test_missing_readme_is_an_error(tmp_path: Path):
    missing = tmp_path / "missing.md"

    with pytest.raises(DocumentationSyncError, match="not found"):
        sync_documentation(fake_app(), missing)
