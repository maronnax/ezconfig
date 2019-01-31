#include ./doc/Makefile

test:
	nosetests -s test

up: | ./venv/bin/python ## Install tool dependencies in a virtualenv

./venv/bin/python:
	virtualenv -p python2.7 venv
	./venv/bin/pip install --upgrade pip

	# Install basic requirements
	./venv/bin/pip install -r requirements.txt

	# Install nose for testing
	./venv/bin/pip install nose

	# Install nose for testing
	./venv/bin/pip install sphinx sphinx-autobuild

pipy-upload:
	python setup.py sdist upload -r pipy

.PHONY: test doc
