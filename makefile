UVICORN := uvicorn

UVICORN_DEV_FLAGS := --reload

start-dev:
	@$(UVICORN) $(UVICORN_DEV_FLAGS) --host 0.0.0.0 --port 8080 server:app
