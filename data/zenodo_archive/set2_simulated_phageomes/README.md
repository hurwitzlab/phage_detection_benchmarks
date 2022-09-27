# Metagenomic Phage Detection Benchmarking Datasets
# Set 2: *Simulated phageomes*

## Description

This dataset contains a total of 58,678 contigs assembled from simulated reads from phage genomes, simulated using 3 error models. The following is the breakdown of the number of contigs.

Error Model | profile_1 | profile_2 | profile_3
| :-------: | :-------: | :-------: | :------: |
HiSeq       | 4,930     | 5,581     | 4,999
MiSeq       | 8,694     | 9,874     | 8,481
NovaSeq     | 5.140     | 5,816     | 5,163

The three profiles were created by, for each profile, selecting 500 phage genomes from the downloaded RefSeq database. The profiles were passed to InSilicoSeq to created simulated paired-end reads, with the specification of creating reads with 30x coverage. Simulated reads were assembled with MegaHit v1.2.9 with a minimum contig length of 1000 bp.

Contigs assembled from simulated reads were also binned with MetaBAT 2 v2:2.15 and using Bowtie2 v2.4.5 for indexing. The following number of bins were created.

Error Model | profile_1 | profile_2 | profile_3
| :-------: | :-------: | :-------: | :------: |
HiSeq       | 23        | 18        | 25
MiSeq       | 20        | 17        | 22
NovaSeq     | 24        | 19        | 22

The phageomes were classified with the classifiers, and those results are present here. During classification, resource usage was also recorded, and are present.

---

## Structure

The top level structure is as follows:

```sh
$ tree -L 1
.
├── assemblies/                  # Assembled simulated reads
├── bins/                        # Binned assemblies
├── contig_identities.csv        # Taxonomic origin of contigs
├── previous_classifications.csv # Classified phageomes
├── previous_resource_usage.csv  # Resources used during classification
└── README.md

2 directories, 4 files
```

---

## Directories

There are two directories: `assemblies` and `bins`:

```sh
$ tree assemblies/
assemblies/
├── profile_1_hiseq
│   └── assembly.fa
├── profile_1_miseq
│   └── assembly.fa
├── profile_1_novaseq
│   └── assembly.fa
├── profile_2_hiseq
│   └── assembly.fa
# ...
└── profile_3_novaseq
    └── assembly.fa

9 directories, 9 files

# Top level structure in bins/
$ tree bins/ -L 1
bins/
├── profile_1_hiseq
├── profile_1_miseq
├── profile_1_novaseq
├── profile_2_hiseq
# ...
└── profile_3_novaseq

9 directories, 0 files

# Inside a single bin directory
$ tree bins/profile_2_miseq/
bins/profile_2_miseq/
├── bin.10.fa
├── bin.11.fa
#...
└── bin.9.fa

0 directories, 17 files
```

---

## Files

### `previous_classifications.csv`

The phageomes have previously been classified by the following tools:

* DeepVirFinder
* MARVEL
* MetaPhinder
* Seeker
* VIBRANT
* viralVerify
* VirFinder
* VirSorter
* VirSorter2

Those classifications are present in the file `previous_classifications.csv`. Output from the original tools has already been cleaned, organized into a consistent manny, and compiled into this single file. The following columns are present:

* `tool`: Phage detection tool (*e.g.* DeepVirFinder)
* `phageome`: Phageome (*e.g.* profile_1_hiseq)
* `prediction`: Predicted identity, which has been grouped into "viral" or "non-viral"
* `lifecycle`: Lifecycle prediction (*e.g.* lytic or prophage) if given by tool
* `value`: Value upon which prediction is made, when given by tool
* `stat`: Statistic (*e.g.* p-value), when given by tool
* `stat_name`: Name of statistic in `stat` column

There may not be a row for each fragment for each tool. Missing observations come from tools that only create output for predicted viruses, so missing observation indicate a "non-viral" prediction.

---

### `previous_resource_usage.csv`

During classification of the genome fragments by the tools, resource usage was tracked by Snakemake, those results are compiled in `previous_resource_usage.csv`. Each row represents the resource usage while classifying a single file of 10k genome fragments.

The columns in this file are those created by Snakemake (information from [stackoverflow](https://stackoverflow.com/questions/46813371/meaning-of-the-benchmark-variables-in-snakemake))

column | type (unit) | description
:----: | :---------: | ------------
s  | float (seconds) | Running time in seconds
h:m:s | string (-) | Running time in hour, minutes, seconds format
max_rss | float (MB) | Maximum "Resident Set Size”, this is the non-swapped physical memory a process has used.
max_vms | float (MB) | Maximum “Virtual Memory Size”, this is the total amount of virtual memory used by the process
max_uss | float (MB) | “Unique Set Size”, this is the memory which is unique to a process and which would be freed if the process was terminated right now.
max_pss | float (MB) | “Proportional Set Size”, is the amount of memory shared with other processes, accounted in a way that the amount is divided evenly between the processes that share it (Linux only)
io_in | float (MB) | the number of MB read (cumulative).
io_out | float (MB) | the number of MB written (cumulative).
mean_load | float (-) | CPU usage over time, divided by the total running time (first row)
cpu_time | float(-) | CPU time summed for user and system
tool | string | Phage detection tool
phageome| string | Phageome name

---

### `assembly.fa`

Each `assembly.fa` file is a FASTA structured file. The headers give taxonomic information about each genome fragment.

```sh
$ head -n 2 assemblies/profile_1_miseq/assembly.fa
>k141_65526 flag=1 multi=1.0000 len=501
ACAATGCTGTTGACGATGTTCTCGATGGTTTCCCGCAGATTCTCCGGGCCGAGCATGCCGGCGATTGACTCGGGGGAGATGTTGCGCAAAGCGTCGACAAATCCTCCAGCGTGTTCTCAACGGTCTGCACGCCGCCGCGCATCACTGACACGACCGTGTCAATGGTCAACTGCACACGCGCCAACAGGGTTGG
# ...

# Each record starts with a ">"
$ grep ">" assemblies/profile_1_miseq/assembly.fa | wc -l
8694
```

These files were classified by all tools except MARVEL.

---

### `bin.*.fa`

Each bin directory contains files of binned contigs, named as `bin.*.fa`, each of which is a FASTA file.

```sh
head -n 2 bins/profile_1_miseq/bin.1.fa
>k141_15995
GTAAATCTAAGGTCTGTCCGGTAATCCACTTCGAGGACAAAGAATGAGAACAGTTATGAA
```

The bins were classified by MARVEL.

---

### `contig_identities.csv`

The true identities of the contigs in each phageome were obtained by running a BLAST search against a database composed of the phage genomes used for simulation of that particular phageome. Based on the accession number of the BLAST matches, TaxIDs were retrieved, and further taxonomic information was obtained using the R package taxonomizr. These results are present in the file `contig_identities.csv`.

The file contains the following columns:

* `profile`: Phageome profile
* `model`: InSilicoSeq error model
* `query_id`: Contig ID that was queried by BLAST
* `query_length`: Query contig length (nt)
* `origin`: Either "single" for alignment to single organism or "chimera" for misassembly
* `accession`: Sequence accession number
* `seq_id`: Sequence SeqID
* `taxid`: Organism TaxID
* `species_taxid`: Species level TaxID (may be same as taxid)
* `superkingdom`
* `phylum`
* `class`
* `order`
* `family`
* `genus`
* `species`
