# Select Genome Fragments

Here are the scripts for using the [selector.py](https://github.com/schackartk/challenging-phage-finders/tree/main/src/data_selection) script to select random fragments from the chopped genomes.

This includes providing a `run.slurm` script, a `Snakefile`, and `config` files.

## Usage

```
snakemake -j 16 --configfile config/config.yaml
```

## Making Changes

The Snakefile should not need to be changed, since all mutable things should be stored in the `config` files. Accordingly, the Snakefile was refined using the practice data located in the selector.py tests directry.

# Problems

Right now I cannot get it to run as a cluster

## What does work

Destination directory is initially empty.

```console
$ ls ../../data/selected_frags/

```

Run Snakemake with 16 threads on interactive

```console
$ conda activate snakemake_env

$ snakemake -j 16 --configfile config/practice_config.yaml

Building DAG of jobs...
Using shell: /usr/bin/bash
Provided cores: 16
Rules claiming more threads will be scaled down.
Job stats:
job             count    min threads    max threads
------------  -------  -------------  -------------
all                 1              1              1
select_frags       16              1              1
total              17              1              1

Select jobs to execute...

[Thu Sep 16 13:57:45 2021]
rule select_frags:
    input: ../data_selection/tests/inputs/chopped/archaea/10
    output: ../../data/selected_frags/archaea/10/selected_frags.fasta
    jobid: 2
    wildcards: kingdom=archaea, length=10
    resources: tmpdir=/tmp

# ...

[Thu Sep 16 13:57:58 2021]
Finished job 0.
17 of 17 steps (100%) done
Complete log: /xdisk/bhurwitz/mig2020/rsgrps/bhurwitz/schackartk/projects/phage_finders/src/select_frags/.snakemake/log/2021-09-16T135745.055809.snakemake.log
```

Now all the output files are there:

```console
$ tree ../../data/selected_frags/
../../data/selected_frags/                                                                                                                                                 |-- archaea
    |   |-- 10
    |   |   `-- selected_frags.fasta
    |   |-- 30
    |   |   `-- selected_frags.fasta
    |   |-- 5
    |   |   `-- selected_frags.fasta
    |   `-- 50
    |       `-- selected_frags.fasta
    |-- bacteria
    |   |-- 10
    |   |   `-- selected_frags.fasta
    |   |-- 30
    |   |   `-- selected_frags.fasta
    |   |-- 5
    |   |   `-- selected_frags.fasta
    |   `-- 50
    |       `-- selected_frags.fasta
    |-- fungi
    |   |-- 10
    |   |   `-- selected_frags.fasta
    |   |-- 30
    |   |   `-- selected_frags.fasta
    |   |-- 5
    |   |   `-- selected_frags.fasta
    |   `-- 50
    |       `-- selected_frags.fasta
    `-- viral
        |-- 10
        |   `-- selected_frags.fasta
        |-- 30
        |   `-- selected_frags.fasta
        |-- 5
        |   `-- selected_frags.fasta
        `-- 50
            `-- selected_frags.fasta
            
20 directories, 16 files 
```

## What is not working

First, I will clean out those output files.

```console
$ rm -rf ../../data/selected_frags/

$ mkdir ../../data/selected_frags

$ ls ../../data/selected_frags

```

Now, running as --cluster.

*Note* I also have a version where I use a cluster.yaml file, but just so it is clear what is being run, I ran it explicitly

```console
snakemake --cluster "sbatch -p windfall -t 00:05:00 --mem-per-cpu=5gb --nodes=1 --ntasks=5 -e err/{rule}/{wildcards}.err -o out/{rule}/{wildcards}.out" -j 16 --latency-wait 15 --configfile config/practice_config.yaml
Building DAG of jobs...
Using shell: /usr/bin/bash
Provided cluster nodes: 16
Job stats:
job             count    min threads    max threads
------------  -------  -------------  -------------
all                 1              1              1
select_frags       16              1              1
total              17              1              1

Select jobs to execute...

[Thu Sep 16 14:13:24 2021]
rule select_frags:
    input: ../data_selection/tests/inputs/chopped/fungi/5
    output: ../../data/selected_frags/fungi/5/selected_frags.fasta
    jobid: 9
    wildcards: kingdom=fungi, length=5
    resources: tmpdir=/tmp
    
Submitted job 9 with external jobid 'Submitted batch job 2075510'.

# ...
```

All 16 jobs are submitted like that, and it just waits.

Going to another terminal and checking my queue shows the 16 jobs in queue, then slowly dwindling off. Until just my interactive session is still running.

Even still, the output directory is empty

```console
$ ls ../../data/selected_frags

```

Clearly, the individual jobs are "completing", but they are not generating any output. Yet Snakemake doesn't quit, even though the rules are not actually generating their targets.

Also, the output to terminal, and the log file, have nothing about `X/17 (X%) done`, unlike when it is ran not as cluster.

There are no errors generated. Nothing is written to `out/` or `err/`. And the snakemake process doesn't die, I have to interrupt it. No errors are present in the log except that I killed it manually.

## What else I have tried

* Originally, I ran this using a SLURM script, and using a config/cluster.yaml type file. But I figured running bare in interactive is the best way to trace down an issue.
* I have tried on both standard and windfall, same results
* I tried removing the `--configfile` argument to make sure that would fail then. It did.

I am really unsure what else to check. I am running this pretty much the same way as I run my chopper, except that of course uses a SLURM file and config file. But the `snakemake --cluster` command is nearly identical.
