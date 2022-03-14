.PHONY: test, dryrun

test:
	python3 -m pytest -v --flake8 --pylint --pylint-rcfile=../../.pylintrc --mypy \
		tests/ \
		bracken_profiler.py \
		cat_genomes.py \
		summarize_profile.py \
		summarize_blast.py \
		filter_contigs.py

dryrun:
	snakemake -np --configfile config/config.yaml

coverage:
	coverage run -m pytest -v --mypy \
		tests/ \
		bracken_profiler.py \
		cat_genomes.py \
		summarize_profile.py \
		summarize_blast.py \
		filter_contigs.py
	coverage report -m
