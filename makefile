PYTHON ?= python
ALEMBIC ?= $(PYTHON) -m alembic -c alembic.ini
REVISION ?= -1

install: install-dev

install-prod:
	$(PYTHON) -m pip install --upgrade pip setuptools wheel
	if [ -f requirements/production.txt ]; then $(PYTHON) -m pip install -r requirements/production.txt; fi

install-dev:
	@echo "Installing development dependencies from requirements/dev.txt"
	$(PYTHON) -m pip install --upgrade pip setuptools wheel
	if [ -f requirements/dev.txt ]; then $(PYTHON) -m pip install -r requirements/dev.txt; fi

run:
	@mkdir -p .build/pycache
	PYTHONPYCACHEPREFIX=$$(pwd)/.build/pycache $(PYTHON) -m run_script

test:
	@mkdir -p .build/pycache
	PYTHONPYCACHEPREFIX=$$(pwd)/.build/pycache $(PYTHON) -m nose2

lint:
	@mkdir -p .build/pycache
	PYTHONPYCACHEPREFIX=$$(pwd)/.build/pycache $(PYTHON) -m flake8 .

lint-fixes:
	@echo "Manual review only. Flake8 reports issues but does not rewrite files."
	@echo "Use: $(PYTHON) -m flake8 ."

clean:
	@rm -rf .build

migration-create:
	@mkdir -p .build/pycache
	@read -p "Enter migration message: " msg; \
	PYTHONPYCACHEPREFIX=$$(pwd)/.build/pycache $(ALEMBIC) revision --autogenerate -m "$$msg"

migration-run:
	@mkdir -p .build/pycache
	PYTHONPYCACHEPREFIX=$$(pwd)/.build/pycache $(ALEMBIC) upgrade head

rollback-run:
	@mkdir -p .build/pycache
	PYTHONPYCACHEPREFIX=$$(pwd)/.build/pycache $(ALEMBIC) downgrade $(REVISION)
