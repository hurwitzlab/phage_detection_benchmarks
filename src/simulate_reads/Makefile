.PHONY: test, dryrun

test:
	python3 -m pytest -v --flake8 --pylint --mypy tests/ bracken_profiler.py cat_genomes.py

dryrun:
	snakemake -np --configfile config/practice_config.yaml
