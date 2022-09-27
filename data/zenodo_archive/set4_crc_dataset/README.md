# Metagenomic Phage Detection Benchmarking Datasets
# Set 4: *CRC dataset*

## Description

This dataset contains 198 metagenomes for a total of 29,285,217 contigs. Metagenomes are fecal shotgun metagenomes from colorectal cancer (CRC) patients and healthy controls (https://doi.org/10.15252/msb.20145645). Raw sequencing data were downloaded from SRA (PRJEB6070) and were quality filtered using fastqc v0.11.9 and trimGalore v0.6.6. Briefly, reads with an average base pair quality score below 20 were removed, and adapters and poly-G sequences were trimmed. After trimming, reads with a length < 20bp were filtered out. Quality-filtered sequences were screened to remove human sequences using bowtie2 v2.4.2 against a non-redundant version of the Genome Reference Consortium Human Build 38, patch release 7 (available at PRJNA31257 in NCBI).

After QC and human read filtering, the reads were assembled using Megahit v1.2.9. The code of 
the pipeline used for the assembly is available on Github (https://github.com/aponsero/Assembly_metagenomes). Megahit was run on the paired-end reads or single-end reads using the default parameters (referred to as the simple assembly). Additionally, a co-assembly of the multiple runs per BioSample was also performed (referred to as the co-assembly). 

Contigs were also binned with MetaBAT 2 v2:2.15 and using Bowtie2 v2.4.5 for indexing.

The metagenomes were classified with the phage detection tools, and those results are present here. During classification, resource usage was also recorded, and are present.

CheckV v1.0.1 was used to assess all contigs for bacterial and viral genes.

---

## Structure

The top level structure is as follows:

```sh
$ tree -L 1
.
├── assemblies                   # Assembled reads
├── bins                         # Binned assemblies
├── checkv_quality_summary.csv   # CheckV results
├── previous_classifications.csv # Classified metagenomes
├── previous_resource_usage.csv  # Resources used during classification
└── README.md

2 directories, 2 files
```

---

## Directories

There are two directories: `assemblies/` and `bins/`:

```sh
$ tree assemblies/
assemblies/
├── 2466887
│   └── assembly.fa
├── 2466888
│   └── assembly.fa
# ...
└── 2467085
    └── assembly.fa

198 directories, 198 files

# Top level structure in bins/
$ tree bins/ -L 1
bins/
├── 2466887
├── 2466888
# ...
└── 2467085

198 directories, 0 files

# Inside a single bins directory
$ tree bins/2466887/
bins/2466887/
├── bin.1.fa
├── bin.2.fa
└── bin.3.fa

0 directories, 3 files
```

---

## Files

### `previous_classifications.csv`

The simulated metagenomes have previously been classified by the following tools:

* DeepVirFinder
* MARVEL
* MetaPhinder
* Seeker
* VIBRANT
* viralVerify
* VirFinder
* VirSorter
* VirSorter2

Those classifications are present in the file `previous_classifications.csv`. This file contains a row per contig, with the following columns:

* `metagenome`: Metagenome number (*e.g.* 2466958)
* `record`: Contig number. Unique within each metagenome
* `dvf` - `VirSorter2`: Columns for each tool

---

### `previous_resource_usage.csv`

During classification of the metagenomes by the tools, resource usage was tracked by Snakemake, those results are compiled in `previous_resource_usage.csv`. Each row represents the resource usage while classifying a single metagenome.

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
tool | string | Metagenom detection tool
metagenome| string | Metagenom name


---

### `assembly.fa`

Each `assembly.fa` file is a FASTA structured file. The headers give taxonomic information about each contig.

```sh
$ head -n 2 assemblies/2466887/assembly.fa
>SAMEA2466887-ContigCoA-k113_2
AAAATCTAATGTATTATTTTCTCTTTCTATTTTTATATTTAAGTCTTCACCTTTTGATTT
# ...

# Each record starts with a ">"
$ grep ">" assemblies/2466887/assembly.fa | wc -l
138439
```

These files were classified by all tools except MARVEL.

---

### `bin.*.fa`

Each bin directory contains files of binned contigs, named as `bin.*.fa`, each of which is a FASTA file.

```sh
head -n 2 bins/2466887/bin.1.fa
>SAMEA2466887-ContigCoA-k113_127722
ACGGCTCTCTCACCTGCAGCCATAACACCCATATGTCCACCAAGACATGGTCCACAGGTA
# ...
```

The bins were classified by MARVEL.

---

### `checkv_quality_summary.csv`

The results of running CheckV on all contigs are present in `checkv_quality_summary.csv`. Each row represents a contig and is uniquely identified by the column `contig_id`. More information about CheckV can be found at (https://bitbucket.org/berkeleylab/checkv/src/master/). In the original publication `checkv_quality` was used for evaluation of contigs that were predicted by the tools.

The columns are as follows (with my understanding of column meanings, refer to official docs for clarity):

* `contig_id`: Contig ID
* `contig_length`: Contig length (bp)
* `provirus`: Boolean indicating provirus ("Yes" or "No")
* `proviral_length`: Length of proviral sequence
* `gene_count`: Total number of genes
* `viral_genes`: Number of viral genes
* `host_genes`: Number of host genes
* `checkv_quality`: Predicted viral quality ("Not-determined", "Low-quality", "Medium-quality", "High-quality", or "Complete")
* `miuvig_quality`
* `completeness`
* `completeness_method`
* `contamination`
* `kmer_freq`
* `warnings`
* `sample`: Sample number, as those in `assemblies/` and `bins/`
