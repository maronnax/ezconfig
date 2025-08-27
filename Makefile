#include ./doc/Makefile

new:
	rm -fr .venv
	uv venv
	uv pip install -e ".[dev"]




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
