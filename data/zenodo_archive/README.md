# Metagenomic Phage Detection Benchmarking Datasets

## Description

There are 4 datasets included here meant for conducting benchmarks on metagenomic phage detection tools. The first is a set of fragmented reference genomes from RefSeq of a variety of organisms and of different length. The second is a set of simulated phageomes created by simulating, assembling, and binning reads from bacteriophage genomes. The third is a set of simulated metagenomes with realistic abundance profiles modeled after marine metagenomes. The fourth is a set of real stool metagenomes from colorectal cancer patients and healthy controls.

Additionally, the results and resource usage from classification of these datasets by 9 phage detection tools are included.

## Structure

```sh
tree -L 1
.
├── benchmark1_fragmented_genomes
├── benchmark2a_simulated_phageomes
├── benchmark2b_simulated_metagenomes
├── benchmark3_crc_dataset
└── README.md
```

Each directory contains a `README.md` describing the dataset and files that are included.

## Authorship
Kenneth Schackart <schackartk1@gmail.com>
