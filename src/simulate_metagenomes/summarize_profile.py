#!/usr/bin/env python3
"""
Author : Kenneth Schackart <schackartk1@gmail.com>
Date   : 2022-03-03
Purpose: Compare original Bracken and InSilicoSeq input profiles
"""

import argparse
from pandas.testing import assert_frame_equal
import bracken_profiler
import os
import pandas as pd
from typing import NamedTuple, TextIO


class Args(NamedTuple):
    """ Command-line arguments """
    bracken: TextIO
    profile: TextIO
    taxonomy: TextIO
    outdir: str


# --------------------------------------------------
def get_args() -> Args:
    """ Get command-line arguments """

    parser = argparse.ArgumentParser(
        description='Compare original Bracken and InSilicoSeq input profiles',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('-b',
                        '--bracken',
                        help='Bracken output file',
                        metavar='FILE',
                        type=argparse.FileType('rt'),
                        required=True)

    parser.add_argument('-p',
                        '--profile',
                        help='Generated profile',
                        metavar='FILE',
                        type=argparse.FileType('rt'),
                        required=True)

    parser.add_argument('-t',
                        '--taxonomy',
                        metavar='FILE',
                        help='Taxonomy mapping file',
                        type=argparse.FileType('rt'),
                        default='../../data/refseq_info/taxonomy.csv')

    parser.add_argument('-o',
                        '--outdir',
                        metavar='DIR',
                        help='Output directory',
                        type=str,
                        default='out')

    args = parser.parse_args()

    return Args(args.bracken, args.profile, args.taxonomy, args.outdir)


# --------------------------------------------------
def main() -> None:
    """ Make it happen """

    args = get_args()
    out_dir = args.outdir
    bracken_profile = args.bracken
    profile = args.profile

    if not os.path.isdir(out_dir):
        os.mkdir(out_dir)

    # Clean Bracken profile using function in other script
    # Keeps 'name', 'taxonomy_id', and 'fraction_total_reads'
    bracken_df = bracken_profiler.clean_bracken(
        pd.read_csv(bracken_profile, sep='\t'))

    taxonomy_df = bracken_profiler.clean_taxonomy(pd.read_csv(args.taxonomy))

    joined_df = bracken_profiler.join_dfs(bracken_df,
                                          taxonomy_df,
                                          how='left',
                                          drop_dup=False)

    profile_df = pd.read_csv(profile,
                             sep='\t',
                             names=['accession', 'fraction_total_reads'])

    joined_profiles = join_profiles(joined_df, profile_df)

    out_file = make_filename(out_dir, bracken_profile.name)

    joined_profiles.to_csv(out_file, index=False)

    print(f'Done. Wrote output to {out_file}.')


# --------------------------------------------------
def join_profiles(bracken: pd.DataFrame,
                  profile: pd.DataFrame) -> pd.DataFrame:
    """ Join generated and Bracken profiles """

    joined_df = pd.merge(bracken,
                         profile,
                         how='left',
                         on='accession',
                         suffixes=['_bracken', None])

    joined_df.drop(['kingdom'], axis='columns', inplace=True)

    joined_df = joined_df[[
        'taxonomy_id', 'accession', 'fraction_total_reads_bracken',
        'fraction_total_reads'
    ]]

    return joined_df


# --------------------------------------------------
def test_join_profiles() -> None:
    """ Test join_profiles() """

    bracken = pd.DataFrame([[
        'Methanococcus voltae', 456320, 0.6523, 'archaea', 'GCF_000006175.1',
        456320
    ]],
                           columns=[
                               'name', 'taxonomy_id', 'fraction_total_reads',
                               'kingdom', 'accession', 'taxid'
                           ])

    profile = pd.DataFrame([['GCF_000006175.1', 0.65250]],
                           columns=['accession', 'fraction_total_reads'])

    out_df = pd.DataFrame([[456320, 'GCF_000006175.1', 0.6523, 0.65250]],
                          columns=[
                              'taxonomy_id', 'accession',
                              'fraction_total_reads_bracken',
                              'fraction_total_reads'
                          ])

    assert_frame_equal(join_profiles(bracken, profile), out_df)


# --------------------------------------------------
def make_filename(out_dir: str, infile: str) -> str:
    """ Create output file name """

    root, _ = os.path.splitext(os.path.basename(infile))

    return os.path.join(out_dir, root + '_profile_comparison.csv')


# --------------------------------------------------
def test_make_filenames() -> None:
    """ Test make_filenames() """

    file_name = 'out/input_1_profile_comparison.csv'
    assert make_filename('out', 'input_1.txt') == file_name
    assert make_filename('out', 'tests/input_1.txt') == file_name


# --------------------------------------------------
if __name__ == '__main__':
    main()
