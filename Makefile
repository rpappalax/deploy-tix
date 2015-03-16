VENVDIR = ./build/venv
BINDIR = $(VENVDIR)/bin
PYTHON = $(BINDIR)/python
PIP = $(BINDIR)/pip
INSTALL = $(PIP) install
MAKEFILE_LIST=Makefile

.PHONE: help
help:
	@echo ""
	@echo "HELP"
	@echo "========================================"
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'  |  \
	    awk '{print "$ make "$$2 " # "substr($$0, index($$0,$$3))}'
	@echo ""
	@echo "Run:"
	@echo "make build:"
	@echo "source ./build/venv/bin/activate"
	@echo "ticket -h"
	@echo ""


.PHONY: all  ## Build all
all:	build test

.PHONY: build
build: $(VENVDIR)/COMPLETE
$(VENVDIR)/COMPLETE: requirements.txt
	mkdir -p build
	virtualenv --no-site-packages --python=`which python` --distribute $(VENVDIR)
	$(INSTALL) -r ./requirements.txt
	$(PYTHON) ./setup.py develop
	touch $(VENVDIR)/COMPLETE

.PHONY: build-jenkins
build-jenkins: $(VENVDIR)/COMPLETE
$(VENVDIR)/COMPLETE: requirements.txt
	mkdir -p build
	virtualenv --no-site-packages --python='/usr/bin/python2.7' --distribute $(VENVDIR)
	#virtualenv --no-site-packages --python='/usr/local/bin/python3.4' --distribute $(VENVDIR)
	$(INSTALL) -r ./requirements.txt
	$(PYTHON) ./setup.py develop
	touch $(VENVDIR)/COMPLETE

.PHONY: clean  ## Clean all build files
clean:
	rm -rf build
	rm -rf *egg*
	rm -rf dist
	rm -rf .tox
	find . -name "*.pyc" -exec rm -rf {} \;


# for dev branch only

.PHONY: pypi  ## Create dist, egg dirs, upload package to pypi
pypi:
	# Create dist, egg dirs, upload package to pypi
	$(PYTHON) setup.py sdist upload -r pypi
	$(PYTHON) setup.py bdist_egg upload -r pypi

.PHONY: testpypi  ## Create dist, egg dirs, upload package to testpypi
testpypi:
	# Create dist, egg dirs, upload package to testpypi
	$(PYTHON) setup.py sdist upload -r testpypi
	$(PYTHON) setup.py bdist_egg upload -r testpypi

.PHONY: pypi-register  ## Register the project to Python package index
pypi-register:
	$(PYTHON) setup.py register -r pypi

.PHONY: testpypi-register  ## Register the project to Test Python package index
testpypi-register:
	$(PYTHON) setup.py register -r testpypi
