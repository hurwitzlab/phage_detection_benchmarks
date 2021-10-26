# Predictions Post Processing

Helpers for cleaning up after classifying chopped genome fragments. They are originally written to be used in the pipeline located in [src/classify_chopped](https://github.com/schackartk/challenging-phage-finders/tree/main/src/classify_chopped). Some scripts may be more broadly usable, but may need to be revised.

There are 3 scripts here:

* `reformat.py`: Convert the files containing predictions from the various tools into a uniform format
* `combine.py`: Merge the formatted files into single file
* `benchmark.py`: Merge the Snakemake benchmark output files

## `reformat.py`

Script for converting the files containing predictions from the various tools into a uniform format.

### Usage

```
$ ./reformat.py --help
usage: reformat.py [-h] [-o str] -l LENGTH -a CLASS -t TOOL FILE

Post processing for tool predictions

positional arguments:
  FILE                  Classification output

optional arguments:
  -h, --help            show this help message and exit
  -o str, --out_dir str
                        Output directory (default: out)
  -l LENGTH, --length LENGTH
                        Length of fragments (default: None)
  -a CLASS, --actual CLASS
                        True classification (default: None)
  -t TOOL, --tool TOOL  Classifier tool (default: None)
```

### Standard Output Format

Output will be csv file.

| record | length | actual | prediction | lifecycle | value | stat | stat_name |
| ------ | ------ | ------ | ---------- | --------- | ----- | ---- | --------- |
frag_x   | 500    | viral  | viral      | prophage  | 0.23  | 0.03 | p         |
frag_y   | 3000   | viral  | bacteria   |           | 0.87  |      |           |
frag_i   | 500    | viral  | viral      | lytic     | 0.11  | 0.01 | p         |
frag_j   | 1000   | viral  | bacteria   |           | 0.69  |      |           |

* `record`: record ID (produced by chopper.py, *e.g.* frag_7116_NZ_CP010595.1). Not the full name and description.

* `length`: fragment length

* `actual`: True origin. When classifying fragments, fragments passed to the classifiers are of only 1 classification, so all results in a file have common true classification.

* `prediction`: predicted classification. Helpful sanity check in case inconsistency in how `value` relates to classification among tools. May not be given by tool, in which case it will be added during post-processing based on `value`.

* `lifecycle`: when predicted as viral, prediction of prophage or lytic.

* `value`: value on which prediction is made. *e.g.* $P(viral)$. Interpretation may vary based on tool, or may not be given.

* `stat`: any associated statistic, especially regarding confidence in classification. If not given by tool, it is not inferred.

* `stat_name`: name of `stat`, such as $p$-value

## `combine.py`

Combine the reformatted prediction files. Since the reformatting adds columns containing information about the run (*e.g.* tool, length, *etc.*) it is safe to merge the reformatted files from many or all prediction jobs.

This is how it is intended to be used in Snakemake, where the `rule all:` calls for a `combined.csv` file, which has merged all predictions from all tools, kingdoms, and lengths.

### Usage

```
$ ./combine.py -h
usage: combine.py [-h] [-o DIR] FILE [FILE ...]

Combine all predictions from a tool

positional arguments:
  FILE                  Files to be merged

optional arguments:
  -h, --help            show this help message and exit
  -o DIR, --out_dir DIR
                        Output directory (default: out)
```

## `benchmark.py`

Merge the benchmark output files from Snakemake. This script is very sensitive to how the files are named since it infers metadata from the name.

Files names should contain the following pattern: *tool*/*kingdom*_*length*_benchmark.txt. This is determined by the `benchmark:` argument in the Snakemake rules.

### Usage

```
$ ./benchmark.py -h
usage: benchmark.py [-h] [-o DIR] FILE [FILE ...]

Combine Snakemake benchmark files

positional arguments:
  FILE                  Files to be merged

optional arguments:
  -h, --help            show this help message and exit
  -o DIR, --out_dir DIR
                        Output directory (default: out)
```

*Note*: At this time, the file name is being parsed for the pattern shown above. Columns for each of the italicized fields are added for each row of the new combined file. It may be more generally useful if instead the file name was simply added to the combined dataframe, and parsing out metadata were performed during analysis instead.