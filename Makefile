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


# See `https://widdowquinn.github.io/coding/update-pypi-package/' for
# latest pypi upload info I reference.
pipy-upload:
	python -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*

test-pipy-upload:
	python -m twine upload dist/*

.PHONY: test doc
