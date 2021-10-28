# Classifying Chopped Genome Fragments

Pipeline to pass the genome fragments that have been chopped and randomly selected to each of the classification tools. Includes any necessary pre- and post-processing steps for consistent output.

## Pre-requisites

Before this can be run at full scale, fragments must be selected from the chopped genomes.

Currently, only 50 fragments have been selected from each kingdom/length combination.

## Scaling up

The Snakefile should not need to be edited, only the config files.

## Progress

The table below shows which steps have been written into the pipeline for each tool.

Tool                  | Pre-process | Running      | Post-process
--------------------- | ----------- | ------------ | ------------
DeepVirFinder         | *NA*        | Yes          | Yes
Seeker                | *NA*        | Yes          | Yes
Unlimited Breadsticks | *NA*        | *Developing* |  
VirSorter2            | *NA*        | Yes          | Yes

## Logging and Benchmarking

Stdout from the rules are forwarded to logs/{tool}/{rule}.log

Resource configuration from prediction steps are output to benchmarks/{tool}/{rule}_benchmark.txt
