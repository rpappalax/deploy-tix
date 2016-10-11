HERE = $(shell pwd)
VENV = ./venv
BIN = $(VENV)/bin
PYTHON = $(BIN)/python
PIP = $(BIN)/pip
INSTALL = $(PIP) install

.PHONY: all build test clean

all:	build test

build: $(VENV)/COMPLETE
$(VENV)/COMPLETE: requirements.txt
	mkdir -p build
	virtualenv --no-site-packages --python=`which python` --distribute $(VENV)
	# virtualenv --no-site-packages --python='/usr/bin/python2.6' --distribute $(VENV)
	$(INSTALL) -r requirements.txt
	$(PYTHON) setup.py develop
	touch $(VENV)/COMPLETE

test:
	$(INSTALL) -r test_requirements.txt
	tox -r

clean:
	rm -rf venv  *egg*  dist  ./docs/_build  .tox
	find . -name '*.pyc' -delete
	find . -name '__pycache__' -type d -exec rm -fr {} \;

