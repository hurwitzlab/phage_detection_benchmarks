#!/usr/bin/env python3
"""
Author : Kenneth Schackart <schackartk1@gmail.com>
Date   : 2021-10-08
Purpose: Post processing tool predictions
"""

import argparse
import numpy as np
import os
import pandas as pd
from typing import NamedTuple, TextIO


class Args(NamedTuple):
    """ Command-line arguments """
    file: TextIO
    out_dir: str
    length: int
    actual: str
    tool: str


# --------------------------------------------------
def get_args() -> Args:
    """ Get command-line arguments """

    parser = argparse.ArgumentParser(
        description='Post processing for tool predictions',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('file',
                        help='Classification output',
                        metavar='FILE',
                        type=argparse.FileType('rt'),
                        default=None)

    parser.add_argument('-o',
                        '--out_dir',
                        help='Output directory',
                        metavar='str',
                        type=str,
                        default='out')

    parser.add_argument('-l',
                        '--length',
                        help='Length of fragments',
                        metavar='LENGTH',
                        type=int,
                        choices=[500, 1000, 3000, 5000],
                        required=True)

    parser.add_argument('-a',
                        '--actual',
                        help='True classification',
                        metavar='CLASS',
                        type=str,
                        choices=['archaea', 'bacteria', 'fungi', 'viral'],
                        required=True)

    parser.add_argument('-t',
                        '--tool',
                        help='Classifier tool',
                        metavar='TOOL',
                        type=str,
                        choices=['dvf', 'seeker'],
                        required=True)

    args = parser.parse_args()

    return Args(args.file, args.out_dir, args.length, args.actual, args.tool)


# --------------------------------------------------
def main() -> None:
    """ Do the stuff """

    # Parse rguments
    args = get_args()
    tool = args.tool
    out_dir = args.out_dir

    # Reformat based on tool
    reformatted = reformatters[tool](args)

    # Reorder columns
    cols = [
        'record', 'length', 'actual', 'prediction', 'lifecycle', 'value',
        'stat', 'stat_name'
    ]
    final_df = reformatted[cols]

    # Dataframe write operattions
    if not os.path.isdir(out_dir):
        os.mkdir(out_dir)

    out_file = os.path.join(out_dir, f'{tool}_pred_formatted.csv')

    with open(out_file, 'wt') as out:
        final_df.to_csv(out, index=False)

    print(f'Done. Wrote to {out_file}')


# --------------------------------------------------
def reformat_dvf(args: Args):
    """ Reformat DeepVirFinder output """

    raw_df = pd.read_csv(args.file, sep='\t')

    # Rename columns that are present
    df = raw_df.rename(
        {
            'name': 'record',
            'len': 'length',
            'score': 'value',
            'pvalue': 'stat'
        },
        axis='columns')

    # Shorten record to just ID
    df['record'] = df['record'].str.split().str.get(0)

    # Add prediction column
    df['prediction'] = np.where(df['value'] < 0.5, 'non-viral', 'viral')

    # Add constant columns
    index_range = range(len(df.index))
    df['actual'] = pd.Series([args.actual for x in index_range])
    df['stat_name'] = pd.Series(['p' for x in index_range])
    df['lifecycle'] = pd.Series([None for x in index_range])

    return df


# --------------------------------------------------
def reformat_seeker(args: Args):
    """ Reformat Seeker output """

    raw_df = pd.read_csv(args.file, sep='\t')

    # Rename columns that are present
    df = raw_df.rename({'name': 'record', 'score': 'value'}, axis='columns')

    # Lower case predictions column
    df['prediction'] = df['prediction'].str.lower()

    # Add constant columns
    index_range = range(len(df.index))
    df['length'] = pd.Series([args.length for x in index_range])
    df['actual'] = pd.Series([args.actual for x in index_range])

    # Add empty columns
    df['stat'] = pd.Series([None for x in index_range])
    df['stat_name'] = pd.Series([None for x in index_range])
    df['lifecycle'] = pd.Series([None for x in index_range])

    return df


reformatters = {'dvf': reformat_dvf, 'seeker': reformat_seeker}

# --------------------------------------------------
if __name__ == '__main__':
    main()
