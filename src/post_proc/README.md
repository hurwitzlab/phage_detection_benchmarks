# Predictions Post Processing

Scripts for converting the files containing predictions from the various tools into a uniform format.

## Standard Output Format

The format that all predictions is:

| record | length | actual | prediction | value | stat | stat_name |
| ------ | ------ | ------ | ---------- | ----- | ---- | --------- |
frag_x   | 500    | viral  | viral      | 0.23  | 0.03 | p         |
frag_y   | 3000   | viral  | bacteria   | 0.87  |      |           |

* `record`: record ID (produced by chopper.py, *e.g.* frag_7116_NZ_CP010595.1)

* `length`: fragment length

* `actual`: True origin

* `prediction`: predicted classification. Helpful sanity check in case inconsistency in how `value` relates to classification among tools. May not be given by tool, in which case it will be added during post-processing based on `value`.

* `value`: value on which prediction is made. *e.g.* $P(viral)$. Interpretation may vary based on tool, or may not be given.

* `stat`: any associated statistic, especially regarding confidence in classification. If not given by tool, it is not inferred.

* `stat_name`: name of `stat`, such as $p$-value