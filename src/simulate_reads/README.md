# Simulate Reads using InSilicoSeq

This is a Snakemake pipeline for generating simulated reads from reference genomes with specified abundances.

## Pipeline description

1. Concatenate genomes into single file
2. Pass to InSilicoSeq, varying error model

### Genome Concatenation

InSiicoSeq treats each record in a multi-FASTA file as a genome. However, some genome files have multiple records (*e.g.* separated by chromosome). The first part of the `cat_genomes` rule executes `cat_genomes.sh` which takes all genome files in the directory, and removes all record headers but the first. Then, these trimmed down genome files are all concatenated into a single file `cat_genomes.fasta`. The headers representing each genome in this new file are what must be used in the abundance profiles.

### Read Simulation

Several abundance profiles can be created, and the specified genomes must have identifiers that match those in `cat_genomes.fasta`. The list of desired abundance profiles should be given in the `--configfile`, as well as other `iss generate` parameters. Multiple error models can be automatically executed by inclusion in the config["model"] field, which currently includes all pre-built error models.
