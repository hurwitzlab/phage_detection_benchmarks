# Metagenomic Phage Detection Benchmarking Datasets
# Set 3: *Simulated metagenomes*

## Description

This dataset contains a total of 1,149,408 contigs assembled from simulated reads, simulated using 3 error models, and based on 5 marine metagenomic abundance profiles. The following is the breakdown of the number of contigs.

Error Model | SRR4831655 | SRR4831664 | SRR5720259 | SRR5720320 | SRR6507280
| :-------: | :--------: | :--------: | :--------: | :--------: | :--------: |
HiSeq       | 30,806     | 30,869     | 14,050     | 14,603     | 13,834
MiSeq       | 328,243    | 234,764    | 64,454     | 144,859    | 134,453
NovaSeq     | 42,881     | 40,366     | 16,052     | 21,087     | 18,087

The five abundance profiles used for simulation come from marine metagenomes obtained from SRA. SRR4831655 and SRR4831664 are from study PRJNA237344; the other three are from study PRJNA385855. Bacterial and phage population abundance profiles were obtained using Kraken2 and Bracken. Phage content was supplemented to include a value of 5% phage. 2M paired-end reads were generated using InSilicoSeq based on the 5 abundance profiles, and using the 3 built-in error models (HiSeq, MiSeq, and NovaSeq). Simulated reads were assembled with MegaHit v1.2.9 with a minimum contig length of 1000 bp. Contigs assembled from simulated reads were also binned with MetaBAT 2 v2:2.15 and using Bowtie2 v2.4.5 for indexing. The following number of bins were created.

Error Model | SRR4831655 | SRR4831664 | SRR5720259 | SRR5720320 | SRR6507280
| :-------: | :--------: | :--------: | :--------: | :--------: | :--------: |
HiSeq       | 22         | 23         | 16         | 16         | 19
MiSeq       | 38         | 33         | 24         | 22         | 20
NovaSeq     | 25         | 24         | 18         | 19         | 23

The metagenomes were classified with the classifiers, and those results are present here. During classification, resource usage was also recorded, and are present.

In the original publication, simulated metagenomes were relabeled to not be confused with the real metagenomes, however the original names are retained here for clarity. The following is how they were mapped in the original publication:

   Original | SRR4831655 | SRR4831664 | SRR5720259 | SRR5720320 | SRR6507280
| :-------: | :--------: | :--------: | :--------: | :--------: | :--------: |
Simulated   | Profile 1  | Profile 2  | Profile 3  | Profile 4  | Profile 5  |

---

## Structure

The top level structure is as follows:

```sh
$ tree -L 1
.
├── assemblies                   # Assembled simulated reads
├── bins                         # Binned assemblies
├── contig_identities.csv        # Taxonomic origin of contigs
├── previous_classifications.csv # Classified metagenomes
├── previous_resource_usage.csv  # Resources used during classification
└── README.md

2 directories, 4 files
```

---

## Directories

There are two directories: `assemblies/` and `bins/`:

```sh
$ tree assemblies/
assemblies/
├── SRR4831655_hiseq
│   └── assembly.fa
├── SRR4831655_miseq
│   └── assembly.fa
├── SRR4831655_novaseq
│   └── assembly.fa
├── SRR4831664_hiseq
│   └── assembly.fa
# ...
└── SRR6507280_novaseq
    └── assembly.fa

15 directories, 15 files

# Top level structure in bins/
$ tree bins/ -L 1
bins/
├── SRR4831655_hiseq
├── SRR4831655_miseq
├── SRR4831655_novaseq
├── SRR4831664_hiseq
# ...
└── SRR6507280_novaseq

15 directories, 0 files

# Inside a single bins directory
$ tree bins/SRR6507280_miseq/
bins/profile_2_miseq/
├── bin.10.fa
├── bin.11.fa
#...
└── bin.9.fa

0 directories, 20 files
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

Those classifications are present in the file `previous_classifications.csv`. Output from the original tools has already been cleaned, organized into a consistent manny, and compiled into this single file. The following columns are present:

* `tool`: Phage detection tool (*e.g.* DeepVirFinder)
* `metagenome`: metagenome (*e.g.* profile_1_hiseq)
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
metagenome| string | metagenome name


---

### `assembly.fa`

Each `assembly.fa` file is a FASTA structured file. The headers give taxonomic information about each genome fragment.

```sh
$ head -n 2 assemblies/SRR6507280_miseq/assembly.fa
>k141_53487 flag=1 multi=1.0000 len=500                                                                                 TGTGCCTTCCATTGACATCTATTGTAGCTATTAGGTTATCCACCTTATTTGCCGACGCGTACATGATTGCTTCCCATATTTGCCCCTCTTGAATTTCGCATCCCCGTGTAGGCTAAATACCAATCTTTCGTCTCCATTTATTTTTTTCGATAGAGCTGCTCCAATAGCTACAGACATGCCTTGTCCTAGAGAT
# ...

# Each record starts with a ">"
$ grep ">" assemblies/SRR6507280_miseq/assembly.fa | wc -l
134453
```

These files were classified by all tools except MARVEL.

---

### `bin.*.fa`

Each bin directory contains files of binned contigs, named as `bin.*.fa`, each of which is a FASTA file.

```sh
head -n 2 bins/SRR6507280_miseq/bin.1.fa
>k141_201389
ATACCGCCCAAGAGTTCATATCGACGGCGGTGTTTGGCACCTCGATGTCGGCTCATCACA
# ...
```

The bins were classified by MARVEL.

---

### `contig_identities.csv`

The true identities of the contigs in each metagenome were obtained by running a BLAST search against a database composed of the phage genomes used for simulation of that particular metagenome. Based on the accession number of the BLAST matches, TaxIDs were retrieved, and further taxonomic information was obtained using the R package taxonomizr. These results are present in the file `contig_identities.csv`.

The file contains the following columns:

* `profile`: metagenome profile
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
