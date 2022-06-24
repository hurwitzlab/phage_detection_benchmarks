#!/usr/bin/env python3
"""
Author : Kenneth Schackart <schackartk1@gmail.com>
Date   : 2021-10-12
Purpose: Calculate performance metrics
"""

import argparse
import os
from typing import NamedTuple, TextIO
from pandas._testing.asserters import assert_almost_equal

from sklearn.metrics import confusion_matrix
import numpy as np
import pandas as pd
from pandas.testing import assert_frame_equal, assert_series_equal


class Args(NamedTuple):
    """ Command-line arguments """
    file: TextIO
    taxonomy: TextIO
    width: float
    min_bin: float
    max_bin: float
    out_dir: str


# --------------------------------------------------
class Metrics(NamedTuple):
    """ Classification metrics """
    tn: int
    fp: int
    fn: int
    tp: int
    specificity: float
    sensitivity: float
    precision: float
    f1: float


# --------------------------------------------------
def get_args() -> Args:
    """ Get command-line arguments """

    parser = argparse.ArgumentParser(
        description='Calculate performance metrics',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('file',
                        metavar='FILE',
                        help='Combined predictions of metagenome file',
                        type=argparse.FileType('rt'))

    parser.add_argument('-t',
                        '--taxonomy_file',
                        metavar='FILE',
                        help='Contig assigned taxonomies',
                        type=argparse.FileType('rt'),
                        required=True)

    parser.add_argument('-w',
                        '--bin_width',
                        metavar='WIDTH',
                        help='Bin width; log scale',
                        type=float,
                        default=0.50)

    parser.add_argument('-s',
                        '--smallest_bin',
                        metavar='WIDTH',
                        help='Lowest bin boundary; log scale',
                        type=float,
                        default=2.50)

    parser.add_argument('-l',
                        '--highest_bin',
                        metavar='WIDTH',
                        help='Highest bin boundary; log scale',
                        type=float,
                        default=5.0)

    parser.add_argument('-o',
                        '--out_dir',
                        metavar='DIR',
                        help='Output directory',
                        type=str,
                        default='out')

    args = parser.parse_args()

    return Args(args.file, args.taxonomy_file, args.bin_width,
                args.smallest_bin, args.highest_bin, args.out_dir)


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
def clean_predictions(df: pd.DataFrame) -> pd.DataFrame:
    """ Fill in missing predicitons, and fix predicted labels """

    df = df[['tool', 'record', 'metagenome', 'prediction']]

    df['record'] = clean_records(df['record'])

    df = df.drop_duplicates(['tool', 'record'])

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
def add_taxonomy(preds: pd.DataFrame, tax: pd.DataFrame) -> pd.DataFrame:
    """ Add contig taxonomy for true values """

    out_df = pd.merge(preds,
                      tax,
                      how='left',
                      left_on='record',
                      right_on='query_id')

    out_df = out_df[out_df['superkingdom'].notna()]
    out_df = out_df[out_df['origin'] == 'single']

    out_df = out_df[[
        'metagenome', 'tool', 'record', 'prediction', 'query_length',
        'superkingdom'
    ]]

    out_df = out_df.rename(columns={'query_length': 'length'})

    out_df['actual_class'] = np.where(out_df['superkingdom'] == 'Viruses',
                                      'viral', 'non-viral')

    return out_df


# --------------------------------------------------
def bin_lengths(df: pd.DataFrame, bin_width: float, min_bin: float,
                max_bin: float) -> pd.DataFrame:

    breaks = [
        x / 100 for x in list(
            range(int(min_bin * 100), int((max_bin + bin_width) *
                                          100), int(bin_width * 100)))
    ]

    df['log_length'] = np.log10(df['length'])

    df['length_bin'] = 0

    for bin in breaks:
        df['length_bin'] = np.where(df['log_length'] >= bin, bin,
                                    df['length_bin'])

    return df


# --------------------------------------------------
def calc_metrics(true: np.array, pred: np.array) -> Metrics:
    """ Caculate classification performance metrics """

    conf_mat = confusion_matrix(true, pred, labels=['non-viral', 'viral'])

    tn, fp, fn, tp = conf_mat.ravel()

    specificity = np.nan if (tn + fp) == 0 else tn / (tn + fp)
    sensitivity = np.nan if (tp + fn) == 0 else tp / (tp + fn)
    precision = np.nan if (tp + fp) == 0 else tp / (tp + fp)
    f1 = np.nan if (
        np.isnan(precision) or np.isnan(sensitivity) or
        (precision + sensitivity)
        == 0) else 2 * precision * sensitivity / (precision + sensitivity)

    return Metrics(tn, fp, fn, tp, specificity, sensitivity, precision, f1)


# --------------------------------------------------
def test_calc_metrics() -> None:
    """ Test calc_metrics() """

    true = np.array(['viral', 'non-viral'])
    pred = np.array(['viral', 'viral'])
    exp = Metrics(0, 1, 0, 1, 0., 1., 0.5, 2 / 3)
    assert calc_metrics(true, pred) == exp

    true = np.array(['viral', 'non-viral'])
    pred = np.array(['non-viral', 'non-viral'])
    exp = Metrics(1, 0, 1, 0, 1., 0., np.nan, np.nan)
    assert_almost_equal(calc_metrics(true, pred), exp)


# --------------------------------------------------
def get_lengthbin_metrics(df: pd.DataFrame) -> pd.DataFrame:
    """ Get metrics for each length bin """

    out_df = pd.DataFrame(columns=[
        'length_bin', 'tp', 'fp', 'tn', 'fn', 'f1', 'sensitivity',
        'specificity', 'precision'
    ])
    for _, lengthbin_df in df.groupby('length_bin'):
        metrics = calc_metrics(np.array(lengthbin_df['prediction']),
                               np.array(lengthbin_df['actual_class']))

        length_bin = lengthbin_df['length_bin'].unique()

        new_row = pd.DataFrame({
            'length_bin': length_bin,
            'tp': metrics.tp,
            'fp': metrics.fp,
            'tn': metrics.tn,
            'fn': metrics.fn,
            'f1': metrics.f1,
            'sensitivity': metrics.sensitivity,
            'specificity': metrics.specificity,
            'precision': metrics.precision
        })

        out_df = pd.concat([out_df, new_row])

    return out_df


# --------------------------------------------------
def get_tool_metrics(df: pd.DataFrame) -> pd.DataFrame:
    """ Get metrics for each tool per length bin """

    out_df = pd.DataFrame(columns=[
        'metagenome', 'tool', 'length_bin', 'tp', 'fp', 'tn', 'fn', 'f1',
        'sensitivity', 'specificity', 'precision'
    ])
    for _, tool_df in df.groupby(['metagenome', 'tool']):
        tool_metrics = get_lengthbin_metrics(tool_df)

        nrows = len(tool_metrics)
        tool_metrics['tool'] = [tool_df['tool'].unique()[0]] * nrows
        tool_metrics['metagenome'] = [tool_df['metagenome'].unique()[0]
                                      ] * nrows

        out_df = pd.concat([out_df, tool_metrics])

    return out_df


# --------------------------------------------------
def main() -> None:
    """ Make a jazz noise here """

    args = get_args()
    out_dir = args.out_dir

    if not os.path.isdir(out_dir):
        os.mkdir(out_dir)

    out_file = os.path.join(out_dir, 'summary_stats.csv')

    contig_tax = pd.read_csv(args.taxonomy)

    in_df = pd.read_csv(args.file)

    predictions = clean_predictions(in_df)

    predictions = add_taxonomy(predictions, contig_tax)

    predictions = bin_lengths(predictions, args.width, args.min_bin,
                              args.max_bin)

    metrics = get_tool_metrics(predictions)

    metrics.to_csv(out_file, index=False)
    
    print(f'Done. Wrote to file {out_file}.')


# --------------------------------------------------
if __name__ == '__main__':
    main()
