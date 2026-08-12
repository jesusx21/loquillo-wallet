# Loquillo Wallet (Mister Krabz)

Loquillo Wallet is a REST API for managing personal finances, including
**wallets**, **categories** / subcategories, and the **accounting accounts**
associated with each wallet.

The project is written in Python using [Falcon](https://falcon.readthedocs.io/)
(ASGI), served with [uvicorn](https://www.uvicorn.org/), and persists data in
PostgreSQL through SQLAlchemy (async, `asyncpg` driver) using Alembic migrations.
It also includes an in-memory database driver used by the test suite.

## Project overview

This application exposes a lightweight API for organizing a personal finance
workspace with clear domain boundaries:

- Wallets represent cash flows or accounts to track
- Categories and subcategories provide a classification structure
- Accounts are linked to wallets and can be grouped under those categories
- The business logic lives in the `mister_krabz/` layer, keeping the API thin

## Project structure

| Folder | Purpose |
| ------- | ------- |
| `api/v1/` | HTTP resources for API v1 |
| `app/` | Falcon application, middleware, error handling, healthcheck, media handlers |
| `mister_krabz/` | Domain logic, use cases, entities |
| `database/` | Stores (`sql` and `memory`), tables, custom types |
| `migrations/` | Alembic migrations |
| `tests/` | Unit, API, and database tests |
| `makefile` | Development tasks |

## API endpoints

All routes are under the prefix `/MrKrabz/api/v1`:

| Method | Route | Description |
| ------ | ----- | ----------- |
| GET | `/health` | Healthcheck |
| POST | `/categories` | Create a category |
| GET | `/categories` | List categories |
| GET | `/categories/{category_id}` | Get a category by id |
| POST | `/categories/{category_id}/subcategories` | Create a subcategory |
| GET | `/categories/{category_id}/subcategories` | List subcategories |
| POST | `/wallets` | Create a wallet |
| GET | `/wallets` | List wallets |
| GET | `/wallets/{wallet_id}` | Get a wallet by id |
| PUT | `/wallets/{wallet_id}` | Update a wallet |
| POST | `/wallets/{wallet_id}/categories/{category_id}/add` | Add a category to a wallet |

## Requirements

- Python 3.8+ (the project has been run with Python 3.10)
- PostgreSQL (for the `sql` driver; tests can run using the in-memory driver)
- `make`

## Installation

A virtual environment is recommended:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
make install       # production dependencies only (requirements/production.txt)
make install-dev   # production + development tooling (requirements/dev.txt)
```

`requirements/common.txt` contains the core stack (Falcon, Uvicorn, SQLAlchemy,
Alembic, asyncpg, PyJWT, orjson, pyhumps, and more). `requirements/dev.txt`
adds development tools such as `flake8`, `nose2`, `assertpy`, `freezegun`,
`aioresponses`, `logassert`, and `tox`.

## Configuration

The app reads `./config.ini` (ignored by git). Create it from the sample file and
adjust the values to match your environment:

```bash
cp config.sample.ini config.ini
```

```ini
[database]
driver = sql              # 'sql' (PostgreSQL) or 'memory' (in-memory)
username = postgres
database = mister_krabz_dev

# Default values for the SQL driver
# host = localhost
# port = 5432
# password =

# Database used by tests
# test_database = mister_krabz_test
```

Notes:

- Environment values are available inside the `.ini` file because `ConfigParser`
  is initialized with `os.environ`, so variable interpolation is supported.
- Alembic (`alembic.ini`) also reads the database URL from `config.ini`.
- Tests use `tests/config.py`, which forces the `memory` driver by default and
  falls back to `mister_krabz_test` when SQL is required.

Create the databases and run the migrations:

```bash
createdb mister_krabz_dev
createdb mister_krabz_test   # only if you are running tests against SQL
make migrations-run
```

## Running the project

```bash
make start-dev
```

This starts uvicorn with auto-reload on `http://0.0.0.0:8080` using the
`server:app` entrypoint. To verify the service:

```bash
curl http://localhost:8080/MrKrabz/api/v1/health
```

## Makefile tasks

| Task | What it does |
| ---- | ------------ |
| `make install` | Installs production dependencies (`requirements/production.txt`) |
| `make install-dev` | Installs development dependencies (`requirements/dev.txt`) |
| `make start-dev` | Runs the server with uvicorn on `0.0.0.0:8080` using `--reload` |
| `make migrations-create name=<name>` | Generates a migration with `alembic revision --autogenerate -m <name>` |
| `make migrations-run` | Applies pending migrations (`alembic upgrade head`) |
| `make migrations-rollback migrations=N` | Rolls back N migrations (`alembic downgrade -N`) |

Binary paths can be overridden through variables, e.g. if you use a virtualenv
or `pip3`:

```bash
make install PIP=pip3
make start-dev UVICORN=.venv/bin/uvicorn
```

Examples:

```bash
make migrations-create name=create_transactions_table
make migrations-rollback migrations=1
```

## Linting

The project uses **flake8** (declared in `requirements/dev.txt` and exposed as
`FLAKE8` in the makefile, although there is no `make lint` task at the moment).
Run it directly:

```bash
flake8 .            # whole project
flake8 api app      # selected folders only
```

There is no flake8 configuration file, so the default settings apply (maximum
line length of 79 characters, etc.).

## Testing

The test suite uses **nose2** on top of `unittest` (`IsolatedAsyncioTestCase`)
and `assertpy`. The configuration lives in `nose2.cfg`, which looks for files
matching `*_test.py` from the repository root. There is also no make task for
this, so tests are run directly:

```bash
nose2                                   # full suite
nose2 tests.unit                        # unit tests only
nose2 tests.api                         # API tests only
nose2 tests.database                    # database tests only
nose2 tests.unit.mister_krabz.wallets_test   # specific module
nose2 -v                                # verbose output
```

Requirements for running tests:

- `config.ini` must exist (tests read it from the repo root)
- By default they use the in-memory database; the checks under
  `tests/database/sql` require PostgreSQL and the database indicated in
  `test_database`

## Contributing

- Base development branch: `develop`
- Run `flake8 .` and `nose2` before opening a PR
- Commits follow the format `[LW-<number>] Description` (ticket + summary)

## Notes

The project is intentionally organized around a small domain layer and a simple
API boundary, making it easy to test and extend as new finance features are added.
