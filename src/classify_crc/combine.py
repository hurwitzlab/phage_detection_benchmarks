#!/usr/bin/env python3
"""
Author : Kenneth Schackart <schackartk1@gmail.com>
Date   : 2021-10-12
Purpose: Combine all predictions from a tool
"""

import argparse
import os
import pandas as pd
from typing import List, NamedTuple, TextIO


class Args(NamedTuple):
    """ Command-line arguments """
    files: List[TextIO]
    out_dir: str


# --------------------------------------------------
def get_args() -> Args:
    """ Get command-line arguments """

    parser = argparse.ArgumentParser(
        description='Combine all predictions from a tool',
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
    """ Make a jazz noise here """

    args = get_args()
    out_dir = args.out_dir

    # Rows of combined dataframe
    rows: List = []

    out_df = pd.DataFrame()

    # Get rows of new dataframe
    for file in args.files:

        new_df = pd.read_csv(file)
        out_df = pd.concat([out_df, new_df])

        # file_header = file.readline()

        # rows.extend(
        #     map(lambda l: str.split(l.rstrip(), sep=','), file.readlines()))

    # Move to dataframe
    # combined_df = pd.DataFrame(rows)

    # # Add header
    # combined_df.columns = file_header.rstrip().split(',')

    # Dataframe write operattions
    if not os.path.isdir(out_dir):
        os.mkdir(out_dir)

    out_file = os.path.join(out_dir, 'combined.csv')

    with open(out_file, 'wt') as out:
        out_df.to_csv(out, index=False)

    print(f'Done. Wrote to {out_file}')


# --------------------------------------------------
if __name__ == '__main__':
    main()
