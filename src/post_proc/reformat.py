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
from typing import List, NamedTuple, TextIO


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
                        choices=[
                            'breadsticks', 'dvf', 'metaphinder', 'seeker',
                            'vibrant', 'viralverify', 'virfinder', 'virsorter',
                            'virsorter2'
                        ],
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
        'tool', 'record', 'length', 'actual', 'prediction', 'lifecycle',
        'value', 'stat', 'stat_name'
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
def reformat_breadsticks(args: Args):
    """ Reformat Unlimited breadsticks output """

    raw_df = pd.read_csv(args.file, sep='\t')

    df = raw_df.rename({
        'ORIGINAL_NAME': 'record',
        'LENGTH': 'length'
    },
                       axis='columns')

    index_range = range(len(df.index))

    # Remove extra columns
    df = df.drop(columns=[
        'CENOTE_NAME', 'END_FEATURE', 'NUM_HALLMARKS', 'HALLMARK_NAMES'
    ])

    # Only records with viral hallmark genes are retained
    # So all records present have been predicted as viral
    df['prediction'] = pd.Series(['viral' for x in index_range], dtype=str)

    # Add constant columns
    df['tool'] = pd.Series([args.tool for x in index_range], dtype=str)
    df['actual'] = pd.Series([args.actual for x in index_range], dtype=str)
    df['lifecycle'] = pd.Series([None for x in index_range], dtype=str)
    df['value'] = pd.Series([None for x in index_range], dtype=str)
    df['stat'] = pd.Series([None for x in index_range], dtype=str)
    df['stat_name'] = pd.Series([None for x in index_range], dtype=str)

    return df


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
    df['tool'] = pd.Series([args.tool for x in index_range])
    df['actual'] = pd.Series([args.actual for x in index_range])
    df['stat_name'] = pd.Series(['p' for x in index_range])
    df['lifecycle'] = pd.Series([None for x in index_range])

    return df


# --------------------------------------------------
def reformat_metaphinder(args: Args):
    """ Reformat MetaPhinder output """

    raw_df = pd.read_csv(args.file, sep='\t')

    # Rename columns that are present
    df = raw_df.rename(
        {
            '#contigID': 'record',
            'classification': 'prediction',
            'ANI [%]': 'value',
            'size[bp]': 'length'
        },
        axis='columns')

    # Rework predictions
    df['prediction'] = np.where(df['prediction'] == 'negative', 'non-viral',
                                'viral')

    # Add constant columns
    index_range = range(len(df.index))
    df['tool'] = pd.Series([args.tool for x in index_range])
    df['actual'] = pd.Series([args.actual for x in index_range])
    df['lifecycle'] = pd.Series([None for x in index_range])
    df['stat'] = pd.Series([None for x in index_range])
    df['stat_name'] = pd.Series([None for x in index_range])

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
    df['tool'] = pd.Series([args.tool for x in index_range])
    df['length'] = pd.Series([args.length for x in index_range])
    df['actual'] = pd.Series([args.actual for x in index_range])

    # Add empty columns
    df['stat'] = pd.Series([None for x in index_range], dtype=str)
    df['stat_name'] = pd.Series([None for x in index_range], dtype=str)
    df['lifecycle'] = pd.Series([None for x in index_range], dtype=str)

    return df


# --------------------------------------------------
def reformat_vibrant(args: Args):
    """ Reformat vibrant output """

    # Read in the file
    seqs: List = args.file.readlines()

    df = pd.DataFrame(seqs, columns=['seq'])

    # Extract sequence ID
    # 1 or more [alphanumeric or .] followed by one whitespace
    # pylint: disable=unsupported-assignment-operation
    df['record'] = df['seq'].str.extract(r'(?P<sequence>[\w.]+)[\s]')

    # Label prophages, as they will have _fragment_ in the name
    df['lifecycle'] = np.where(df['seq'].str.contains(r'_fragment_'),
                               'prophage', 'lytic')

    # Remove unused columns
    df = df.drop(columns=['seq'])

    # Add constant columns
    index_range = range(len(df.index))
    df['tool'] = pd.Series([args.tool for x in index_range], dtype=str)
    df['length'] = pd.Series([args.length for x in index_range], dtype=str)
    df['actual'] = pd.Series([args.actual for x in index_range], dtype=str)
    df['prediction'] = pd.Series(['viral' for x in index_range], dtype=str)

    # Add empty columns
    df['value'] = pd.Series([None for x in index_range], dtype=str)
    df['stat'] = pd.Series([None for x in index_range], dtype=str)
    df['stat_name'] = pd.Series([None for x in index_range], dtype=str)

    return df


# --------------------------------------------------
def reformat_viralverify(args: Args):
    """ Reformat viralVerify output """

    # Read in the dataframe
    raw_df = pd.read_csv(args.file)

    # Rename current columns
    df = raw_df.rename(
        {
            'Contig name': 'record',
            'Prediction': 'prediction',
            'Length': 'length',
            'Score': 'value'
        },
        axis='columns')

    # Add constant columns
    index_range = range(len(df.index))
    df['tool'] = pd.Series([args.tool for x in index_range])
    df['actual'] = pd.Series([args.actual for x in index_range])
    df['lifecycle'] = pd.Series([None for x in index_range])
    df['stat'] = pd.Series([None for x in index_range], dtype=str)
    df['stat_name'] = pd.Series([None for x in index_range])

    return df


# --------------------------------------------------
def reformat_virfinder(args: Args):
    """ Reformat virfinder output """

    # Read in the dataframe
    raw_df = pd.read_csv(args.file, sep='\t')

    # Rename current columns
    df = raw_df.rename({
        'name': 'record',
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
    df['tool'] = pd.Series([args.tool for x in index_range])
    df['actual'] = pd.Series([args.actual for x in index_range])
    df['stat_name'] = pd.Series(['p' for x in index_range])
    df['lifecycle'] = pd.Series([None for x in index_range])

    return df


# --------------------------------------------------
def reformat_virsorter(args: Args):
    """ Reformat virsorter output """

    # Read in the single column in the file
    df = pd.read_csv(args.file)

    if not df.empty:

        # pylint: disable=no-member
        df = df.rename({'sequences': 'record'}, axis='columns')

        # Extract category number from sequence name
        df['value'] = df['record'].str.extract(r'-cat_(?P<value>[\d])')

        # Keep only original record name
        df['record'] = df['record'].str.replace(r'_Fragment.*', '', regex=True)
        df['record'] = df['record'].str.replace(r'(_)([\d]+)$',
                                                '.\\2',
                                                regex=True)

        # Keep only the category number
        df['value'] = df['value'].str[-1]

        # Replace category code with lifecycle
        df['lifecycle'] = df['value']
        df['lifecycle'] = df['lifecycle'].str.replace(r'[123]',
                                                      'lytic',
                                                      regex=True)
        df['lifecycle'] = df['lifecycle'].str.replace(r'[456]',
                                                      'prophage',
                                                      regex=True)

        # Convert value to 1, 2, or 3
        df['value'] = df['value'].str.replace('4', '1')
        df['value'] = df['value'].str.replace('5', '2')
        df['value'] = df['value'].str.replace('6', '3')

        # Add constant columns
        index_range = range(len(df.index))
        df['tool'] = pd.Series([args.tool for x in index_range])
        df['length'] = pd.Series([args.length for x in index_range])
        df['actual'] = pd.Series([args.actual for x in index_range])
        df['prediction'] = pd.Series(['viral' for x in index_range])

        # Add empty columns
        df['stat'] = pd.Series([None for x in index_range], dtype=str)
        df['stat_name'] = pd.Series([None for x in index_range], dtype=str)

    else:  # Dataframe is empty, just output column names
        for col in [
                'tool', 'record', 'length', 'actual', 'prediction',
                'lifecycle', 'value', 'stat', 'stat_name'
        ]:

            # pylint: disable=unsupported-assignment-operation
            df[col] = pd.Series([], dtype=str)

    return df


# --------------------------------------------------
def reformat_virsorter2(args: Args):
    """ Reformat virsorter2 output """

    raw_df = pd.read_csv(args.file, sep='\t')

    index_range = range(len(raw_df.index))

    if len(raw_df) == 0:
        # pylint: disable=unsupported-assignment-operation
        raw_df['max_score'] = pd.Series(['' for x in index_range], dtype=str)

    # Rename columns that are present
    # pylint: disable=no-member
    df = raw_df.rename(
        {
            'seqname': 'record',
            'max_score': 'value',
            'max_score_group': 'prediction'
        },
        axis='columns')

    # Remove extra columns
    df = df.drop(
        columns=['dsDNAphage', 'ssDNA', 'hallmark', 'viral', 'cellular'])

    # Clean up record names
    df['record'] = df['record'].str.replace(r'[\|]{2}.*$', '', regex=True)

    # Add constant columns
    index_range = range(len(df.index))
    df['tool'] = pd.Series([args.tool for x in index_range], dtype=str)
    df['length'] = pd.Series([args.length for x in index_range], dtype=str)
    df['actual'] = pd.Series([args.actual for x in index_range], dtype=str)

    # Add empty columns
    df['stat'] = pd.Series([None for x in index_range], dtype=str)
    df['stat_name'] = pd.Series([None for x in index_range], dtype=str)
    df['lifecycle'] = pd.Series([None for x in index_range], dtype=str)

    return df


# --------------------------------------------------
reformatters = {
    'breadsticks': reformat_breadsticks,
    'dvf': reformat_dvf,
    'metaphinder': reformat_metaphinder,
    'seeker': reformat_seeker,
    'vibrant': reformat_vibrant,
    'viralverify': reformat_viralverify,
    'virfinder': reformat_virfinder,
    'virsorter': reformat_virsorter,
    'virsorter2': reformat_virsorter2
}

# --------------------------------------------------
if __name__ == '__main__':
    main()
