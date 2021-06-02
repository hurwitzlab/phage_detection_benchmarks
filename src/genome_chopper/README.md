# genome_chopper

Create simulated assemblies from reference genome by chopping.

## Motivation

The effect of read errors on phage identification tools will be assessed through read simulation methods, such as with [InSilicoSeq](https://github.com/HadrienG/InSilicoSeq). However, we would also like to assess the effect of contig assembly size directly.

To achieve this, we can cut the genome into smaller substrings, which would be analogous to contigs assembled from reads.

## Method

The genome is input as FASTA file. Genome is then cut into small, overlapping pieces. These chopped genomes are output.

# Usage

```console
$ ./chopper.py

usage: chopper.py [-h] [-o DIR] [-l INT] [-v INT] FILE [FILE ...]

Chop a genome into simulated contigs

positional arguments:
  FILE                  Input DNA file(s), each with only 1 record

optional arguments:
  -h, --help            show this help message and exit
  -o DIR, --out_dir DIR
                        Output directory (default: out)
  -l INT, --length INT  Segment length (b) (default: 100)
  -v INT, --overlap INT
                        Overlap length (b) (default: 10)
```