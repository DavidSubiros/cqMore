SHELL=sh

.PHONY: audit
audit:
	@echo "python dependencies audit"
	pip-audit

.PHONY: build
build:
	@echo "building local conda environment"
	conda install -c conda-forge -c cadquery cadquery=master ocp numpy-stl pip-audit -y

.PHONY: test
test:
	@echo "executing Proveder CAD Service unit tests"
	python -m unittest discover -s ./tests -p 'test_*.py'


.PHONY: audit build test
