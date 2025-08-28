#include ./doc/Makefile

venv:
	rm -fr .venv
	uv venv
	uv pip install -e ".[dev"]

dist-files:
	rm -rf dist/
	python -m build

pypi-upload: dist-files
	python -m twine upload dist/* --repository ezconfig

test-pypi-upload: dist-files
	python -m twine upload dist/* --repository ezconfig-test

.PHONY: test doc
