# Simulate Reads using InSilicoSeq

This is a Snakemake pipeline for generating simulated reads from reference genomes with specified abundances.

## Pipeline description

1. Concatenate genomes into single file
2. Pass to InSilicoSeq, varying error model

### Genome Concatenation

InSiicoSeq treats each record in a multi-FASTA file as a genome. However, some genome files have multiple records (*e.g.* separated by chromosome). The first part of the `cat_genomes` rule executes `cat_genomes.sh` which takes all genome files in the directory, and removes all record headers but the first. Then, these trimmed down genome files are all concatenated into a single file `cat_genomes.fasta`. The headers representing each genome in this new file are what must be used in the abundance profiles.

### Read Simulation

Several abundance profiles can be created, and the specified genomes must have identifiers that match those in `cat_genomes.fasta`. The list of desired abundance profiles should be given in the `--configfile`, as well as other `iss generate` parameters. Multiple error models can be automatically executed by inclusion in the config["model"] field, which currently includes all pre-built error models.


## `braken_profiler.py`

This script takes Braken output and creates a profile for use in ISS. Taxonomic IDs are used to join the Braken output with my list of refseq genomes. Since not all genomes may be found, the abundances are rescaled so they still add to 1. The abundance profile is written to `*_profile.txt`.

Additionally, a file is created (`*_files.txt`) that contains a list of "file names" (file globs that should only match one file). The files that match these globs are the files that contain the sequences in the profile.

Example usage
```
 $ ./braken_profiler.py tests/inputs/braken_profiler/input_1.txt
Done. Wrote output files to "out".

$ ls out/
input_1_files.txt  input_1_profile.txt

# File globs do not include the parent directory (refseq)
$ head -n 3 out/input_1_files.txt 
bacteria/GCF_006742345.1*.fna
bacteria/GCF_004328515.1*.fna
bacteria/GCF_015679285.1*.fna

# First column is sequence ID, so will still need to use cat_genomes.sh
$ head -n 3 out/input_1_profile.txt 
NZ_AP019724.1   0.1027
NZ_CP036491.1   0.0189
NZ_CP064937.1   0.01957
```
