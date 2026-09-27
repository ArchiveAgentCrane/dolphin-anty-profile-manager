# Contributing to dolphin-anty-profile-manager

Dolphin Anty Unlimited Profiles Method — an orchestration layer for running
many Dolphin Anty browser profiles in parallel from one Python process.

## Ground rules

- Python 3.11+. Use `ruff` and `mypy --strict` locally before pushing.
- One service per concern. Handlers stay thin; business logic lives in
  `services/`. Platform-specific glue lives in `adapters/`.
- No blocking calls in async paths. Wrap sync SDK calls with
  `asyncio.to_thread`.
- Every new profile mutation must emit an event through
  `services/event_bus.py` so the audit trail in `models/audit_entry.py`
  stays complete.

## Dev loop

```
python -m venv .venv && . .venv/bin/activate
pip install -e ".[dev]"
pytest -q
ruff check .
mypy dolphin_anty
```

## Branching

`main` is protected. Feature branches: `feat/<area>-<slug>`. Hotfixes branch
from the last tagged release and get cherry-picked back.

## Reporting profile-launch regressions

Include: Dolphin Anty build number, OS, profile count, the exact
`bootstrap.launch_batch` args, and a redacted `audit_entry` JSON line.