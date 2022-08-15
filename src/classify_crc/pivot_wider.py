#!/usr/bin/env python3
"""
Author : Kenneth Schackart <schackartk1@gmail.com>
Date   : 2022-07-18
Purpose: Pivot combined predictions to have one row per contig
"""

import argparse
import os
from typing import NamedTuple, TextIO

import numpy as np
import pandas as pd
from pandas.testing import assert_frame_equal, assert_series_equal


class Args(NamedTuple):
    """ Command-line arguments """
    files: TextIO
    out_dir: str


# --------------------------------------------------
def get_args() -> Args:
    """ Get command-line arguments """

    parser = argparse.ArgumentParser(
        description='Pivot combined predictions to have one row per contig',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('file',
                        metavar='FILE',
                        help='File of combined predictions from each tool',
                        type=argparse.FileType('rt'))

    parser.add_argument('-o',
                        '--out_dir',
                        metavar='DIR',
                        help='Output directory',
                        type=str,
                        default='out')

    args = parser.parse_args()

    return Args(args.file, args.out_dir)


# --------------------------------------------------
def relabel_predictions(pred_column: pd.Series) -> pd.Series:
    """ Relabel predictions for consistency"""

    viral = ['dsDNAphage', 'phage', 'viral', 'Virus']
    nonviral = [
        'bacteria', 'Chromosome', 'non-viral', 'Plasmid', 'ssDNA',
        'Uncertain - plasmid or chromosomal', 'Uncertain - too short',
        'Uncertain - viral or bacterial'
    ]

    conditions = [pred_column.isin(viral), pred_column.isin(nonviral)]
    choices = ['viral', 'non-viral']

    pred_column = pd.Series(np.select(conditions, choices))

    return pred_column


# --------------------------------------------------
def test_relabel_predictions() -> None:
    """ Test relabel_predictions() """

    in_col = pd.Series([
        'dsDNAphage', 'phage', 'viral', 'Virus', 'bacteria', 'Chromosome',
        'non-viral', 'Plasmid', 'ssDNA', 'Uncertain - plasmid or chromosomal',
        'Uncertain - too short', 'Uncertain - viral or bacterial'
    ])

    out_col = pd.Series([
        'viral', 'viral', 'viral', 'viral', 'non-viral', 'non-viral',
        'non-viral', 'non-viral', 'non-viral', 'non-viral', 'non-viral',
        'non-viral'
    ])

    assert_series_equal(relabel_predictions(in_col), out_col)


# --------------------------------------------------
def clean_records(records: pd.Series) -> pd.Series:
    """ Clean record names for virsorter """

    return records.str.extract(r'(\w+_\d+)', expand=False)


# --------------------------------------------------
def test_clean_records() -> None:
    """ Test clean_records() """

    in_col = pd.Series(
        ['k141_52055_flag=1_multi=2_0000_len=562-cat.3', 'k141_25081'])

    out_col = pd.Series(['k141_52055', 'k141_25081'])

    assert_series_equal(clean_records(in_col), out_col)


# --------------------------------------------------
def complete_classifications(df: pd.DataFrame) -> pd.DataFrame:
    """ Fill in missing classifications """

    out_df = pd.DataFrame(
        columns=['tool', 'record', 'metagenome', 'prediction'])

    for metagenome, metagenome_df in df.groupby('metagenome'):
        metagenome = metagenome_df['metagenome'].unique()
        all_records = metagenome_df['record'].unique()
        all_tools = metagenome_df['tool'].unique()
        names = ['record', 'tool']

        multi_index = pd.MultiIndex.from_product([all_records, all_tools],
                                                 names=names)

        metagenome_df = metagenome_df.set_index(names).reindex(
            multi_index).reset_index()
        metagenome_df['metagenome'] = metagenome_df['metagenome'].fillna(
            metagenome[0])

        out_df = pd.concat([out_df, metagenome_df])

    out_df['prediction'] = out_df['prediction'].fillna('non-viral')
    out_df = out_df.reset_index(drop=True)

    return out_df


# --------------------------------------------------
def test_complete_classifications() -> None:
    """ Test complete_classifications() """

    in_df = pd.DataFrame(
        [['dvf', 'k141', 'Adult1_hiseq', 'non-viral'],
         ['dvf', 'k142', 'Adult1_hiseq', 'non-viral'],
         ['dvf', 'k143', 'Adult1_hiseq', 'non-viral'],
         ['dvf', 'k141', 'Adult1_miseq', 'viral'],
         ['dvf', 'k142', 'Adult1_miseq', 'viral'],
         ['seeker', 'k141', 'Adult1_hiseq', 'viral'],
         ['seeker', 'k141', 'Adult1_miseq', 'viral']],
        columns=['tool', 'record', 'metagenome', 'prediction'])

    out_df = pd.DataFrame(
        [['dvf', 'k141', 'Adult1_hiseq', 'non-viral'],
         ['seeker', 'k141', 'Adult1_hiseq', 'viral'],
         ['dvf', 'k142', 'Adult1_hiseq', 'non-viral'],
         ['seeker', 'k142', 'Adult1_hiseq', 'non-viral'],
         ['dvf', 'k143', 'Adult1_hiseq', 'non-viral'],
         ['seeker', 'k143', 'Adult1_hiseq', 'non-viral'],
         ['dvf', 'k141', 'Adult1_miseq', 'viral'],
         ['seeker', 'k141', 'Adult1_miseq', 'viral'],
         ['dvf', 'k142', 'Adult1_miseq', 'viral'],
         ['seeker', 'k142', 'Adult1_miseq', 'non-viral']],
        columns=['tool', 'record', 'metagenome', 'prediction'])

    assert_frame_equal(complete_classifications(in_df), out_df)


# --------------------------------------------------
def clean_predictions(df: pd.DataFrame) -> pd.DataFrame:
    """ Fill in missing predicitons, and fix predicted labels """

    df = df[['tool', 'record', 'metagenome', 'prediction']]

    df['record'] = clean_records(df['record'])

    df = df.drop_duplicates(['tool', 'record', 'metagenome'])

    df = complete_classifications(df)

    df['prediction'] = relabel_predictions(df['prediction'])

    return df


# --------------------------------------------------
def test_clean_predictions() -> None:
    """ Test clean_predictions() """

    in_df = pd.DataFrame(
        [['dvf', 'k141_1', 'Adult1_hiseq', 'bacteria', ''],
         ['dvf', 'k142_1', 'Adult1_hiseq', 'ssDNA', ''],
         ['dvf', 'k143_1', 'Adult1_hiseq', 'Plasmid', ''],
         ['dvf', 'k141_1', 'Adult1_miseq', 'viral', ''],
         ['dvf', 'k142_1', 'Adult1_miseq', 'phage', ''],
         ['seeker', 'k141_1', 'Adult1_hiseq', 'viral', ''],
         ['seeker', 'k141_1', 'Adult1_miseq', 'Virus', '']],
        columns=['tool', 'record', 'metagenome', 'prediction', 'lifecycle'])

    out_df = pd.DataFrame(
        [['dvf', 'k141_1', 'Adult1_hiseq', 'non-viral'],
         ['seeker', 'k141_1', 'Adult1_hiseq', 'viral'],
         ['dvf', 'k142_1', 'Adult1_hiseq', 'non-viral'],
         ['seeker', 'k142_1', 'Adult1_hiseq', 'non-viral'],
         ['dvf', 'k143_1', 'Adult1_hiseq', 'non-viral'],
         ['seeker', 'k143_1', 'Adult1_hiseq', 'non-viral'],
         ['dvf', 'k141_1', 'Adult1_miseq', 'viral'],
         ['seeker', 'k141_1', 'Adult1_miseq', 'viral'],
         ['dvf', 'k142_1', 'Adult1_miseq', 'viral'],
         ['seeker', 'k142_1', 'Adult1_miseq', 'non-viral']],
        columns=['tool', 'record', 'metagenome', 'prediction'])

    assert_frame_equal(clean_predictions(in_df), out_df)


# --------------------------------------------------
def pivot_wider(df: pd.DataFrame) -> pd.DataFrame:
    """ Rearrange dataframe by creating one row per contig """

    df = df.pivot(index=['metagenome', 'record'],
                  columns='tool',
                  values='prediction')

    df.reset_index(inplace=True)

    df = df.rename_axis(None, axis="columns")

    print(df.columns)

    return df


# --------------------------------------------------
def test_pivot_wider() -> None:
    """ Test pivot_wider """

    in_df = pd.DataFrame(
        [['dvf', 'k141_1', 'Adult1_hiseq', 'non-viral'],
         ['seeker', 'k141_1', 'Adult1_hiseq', 'viral'],
         ['dvf', 'k142_1', 'Adult1_hiseq', 'non-viral'],
         ['seeker', 'k142_1', 'Adult1_hiseq', 'non-viral'],
         ['dvf', 'k143_1', 'Adult1_hiseq', 'non-viral'],
         ['seeker', 'k143_1', 'Adult1_hiseq', 'non-viral'],
         ['dvf', 'k141_1', 'Adult1_miseq', 'viral'],
         ['seeker', 'k141_1', 'Adult1_miseq', 'viral'],
         ['dvf', 'k142_1', 'Adult1_miseq', 'viral'],
         ['seeker', 'k142_1', 'Adult1_miseq', 'non-viral']],
        columns=['tool', 'record', 'metagenome', 'prediction'])

    out_df = pd.DataFrame(
        [['Adult1_hiseq', 'k141_1', 'non-viral', 'viral'],
         ['Adult1_hiseq', 'k142_1', 'non-viral', 'non-viral'],
         ['Adult1_hiseq', 'k143_1', 'non-viral', 'non-viral'],
         ['Adult1_miseq', 'k141_1', 'viral', 'viral'],
         ['Adult1_miseq', 'k142_1', 'viral', 'non-viral']],
        columns=['metagenome', 'record', 'dvf', 'seeker'])

    assert_frame_equal(pivot_wider(in_df), out_df)


# --------------------------------------------------
def main() -> None:
    """ Make a jazz noise here """

    args = get_args()

    out_dir = args.out_dir
    if not os.path.isdir(out_dir):
        os.makedirs(out_dir)

    df = clean_predictions(pd.read_csv(args.files))
    df = pivot_wider(df)

    out_file = os.path.join(args.out_dir, 'pivoted_predictions.csv')
    df.to_csv(out_file, index=False)


# --------------------------------------------------
if __name__ == '__main__':
    main()
