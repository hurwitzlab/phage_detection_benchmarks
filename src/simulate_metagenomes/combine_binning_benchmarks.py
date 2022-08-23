#!/usr/bin/env python3
"""
Author : Kenneth Schackart <schackartk1@gmail.com>
Date   : 2022-03-16
Purpose: Combine benchmark files from all binning steps
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
    regex: str
    out_dir: str


class Nameparts(NamedTuple):
    """ Extracted parts of filename """
    step: str
    profile: str
    model: str


# --------------------------------------------------
def get_args() -> Args:
    """ Get command-line arguments """

    parser = argparse.ArgumentParser(
        description='Combine binning benchmark files',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument(
        'files',
        help='Benchmark files',
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
    """ Come together, right now, over me """

    args = get_args()
    out_dir = args.out_dir

    if not os.path.isdir(out_dir):
        os.makedirs(out_dir)

    out_df = concat_files(args.regex, args.files)

    out_file = os.path.join(out_dir, 'combined.csv')

    out_df.to_csv(out_file, index=False)

    print(f'Done. Wrote output to {out_file}')


# --------------------------------------------------
def concat_files(regex: str, files: List[TextIO]) -> pd.DataFrame:
    """ Concatenate files into single dataframe """

    dfs = []

    for file in files:
        parts = match_regex(regex, file.name)

        df = pd.read_csv(file)

        df['step'] = parts.step
        df['profile'] = parts.profile
        df['model'] = parts.model

        dfs.append(df)

    out_df = pd.concat(dfs, ignore_index=True)

    return out_df


# --------------------------------------------------
def match_regex(regex: str, filename: str) -> Nameparts:
    """ Use supplied regex to extract parts of filename """

    compiled_re = re.compile(regex)

    match = re.search(compiled_re, filename)

    if not match:
        sys.exit(f'--regex "{regex}" did not match filename "{filename}".')

    match_step = match.group('step')
    match_profile = match.group('profile')
    match_model = match.group('model')

    return Nameparts(match_step, match_profile, match_model)


# --------------------------------------------------
def test_match_regex() -> None:
    """ Test match_regex() """

    file = 'data/bowtie_map_reads/Adult1_hiseq.txt'
    file_re = (r'(?P<step>[\w_]+)/(?P<profile>[\w.]+)_(?P<model>\w+).txt')
    file_exp = Nameparts('bowtie_map_reads', 'Adult1', 'hiseq')

    assert match_regex(file_re, file) == file_exp


# --------------------------------------------------
if __name__ == '__main__':
    main()
