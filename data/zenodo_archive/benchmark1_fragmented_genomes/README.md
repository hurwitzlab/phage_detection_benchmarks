# Metagenomic Phage Detection Benchmarking Datasets
# Set 1: *Fragmented genomes*

## Description

This dataset contains a total of 160,000 Refseq reference genome fragments (10,000 * 4 taxa * 4 lengths).

length (nt) | archaea | bacteria | fungi | viruses
| ---------: | :-----: | :------: | :---: | :-----:
500         | 10k     | 10k      | 10k   | 10k
1,000       | 10k     | 10k      | 10k   | 10k
3,000       | 10k     | 10k      | 10k   | 10k
5,000       | 10k     | 10k      | 10k   | 10k

Sequences were created by fragmenting reference genomes from RefSeq. All reference genomes were downloaded before 20 July 2021. Reference genomes were fragmented into adjacent non-overlapping fragments of lengths 500, 1000, 3000, and 5000 nt. 10,000 fragments per taxon/length were selected by 1) randomly selecting genomes, then 2) randomly selecting a fragment from that genome. When fewer than 10k genomes were present, genomes were selected with replacement. If a genome fragment wa already selected, it was discarded and another was selected, making genome fragments within a set unique.

The genome fragments were classified with the classifiers, and those results are present here. During classification, resource usage was also recorded, and are present.

## Structure

The top level structure is as follows:

```sh
$ tree -L 1
.
├── archaea/                     # Fragmented archaeal genomes
├── bacteria/                    # Fragmented bacterial genomes
├── fungi/                       # Fragmented fungal genomes
├── previous_classifications.csv # Classified fragments
├── previous_resource_usage.csv  # Resources used during classification
├── README.md
└── viruses/                     # Fragmented viral genomes

4 directories, 3 files
```

## Directories

Each of the 4 directories have similar internal structure:

```sh
$ tree archaea/
archaea/
├── 1000                    # 1000 nt fragments 
│   └── genome_fragments.fa # File with 10k fragments
├── 3000                    # 3000 nt fragments
│   └── genome_fragments.fa # File with 10k fragments
├── 500                     # 500 nt fragments
│   └── genome_fragments.fa # File with 10k fragments
└── 5000                    # 5000 nt fragments
    └── genome_fragments.fa # File with 10k fragments
4 directories, 4 files
```

There are 4 sub-directories, each corresponding to a certain fragment length. Within those directories are files called `genome_fragments.fa` which are FASTA files of 10,000 reference genome fragments.

These FASTA files are the input to the phage detection tools.

## Files

### `previous_classifications.csv`

All fragments have previously been classified by the following tools:

* DeepVirFinder
* MetaPhinder
* Seeker
* VIBRANT
* viralVerify
* VirFinder
* VirSorter
* VirSorter2

Those classifications are present in the file `previous_classifications.csv`. Output from the original tools has already been cleaned, organized into a consistent manny, and compiled into this single file. The following columns are present:

* `tool`: Phage detection tool (*e.g.* DeepVirFinder)
* `record`: Fragment ID (*e.g.* frag_1227_NC_009033.1, which indicates it is fragment number 1227 from the organism with accession NC_009033.1)
* `length`: Fragment length
* `actual`: Actual identity; one of "archaea", "bacteria", "fungi", or "viral"
* `prediction`: Predicted identity, which has been grouped into "viral" or "non-viral"
* `lifecycle`: Lifecycle prediction (*e.g.* lytic or prophage) if given by tool
* `value`: Value upon which prediction is made, when given by tool
* `stat`: Statistic (*e.g.* p-value), when given by tool
* `stat_name`: Name of statistic in `stat` column

There may not be a row for each fragment for each tool. Missing observations come from tools that only create output for predicted viruses, so missing observation indicate a "non-viral" prediction.

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
taxon | string | Reference genome taxon
length | integer | Genome fragment length

### `genome_fragments.fa`

Each `genome_fragments.fa` file is a FASTA structured file. The headers give taxonomic information about each genome fragment.

```sh
$ head -n 3 archaea/1000/genome_fragments.fa
>frag_614_NC_009033.1 Fragment 614 of NC_009033.1 Staphylothermus marinus F1, complete sequence
GCATATCCTATGATATCGGATATTCTCGTAAATCCTTTCTCTTCCATATACTTCTTGATA
CCATCAAGTATATTGTTTACTATATTGTATCCAACCATGTAGAATCCTGTACCTATTTGA

# Each record starts with a ">"
$ grep ">" archaea/1000/genome_fragments.fa | wc -l
10000
```
