#include ./doc/Makefile

venv:
	rm -fr .venv
	uv venv
	uv pip install -e ".[dev"]

clean:
	rm -rf dist/ build/ *.egg-info

dist-files: clean
	rm -rf dist/
	# python -m build
	uv build --no-sources

pypi-upload: dist-files
	python -m twine upload dist/* --repository ezconfig

test-pypi-upload: dist-files
	#python -m twine upload dist/* --repository ezconfig-test
	uv publish --index testpypi

.PHONY: test doc clean dist-files
