VENV := .venv
PYTHON := $(VENV)/bin/python
PIP := $(VENV)/bin/pip

NB := notebooks/UAO_midterm.ipynb

.PHONY: venv install notebook run-notebook test clean

venv: $(VENV)/bin/python

$(VENV)/bin/python:
	python -m venv $(VENV)
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt

install: venv
	$(PIP) install -r requirements.txt

notebook: venv
	$(PYTHON) -m jupyter notebook $(NB)

run-notebook: venv
	$(PYTHON) -m jupyter nbconvert --to notebook --execute $(NB) --output UAO_midterm_executed.ipynb

test: venv
	$(PYTHON) -m pytest

clean:
	rm -f UAO_midterm_executed.ipynb
	find . -name "__pycache__" -type d -exec rm -rf {} +