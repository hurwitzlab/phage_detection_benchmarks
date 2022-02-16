.PHONY: test, dryrun

test:
	python3 -m pytest -xv --flake8 --pylint

dryrun:
	snakemake -np --configfile config/practice_config.yaml
