# Loquillo Wallet

Minimal personal-finance starter project in Python.

## Overview

This repository is a small starter for a wallet-style app. It currently contains a few modules, fixture data, and a simple runner script for local experimentation.

## Current repository state

Key files and folders:

- `.python-version` — configured Python version for the project
- `requirements.txt` — pinned requirements for this workspace
- `run_script.py` — small example runner
- `account.py`, `entry.py` — simple domain classes
- `fixtures/` — fixture data used by the examples

## Python version

The project declares its Python target in `.python-version`.

## Requirements

Install the dependencies listed in `requirements.txt`:

```bash
python -m pip install --upgrade pip setuptools wheel
python -m pip install -r requirements.txt
```

## Recommended: pyenv (optional)

If you prefer `pyenv` to manage interpreters, install `pyenv` and `pyenv-virtualenv`, then set the project Python and create/activate a virtualenv:

```bash
# install pyenv (example macOS Homebrew)
# brew install pyenv pyenv-virtualenv

# add initialization to your shell (e.g. ~/.zshrc)
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"

# install and set local Python (example)
pyenv install 3.13.5
pyenv local 3.13.5

# optional: create and activate a pyenv virtualenv
pyenv virtualenv 3.13.5 loquillo-3.13.5
pyenv activate loquillo-3.13.5

# then install requirements
python -m pip install -r requirements.txt
```

## Run

Run the example script from the repository root:

```bash
python run_script.py
```

If you encounter import errors when running directly (e.g. `attempted relative import`), ensure you run from the project root or use the module form:

```bash
python -m run_script
```

## Fixtures

The `fixtures/` package provides sample `accounts` used by the examples. The package exports its public API via `__all__` in `fixtures/__init__.py`.

## Notes & Troubleshooting

- Make sure `python` in your PATH points to the interpreter where you installed the requirements (use `python3` or the pyenv-managed binary if necessary).
- To install dependencies quickly: `python -m pip install -r requirements.txt`.

If you'd like, I can add a small example that prints the fixture accounts or a `make` target to automate setup.
