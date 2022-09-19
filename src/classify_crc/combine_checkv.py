#!/usr/bin/env python3
"""
Author : Kenneth Schackart <schackartk1@gmail.com>
Date   : 2022-03-16
Purpose: Combine summary files
"""

import argparse
import os
import pandas as pd
import re
import sys
from typing import List, NamedTuple, Optional, TextIO, Tuple


class Args(NamedTuple):
    """ Command-line arguments """
    files: List[TextIO]
    regex: str
    out_dir: str


class Nameparts(NamedTuple):
    """ Extracted parts of filename """
    filename: str
    sample: str


# --------------------------------------------------
def get_args() -> Args:
    """ Get command-line arguments """

    parser = argparse.ArgumentParser(
        description='Combine CheckV results',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument(
        'files',
        help='CheckV result files',
        metavar='FILE',
        type=argparse.FileType('rt'),
        nargs='+',
    )

    parser.add_argument('-r',
                        '--regex',
                        help='Filename regular expression',
                        metavar='STR',
                        type=str,
                        required=True)

    parser.add_argument('-o',
                        '--outdir',
                        help='Output directory',
                        metavar='DIR',
                        type=str,
                        default='out')

    args = parser.parse_args()

    return Args(args.files, args.regex, args.outdir)


# --------------------------------------------------
def main() -> None:
    """ Main function """

    args = get_args()
    out_dir = args.out_dir

    if not os.path.isdir(out_dir):
        os.makedirs(out_dir)

    out_df, filename = concat_files(args.regex, args.files)

    out_file = make_filename(out_dir, filename)

    out_df.to_csv(out_file, index=False)

    print(f'Done. Wrote output to {out_file}')


# --------------------------------------------------
def concat_files(regex: str, files: List[TextIO]) -> Tuple[pd.DataFrame, str]:
    """ Concatenate files into single dataframe """

    dfs = []

    for file in files:
        parts = match_regex(regex, file.name)

        df = pd.read_csv(file, sep='\t')

        df['sample'] = parts.sample

        dfs.append(df)

    out_df = pd.concat(dfs, ignore_index=True)

    return out_df, parts.filename


# --------------------------------------------------
def match_regex(regex: str, filename: str) -> Nameparts:
    """ Use supplied regex to extract parts of filename """

    compiled_re = re.compile(regex)

    if 'sample' not in compiled_re.groupindex:
        sys.exit(f'--regex "{regex}" missing "sample" group.')

    match = re.match(compiled_re, filename)

    if not match:
        sys.exit(f'--regex "{regex}" did not match filename "{filename}".')

    match_filename = match.group('filename')
    match_sample = match.group('sample')

    return Nameparts(match_filename, match_sample)


# --------------------------------------------------
def test_match_regex() -> None:
    """ Test match_regex() """

    profile = 'foo/zeller_2466887/checkv/quality_summary.tsv'
    profile_re = (
        r'.*/(?P<sample>\w+_\d+)/checkv/(?P<filename>quality_summary).tsv')
    profile_exp = Nameparts('quality_summary', 'zeller_2466887')

    assert match_regex(profile_re, profile) == profile_exp


# --------------------------------------------------
def make_filename(out_dir: str, filename: str) -> str:
    """ Make output filename """

    out_file = os.path.join(out_dir, 'combined_' + filename + '.csv')

    return out_file


# --------------------------------------------------
def test_make_filename() -> None:
    """ Test make_filename() """

    assert make_filename('out',
                         'parsed_blast') == 'out/combined_parsed_blast.csv'
    assert make_filename('out',
                         'contig_summary') == 'out/combined_contig_summary.csv'
    assert make_filename(
        'out', 'profile_comparison') == 'out/combined_profile_comparison.csv'


# --------------------------------------------------
if __name__ == '__main__':
    main()
