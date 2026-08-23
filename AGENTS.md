# AGENTS.md

Guidance for AI coding agents (Claude Code, Copilot, Cursor, etc.) working in this
repository. Human contributors may find it useful too, but the primary audience is
an agent preparing a pull request.

## Before you start

Open an issue and discuss the change before writing a PR — see "Contribute" in
`README.md`. This avoids agents (and their operators) spending effort on a PR that
gets rejected for being out of scope.

## Setup

This project uses [`uv`](https://docs.astral.sh/uv/) to manage the virtualenv and
dependencies. Don't `pip install` into a venv by hand and don't hand-edit
`uv.lock`.

```bash
uv sync
```

## Running checks

Run these before proposing a change as done — they are what CI
(`.github/workflows/ci.yml`) runs.

```bash
uv run pytest              # unit tests
uv run pylint irc2phpbb    # lint production code
uv run pylint tests        # lint tests
```

Coverage (optional, not enforced by CI):

```bash
uv run pytest --cov=irc2phpbb
```

Do not commit generated coverage reports (`htmlcov/`, `.coverage`).

## Project layout

- `irc2phpbb/` — the package. `bot.py` / `irc_bot.py` / `discord_bot.py` wire up the
  bot; `marvin_actions.py` and `marvin_general_actions.py` hold the individual
  chat actions (one function per command/response); `data/marvin_strings.json`
  holds the response text those actions pick from; `config/` holds default JSON
  config.
- `tests/` — one `test_<action>.py` per action module, named after the action it
  covers (e.g. `marvinSayHi` → `tests/test_hello.py`). `test_action.py` provides
  the shared `ActionTest` base class (`assertActionOutput`, `assertActionSilent`)
  — use it instead of re-implementing action-invocation boilerplate.

## Conventions

- New chat actions: add the function to `marvin_actions.py` (or
  `marvin_general_actions.py`), register it in `getAllActions()`, add response
  strings to `data/marvin_strings.json` rather than hardcoding them, and add a
  matching `tests/test_<name>.py` using the `ActionTest` base class.
- Max line length is 100 (`.pylintrc`); keep `uv run pylint` clean rather than
  suppressing new warnings.
- Don't add new runtime dependencies without discussing in the issue first —
  Marvin is meant to stay light enough to run in the provided Docker image.

## Docs

Public API docs are generated with `pdoc` and published from `master`; don't hand-
edit anything under `docs/pdoc`.

```bash
uv run pdoc --output-dir=docs/pdoc irc2phpbb
```
