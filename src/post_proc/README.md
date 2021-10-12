# Predictions Post Processing

Scripts for converting the files containing predictions from the various tools into a uniform format.

## Usage

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

## Standard Output Format

Output will be csv file.

| record | length | actual | prediction | lifecycle | value | stat | stat_name |
| ------ | ------ | ------ | ---------- | --------- | ----- | ---- | --------- |
frag_x   | 500    | viral  | viral      | prophage  | 0.23  | 0.03 | p         |
frag_y   | 3000   | viral  | bacteria   |           | 0.87  |      |           |

* `record`: record ID (produced by chopper.py, *e.g.* frag_7116_NZ_CP010595.1). Not the full name and description.

* `length`: fragment length

* `actual`: True origin. When classifying fragments, fragments passed to the classifiers are of only 1 classification, so all results in a file have common true classification.

* `prediction`: predicted classification. Helpful sanity check in case inconsistency in how `value` relates to classification among tools. May not be given by tool, in which case it will be added during post-processing based on `value`.

* `lifecycle`: when predicted as viral, prediction of prophage or lytic.

* `value`: value on which prediction is made. *e.g.* $P(viral)$. Interpretation may vary based on tool, or may not be given.

* `stat`: any associated statistic, especially regarding confidence in classification. If not given by tool, it is not inferred.

* `stat_name`: name of `stat`, such as $p$-value