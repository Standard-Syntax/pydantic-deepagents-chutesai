
---

name: feature-delivery
description: Use this for implementing new features (small or large). Focus on acceptance criteria, incremental commits, tests, and keeping API/CLI changes well documented
---

# Feature Delivery Workflow

## Inputs to extract from the Issue

- Acceptance criteria (convert to a checklist)
- Non-goals / constraints
- Target interfaces (CLI command, function, module)
- Backward-compat requirements

## Design approach (small vs large)

### Small feature

- Implement in a single module where possible.
- Add tests covering happy path + 1–2 edge cases.

### Large feature

- Break into milestones:
  1) scaffolding / interfaces + tests for contract
  2) core implementation
  3) performance considerations / monitoring (if applicable)
  4) docs updates and CLI UX polish
- Prefer composable functions and typed models (Pydantic) for IO boundaries.

## Data-processing specific guidance

- Prefer Polars for DataFrame transformations.
- Use DuckDB for SQL-style transforms when it improves clarity/perf.
- For configs, use Pydantic Settings and StrictYAML validation patterns already in the codebase.

## Testing

- Every feature PR must include tests under `tests/`.
- Ensure coverage ≥ 90% and that strict type checking passes.

## Validation

- Always run:
  - `ruff check .`
  - `ty`
  - `pytest`
(Use the repo’s canonical commands in `.github/copilot-instructions.md`.)

## PR output

- Include:
  - A checklist of acceptance criteria with ✅/❌
  - How to test
  - Any new CLI commands and example usage
