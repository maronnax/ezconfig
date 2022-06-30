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



dist-files:
	rm dist/*
	python setup.py sdist bdist_wheel


# See `https://widdowquinn.github.io/coding/update-pypi-package/' for
# latest pypi upload info I reference.
pypi-upload: dist-files
	python -m twine upload dist/*

test-pypi-upload: dist-files
	python -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*


.PHONY: test doc
