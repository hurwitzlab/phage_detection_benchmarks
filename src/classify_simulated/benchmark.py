#!/usr/bin/env python3
"""
Author : Kenneth Schackart <schackartk1@gmail.com>
Date   : 2021-10-25
Purpose: Combine Snakemake benchmark files
"""

import argparse
import os
import pandas as pd
import re
import sys
from typing import List, NamedTuple, TextIO


class Args(NamedTuple):
    """ Command-line arguments """
    files: List[TextIO]
    out_dir: str


# --------------------------------------------------
def get_args() -> Args:
    """ Get command-line arguments """

    parser = argparse.ArgumentParser(
        description='Combine Snakemake benchmark files',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('files',
                        metavar='FILE',
                        help='Files to be merged',
                        type=argparse.FileType('rt'),
                        nargs='+')

    parser.add_argument('-o',
                        '--out_dir',
                        metavar='DIR',
                        help='Output directory',
                        type=str,
                        default='out')

    args = parser.parse_args()

    return Args(args.files, args.out_dir)


# --------------------------------------------------
def main() -> None:
    """ Do the stuff """

    args = get_args()
    out_dir = args.out_dir

    # Assumed column names for combining dataframes
    old_header = ('s\th:m:s\tmax_rss\tmax_vms\tmax_uss\t'
                  'max_pss\tio_in\tio_out\tmean_load\tcpu_time\n')

    # Assumed benchmark file naming convention regex
    # {tool}/{kingdom}_{length}_benchmark.txt
    name_re = re.compile(
        r'(?P<tool>\w+)/(?P<kingdom>\w+)_(?P<length>\d+)_benchmark.txt')

    # Rows of combined dataframe
    # Using list first instead of dataframe for speed
    rows: List = []

    # Get rows of new dataframe
    for file in args.files:

        file_header = file.readline()

        if file_header != old_header:
            sys.exit(f'File {file.name}: unexpected column names.')

        # Match the file name to get information about rule that produced file
        name_match = name_re.search(file.name)

        # Die if info cannot be inferred
        if not name_match:
            sys.exit(f'File {file.name}: unexpected file name.\n'
                     'Consistency needed for inferring meta information.\n'
                     'Expected {tool}/{kingdom}_{length}_benchmark.txt')

        # Add new row to merged df (list at this time)
        rows.extend(
            map(lambda l: str.split(l.rstrip(), sep='\t'), file.readlines()))

        # Add inferred information about rule
        rows[-1].extend(list(name_match.group('tool', 'kingdom', 'length')))

    # Move to dataframe
    combined_df = pd.DataFrame(rows)

    # Define new header with new rows
    # Remove previous newline first
    new_header = old_header[:-1] + '\ttool\tkingdom\tlength\n'

    # Add header
    combined_df.columns = new_header.rstrip().split('\t')

    # Dataframe write operattions
    if not os.path.isdir(out_dir):
        os.mkdir(out_dir)

    out_file = os.path.join(out_dir, 'combined_benchmarks.csv')

    with open(out_file, 'wt') as out:
        combined_df.to_csv(out, index=False)

    print(f'Done. Wrote to {out_file}')


# --------------------------------------------------
if __name__ == '__main__':
    main()
