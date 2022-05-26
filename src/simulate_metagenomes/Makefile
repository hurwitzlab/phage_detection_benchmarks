.PHONY: test, dryrun

test:
	python3 -m pytest -v --flake8 --pylint --pylint-rcfile=../../.pylintrc --mypy \
		tests/ \
		phage_injector.py \
		bracken_profiler.py \
		cat_genomes.py \
		summarize_profile.py \
		summarize_blast.py \
		summarize_contigs.py \
		sort_blast.py \
		combine_summary.py

dryrun:
	snakemake -np --configfile config/config.yaml

coverage:
	coverage run -m pytest -v --mypy \
		tests/ \
		phage_injector.py \
		bracken_profiler.py \
		cat_genomes.py \
		summarize_profile.py \
		summarize_blast.py \
		summarize_contigs.py \
		sort_blast.py \
		combine_summary.py
	coverage report -m
