# Metagenomic Phage Detection Benchmarking Datasets

## Description

There are 4 datasets included here meant for conducting benchmarks on metagenomic phage detection tools. The first is a set of fragmented reference genomes from NCBI Reference Sequence database (RefSeq) of a variety of micro-organisms and of different length. The second is a set of simulated phageomes created by simulating, assembling, and binning reads from bacteriophage genomes. The third is a set of simulated metagenomes with realistic abundance profiles modeled after marine metagenomes. The fourth is a set of real stool metagenomes from colorectal cancer patients and healthy controls (Study PRJEB6070).

Additionally, the results and resource usage from classification of these datasets by 9 phage detection tools are included.

---

## Unpacking the data

All datasets are compressed as `.tar.gz`, to extract the contents of these files to the current directory run:

```sh
$ tar -zxvf set*.tar.gz
```

To extract to another directory (*e.g.* `dir/`):

```sh
$ tar -C dir/ -zxvf set*.tar.gz
```

Once the tar files have been extracted, they can be deleted:

```sh
$ rm set*.tar.gz
```

---

## Structure

Once the datasets are extracted (and tar files deleted), there will be the following structure.

```sh
tree -L 1
.
├── LICENSE
├── README.md
├── set1_fragmented_genomes.tar.gz
├── set2_simulated_phageomes.tar.gz
├── set3_simulated_metagenomes.tar.gz
└── set4_crc_dataset.tar.gz
```

Each directory contains a `README.md` describing the dataset and files that are included.
