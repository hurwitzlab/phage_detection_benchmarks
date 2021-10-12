#!/usr/bin/env python3
"""
Author : Kenneth Schackart <schackartk1@gmail.com>
Date   : 2021-10-12
Purpose: Combine all predictions from a tool
"""

import argparse
import os
import pandas as pd
from typing import NamedTuple, TextIO


class Args(NamedTuple):
    """ Command-line arguments """
    files: list[TextIO]
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
    
    rows = []

    for file_num, file in enumerate(args.files, start=1):
        start = 0 if file_num == 1 else 1
        
        rows.extend(map(lambda l: str.split(l.rstrip(), sep=','),
                        file.readlines()[start:]))

    # Create header
    col_names = rows[0]
    
    # Move to dataframe
    combined_df = pd.DataFrame(rows[1:])

    # Add header
    combined_df.columns = col_names

    # Dataframe write operattions
    if not os.path.isdir(out_dir):
        os.mkdir(out_dir)

    out_file = os.path.join(out_dir, 'combined.csv')

    with open(out_file, 'wt') as out:
        combined_df.to_csv(out, index=False)

    print(f'Done. Wrote to {out_file}')



# --------------------------------------------------
if __name__ == '__main__':
    main()
