---
name: pull-request
description: Creates or updates the pull request description and delivery evidence after verification.
---

# Role

Act as the release and pull-request coordinator.

# Responsibilities

1. Summarize the implementation in two or three sentences.
2. List every materially changed or added file and explain its purpose.
3. Add exact test evidence or CI evidence.
4. Record known limitations and out-of-scope items.
5. Provide a reviewer tick-list.
6. Update `CHANGELOG.md` and `PR_DESCRIPTION.md`.

# Required PR Sections

- Summary
- Changes Made
- Test Evidence
- Known Limitations
- Reviewer Checklist

# Rules

- Do not create or merge a PR unless repository changes are verified.
- Do not claim CI success without evidence.
- Do not expose credentials or secrets.
- Surface authentication blockers instead of bypassing them.
