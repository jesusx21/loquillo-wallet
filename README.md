# Loquillo Wallet

Minimal personal-finance starter project in Python.

## Overview

This repository is a small wallet-style starter app. It includes the domain model, an example runner, fixtures, and in-memory persistence to demonstrate how the project is structured.

## Project layout

- `domain/` — business-logic layer: entities, services, and use cases.
- `database/` — persistence adapters and table definitions.
- `run_script/` — runnable example that seeds data and creates a sample transaction.
- `tests/` — unit/integration-style tests.
- `requirements/` — dependency files for runtime and development installs.

## Python version

The project targets Python 3.10+ and is expected to run with the version defined in `.python-version` via `pyenv`.

## Install dependencies

For development work, install the dev requirements explicitly:

```bash
python -m pip install --upgrade pip setuptools wheel
python -m pip install -r requirements/dev.txt
```

Use the production file only when you specifically want the runtime-only environment:

```bash
python -m pip install -r requirements/production.txt
```

Or use the provided Make targets:

```bash
make install-dev
make install-prod
```

If you are using `pyenv`, you can do this:

```bash
pyenv install 3.13.5
pyenv local 3.13.5
make install-dev
```

## Run the example

The runner is executed as a module so imports resolve correctly:

```bash
make run
```

Or directly:

```bash
PYTHONPYCACHEPREFIX=$(pwd)/.build/pycache python -m run_script
```

`PYTHONPYCACHEPREFIX` keeps Python bytecode under `.build/pycache` instead of scattering it across the repo.

## Quality checks

The project uses Flake8 for linting and keeps the workflow manual instead of auto-fixing code on commit:

```bash
make lint
```

This runs:

```bash
python -m flake8 .
```

If you want to review the rule set only, you can use:

```bash
make lint-fixes
```

## Tests

The project includes nose2-based tests.

```bash
make test
```

Or directly:

```bash
python -m nose2
```

## Cleanup

```bash
make clean
```

This removes generated cache/build artifacts such as `.build` and `.ruff_cache`.

## Contributing

Keep business rules inside `domain/` and add tests under `tests/` when changing behavior.
