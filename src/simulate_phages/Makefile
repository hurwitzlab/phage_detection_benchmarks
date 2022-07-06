.PHONY: test, dryrun

test:
	python3 -m pytest -v --flake8 --pylint --pylint-rcfile=../../.pylintrc --mypy \
		phage_profiler.py

dryrun:
	snakemake -np --configfile config/config.yaml

coverage:
	coverage run -m pytest -v --mypy \
		phage_profiler.py
	coverage report -m
