PIP := pip
UVICORN := uvicorn
ALEMBIC := alembic
FLAKE8 := flake8

UVICORN_DEV_FLAGS := --reload

install:
	@$(PIP) install -r requirements/production.txt

install-dev:
	@$(PIP) install -r requirements/dev.txt

start-dev:
	@$(UVICORN) $(UVICORN_DEV_FLAGS) --host 0.0.0.0 --port 8080 server:app

migrations-create:
	@$(ALEMBIC) revision --autogenerate -m $(name)

migrations-run:
	@$(ALEMBIC) upgrade head
