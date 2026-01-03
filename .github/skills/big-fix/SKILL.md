
---

name: big-fix
description: Use this for complex bug fixes that span multiple modules or require careful regression coverage. Emphasize root cause analysis, minimal changes, and strong tests
---

# Big Fix Workflow

## Goals

- Identify root cause, not just symptoms.
- Fix with minimal, targeted changes.
- Add regression tests that fail before the fix and pass after.
- Keep coverage at or above 90% and ensure ruff + ty strict pass.

## Step-by-step

1) Reproduce

- Convert the Issue description into a deterministic repro:
  - minimal input files / minimal DataFrame
  - avoid external dependencies
- Add a failing test that captures the bug (red test).

1) Locate the failure

- Trace the call path in `src/data_processing/`.
- Prefer reading existing code and tests to infer intended behavior.

1) Implement the fix

- Prefer small refactors over large rewrites unless the Issue explicitly requests it.
- Maintain strict typing; avoid `Any` unless unavoidable and justified.

1) Validate

- Run the full validation workflow from `.github/copilot-instructions.md`:
  - ruff → ty → pytest
- If the fix impacts parsing/extraction (PDF/Excel/YAML), add focused tests:
  - PDF/table extraction: use tiny fixtures
  - Excel reading: use minimal xlsx fixtures or generated workbooks
  - YAML validation: include both valid and invalid cases

1) PR output

- PR description must include:
  - Root cause summary
  - Fix summary
  - Tests added (names/paths)
  - How to reproduce / verify
