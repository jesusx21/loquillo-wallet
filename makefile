PYTHON ?= python

install:
	$(PYTHON) -m pip install --upgrade pip setuptools wheel
	$(PYTHON) -m pip install -r requirements.txt

run:
	@mkdir -p .build/pycache
	PYTHONPYCACHEPREFIX=$$(pwd)/.build/pycache $(PYTHON) -m run_script

test:
	@mkdir -p .build/pycache
	PYTHONPYCACHEPREFIX=$$(pwd)/.build/pycache $(PYTHON) -m nose2

clean:
	@rm -rf .build
