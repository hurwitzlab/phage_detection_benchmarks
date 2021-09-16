# Select Genome Fragments

Here are the scripts for using the [selector.py](https://github.com/schackartk/challenging-phage-finders/tree/main/src/data_selection) script to select random fragments from the chopped genomes.

This includes providing a `run.slurm` script, a `Snakefile`, and `config` files.

## Usage

```
snakemake -j 16 --configfile config/config.yaml
```

## Making Changes

The Snakefile should not need to be changed, since all mutable things should be stored in the `config` files. Accordingly, the Snakefile was refined using the practice data located in the selector.py tests directry.
