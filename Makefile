PYTHON = python3

.PHONY: install run debug clean lint test

install:
	$(PYTHON) -m pip install -r requirements.txt

run:
	$(PYTHON) pac-man.py config.json

debug:
	$(PYTHON) -m pdb pac-man.py config.json

clean:
	find . -type d -name __pycache__ -prune -exec rm -rf {} +
	find . -type f -name '*.pyc' -delete

lint:
	$(PYTHON) -m flake8 src pac-man.py
	$(PYTHON) -m mypy src pac-man.py --check-untyped-defs

test:
	$(PYTHON) -m pytest tests
