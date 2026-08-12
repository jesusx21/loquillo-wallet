# Loquillo Wallet

Minimal personal-finance starter project in Python.

## Overview

This repository is a small starter for a wallet-style app. It contains core domain entities, a tiny async-backed runner (`run_script.py`), fixture data, and simple stores that demonstrate the app structure.

## Project layout (high level)

- `domain/` — business logic layer (entities, services, use-cases). Prefer this for domain rules instead of `app` or the project name.
- `fixtures/` — test/demo data and seeding helpers.
- `database/` — storage adapters and tables (memory/sql stores).
- `run_script.py` — interactive example that seeds data and creates a transaction.
- `requirements.txt` — pinned dependencies used for development and examples.

## Python version

The target Python version is declared in `.python-version`. We recommend using a maintained CPython (3.10+) or the version in the file via `pyenv`.

## Install dependencies

Recommended quick install:

```bash
python -m pip install --upgrade pip setuptools wheel
python -m pip install -r requirements.txt
```

If you use `pyenv`:

```bash
# install pyenv and pyenv-virtualenv (example macOS via Homebrew)
# brew install pyenv pyenv-virtualenv

# initialize pyenv in your shell, then:
pyenv install 3.13.5
pyenv local 3.13.5
python -m pip install -r requirements.txt
```

Note: some packages (for example `orjson`) may require Rust/toolchain to build from source; see Troubleshooting below.

## Run the example (interactive)

`run_script.py` is async and uses an interactive prompt. It runs with the event loop and executes the blocking prompt in a background thread, so running it is as simple as:

```bash
python run_script.py
```

If your system Python command is `python3` or you prefer a specific interpreter, call that binary instead.

## Domain layer

The `domain/` package holds the core business logic: entities (`domain/entities`), services (`domain/services.py`), and possible repository interfaces. This keeps rules and invariants isolated from persistence and transport concerns.

Suggested internal layout:

- `domain/entities.py` or `domain/entities/` — entity classes and value objects
- `domain/services.py` — orchestrating use-cases and application facades
- `domain/repositories.py` — repository interfaces/adapters (optional)

Naming rationale: `domain` avoids collision with `app` or configuration modules and aligns with Domain‑Driven Design conventions.

## Troubleshooting

- If `python` is not found or points to the wrong interpreter, run the script with `python3` or the full pyenv path.
- If installation of a wheel fails and the error references `maturin`/`cargo`, install Rust (`rustup`) locally:

```bash
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
source "$HOME/.cargo/env"
python -m pip install -r requirements.txt
```

## Tests

There are unit and integration style tests under `tests/`. Run them with your test runner (nose2 is present in dev requirements):

```bash
# run nose2 tests
nose2
```

## Contributing

If you add domain logic, keep it inside `domain/` and add tests under `tests/unit` or `tests/api` depending on scope.

---

If you want, I can:

- add a short `make` target to create a venv and install deps, or
- add a tiny demo script that prints fixture accounts to verify the environment quickly.
