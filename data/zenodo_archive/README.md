# Metagenomic Phage Detection Benchmarking Datasets

## Description

There are 4 datasets included here meant for conducting benchmarks on metagenomic phage detection tools. The first is a set of fragmented reference genomes from RefSeq of a variety of organisms and of different length. The second is a set of simulated phageomes created by simulating, assembling, and binning reads from bacteriophage genomes. The third is a set of simulated metagenomes with realistic abundance profiles modeled after marine metagenomes. The fourth is a set of real stool metagenomes from colorectal cancer patients and healthy controls.

Additionally, the results and resource usage from classification of these datasets by 9 phage detection tools are included.

---

## Unpacking the data

All datasets are compressed as `.tar.gz`, to extract the contents of these files to the current directory run:

```sh
$ tar -zxvf benchmark*.tar.gz
```

To extract to another directory (*e.g.* `dir/`):

```sh
$ tar -C dir/ -zxvf benchmark*.tar.gz
```

Once the tar files have been extracted, they can be deleted:

```sh
$ rm benchmark*.tar.gz
```

---

## Structure

Once the datasets are extracted (and tar files deleted), there will be the following structure.

```sh
tree -L 1
.
├── benchmark1_fragmented_genomes.tar.gz
├── benchmark2a_simulated_phageomes.tar.gz
├── benchmark2b_simulated_metagenomes.tar.gz
├── benchmark3_crc_dataset.tar.gz
└── README.md
```

Each directory contains a `README.md` describing the dataset and files that are included.

---

## Authorship
Kenneth Schackart <schackartk1@gmail.com>
