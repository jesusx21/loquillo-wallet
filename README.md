# Loquillo Wallet

Minimal personal-finance starter project in Python.

## Overview

This repository is a small wallet-style starter app built around domain entities, SQLAlchemy table definitions, and in-memory or SQL-backed persistence layers.

## Project layout

- `domain/` — business rules and entity definitions.
- `database/` — SQLAlchemy metadata, table definitions, and store implementations.
- `run_script/` — example runner that creates and seeds wallet data.
- `tests/` — project tests, including SQL-backed fixtures and account/transaction checks.
- `requirements/` — dependency files for development and production.
- `migrations/` — Alembic migration scripts and configuration.

## Python version

The project targets Python 3.10+ and expects the version defined in `.python-version` via `pyenv`.

## Install dependencies

For development work:

```bash
python -m pip install --upgrade pip setuptools wheel
python -m pip install -r requirements/dev.txt
```

For runtime only:

```bash
python -m pip install -r requirements/production.txt
```

Or use the project shortcuts:

```bash
make install-dev
make install-prod
```

With `pyenv`:

```bash
pyenv install 3.13.5
pyenv local 3.13.5
make install-dev
```

## Available make tasks

- `make install` — installs the project dependencies for development.
- `make install-prod` — installs the runtime dependencies only.
- `make install-dev` — installs the development dependencies from `requirements/dev.txt`.
- `make run` — starts the app entrypoint.
- `make test` — runs the project test suite with `nose2`.
- `make lint` — runs `flake8` to check style and errors.
- `make lint-fixes` — shows the linting command to review manually.
- `make clean` — removes generated build/cache artifacts.
- `make migration-create` — generates an Alembic migration from the current schema.
- `make migration-run` — applies pending migrations to the database.
- `make rollback-run REVISION=-1` — rolls back the last migration.

## Run the app

```bash
make run
```

Or directly:

```bash
PYTHONPYCACHEPREFIX=$(pwd)/.build/pycache python -m run_script
```

`PYTHONPYCACHEPREFIX` keeps Python bytecode under `.build/pycache` to avoid scattering cache files across the repo.

## Tests and lint

Run the unit suite:

```bash
make test
```

Or directly:

```bash
python -m nose2
```

Run the linter:

```bash
make lint
```

Or directly:

```bash
python -m flake8 .
```

## Database migrations

Generate an autogenerate migration:

```bash
make migration-make
```

Apply migrations:

```bash
make migration-run
```

Rollback a revision:

```bash
make rollback-run REVISION=-1
```

The migration targets are kept compatible with both the older name (`migration-make`) and the newer explicit name (`migration-create`).

## Cleanup

```bash
make clean
```

This removes generated cache/build artifacts such as `.build` and `.ruff_cache`.

## Contributing

Keep business rules in `domain/`, persist data in `database/`, and add tests under `tests/` whenever behavior changes.
