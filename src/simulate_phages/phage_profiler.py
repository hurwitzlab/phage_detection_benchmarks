#!/usr/bin/env python3
"""
Author : Kenneth Schackart <schackartk1@gmail.com>
Date   : 2022-02-09
Purpose: Create profile of phages
"""

import argparse
import os
import pandas as pd
from pandas.testing import assert_frame_equal
from typing import NamedTuple, TextIO, Tuple

pd.options.mode.chained_assignment = None


class Args(NamedTuple):
    """ Command-line arguments """
    taxonomy: TextIO
    num_phages: int
    coverage: int
    num_profiles: int
    seed: bool
    outdir: str


# ---------------------------------------------------------------------------
def get_args() -> Args:
    """ Get command-line arguments """

    parser = argparse.ArgumentParser(
        description='Create profiles of phages',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('taxonomy',
                        metavar='FILE',
                        help='Taxonomy mapping file',
                        type=argparse.FileType('rt'),
                        default='../../data/refseq_info/taxonomy.csv')

    parser.add_argument('-n',
                        '--num_phages',
                        metavar='INT',
                        help='Number of phages to include in profile',
                        type=int,
                        default=500)

    parser.add_argument('-c',
                        '--coverage',
                        metavar='INT',
                        help='Read coverage',
                        type=int,
                        default=30)

    parser.add_argument('-p',
                        '--num_profiles',
                        metavar='INT',
                        help='Number of profiles to make',
                        type=int,
                        default=3)

    parser.add_argument('-s',
                        '--seed',
                        help='Use random seed',
                        action='store_true')

    parser.add_argument('-o',
                        '--outdir',
                        metavar='DIR',
                        help='Output directory',
                        type=str,
                        default='out')

    args = parser.parse_args()

    return Args(args.taxonomy, args.num_phages, args.coverage,
                args.num_profiles, args.seed, args.outdir)


# ---------------------------------------------------------------------------
def main() -> None:
    """ Do the stuff """

    args = get_args()
    out_dir = args.outdir

    if not os.path.isdir(out_dir):
        os.mkdir(out_dir)

    taxonomy_df = clean_taxonomy(pd.read_csv(args.taxonomy))

    phages = get_phages(taxonomy_df)

    for profile_i in range(1, args.num_profiles + 1):

        seed = profile_i if args.seed else None

        select_phages = phages.sample(n=args.num_phages,
                                      random_state=seed,
                                      replace=False)

        profile_df = make_profile_df(select_phages, args.coverage)

        files_df = make_files_df(profile_df)
        profile_out_df = make_out_profile_df(profile_df)

        files_output, profile_output = make_filenames(out_dir, profile_i)

        files_df.to_csv(files_output, sep=",", index=False)
        profile_out_df.to_csv(profile_output,
                              sep="\t",
                              index=False,
                              header=False)

    plu = 's' if args.num_profiles != 1 else ''
    print(f'Done. Wrote {args.num_profiles} profile{plu} to {out_dir}.')


# ---------------------------------------------------------------------------
def clean_taxonomy(df: pd.DataFrame) -> pd.DataFrame:
    """ Clean taxonomy dataframe """

    df = df[[
        'kingdom', 'superkingdom', 'genus', 'species', 'accession', 'taxid'
    ]]

    # There may be multiple refseq files (accession #)
    # for a given tax_id. I need tax_id to be unique,
    # so I will drop duplicate tax id's, keeping only the
    # first accession.
    df = df.drop_duplicates('taxid').reset_index(drop=True)

    return df


# ---------------------------------------------------------------------------
def test_clean_taxonomy() -> None:
    """ Test clean_taxonomy() """

    in_df = pd.DataFrame(
        [
            [
                'archaea', 'GCF_000006175.1', 'NC_014222.1', 456320, 2188,
                'Archaea', 'Euryarchaeota', 'Methanococci', 'Methanococcales',
                'Methanococcaceae', 'Methanococcus', 'Methanococcus voltae'
            ],
            [  # Same as above, but different seq_id
                'archaea', 'GCF_000006175.1', 'NC_014223.1', 456320, 2188,
                'Archaea', 'Euryarchaeota', 'Methanococci', 'Methanococcales',
                'Methanococcaceae', 'Methanococcus', 'Methanococcus voltae'
            ],
            [
                'bacteria', 'GCF_003860425.1', 'NZ_CP034193.1', 1613, 1613,
                'Bacteria', 'Firmicutes', 'Bacilli', 'Lactobacillales',
                'Lactobacillaceae', 'Limosilactobacillus',
                'Limosilactobacillus fermentum'
            ]
        ],
        columns=[
            'kingdom', 'accession', 'seq_id', 'taxid', 'species_taxid',
            'superkingdom', 'phylum', 'class', 'order', 'family', 'genus',
            'species'
        ])

    out_df = pd.DataFrame(
        [[
            'archaea', 'Archaea', 'Methanococcus', 'Methanococcus voltae',
            'GCF_000006175.1', 456320
        ],
         [
             'bacteria', 'Bacteria', 'Limosilactobacillus',
             'Limosilactobacillus fermentum', 'GCF_003860425.1', 1613
         ]],
        columns=[
            'kingdom', 'superkingdom', 'genus', 'species', 'accession', 'taxid'
        ])

    assert_frame_equal(clean_taxonomy(in_df), out_df)


# ---------------------------------------------------------------------------
def get_phages(df: pd.DataFrame) -> pd.DataFrame:
    """ Filter taxonomy dataframe to only include phages """

    df = df[df['superkingdom'] == 'Viruses']
    df = df[df['species'].str.contains('phage', case=False)]

    df.reset_index(drop=True, inplace=True)

    return df


# ---------------------------------------------------------------------------
def test_get_phages() -> None:
    """ Test get_phages() """

    in_df = pd.DataFrame(
        [[
            'archaea', 'Archaea', 'Methanococcus', 'Methanococcus voltae',
            'GCF_001', 123
        ], ['bacteria', 'Bacteria', 'Limo', 'Limo fermentum', 'GCF_002', 456],
         ['bacteria', 'Bacteria', 'Escher', 'Escher phage', 'GCF_003', 789],
         ['viruses', 'Viruses', 'Gen', 'Generic virus', 'GCF_004', 741],
         ['viruses', 'Viruses', 'Actual', 'Actual phage', 'GCF_005', 852]],
        columns=[
            'kingdom', 'superkingdom', 'genus', 'species', 'accession', 'taxid'
        ])

    out_df = pd.DataFrame(
        [['viruses', 'Viruses', 'Actual', 'Actual phage', 'GCF_005', 852]],
        columns=[
            'kingdom', 'superkingdom', 'genus', 'species', 'accession', 'taxid'
        ])

    assert_frame_equal(get_phages(in_df), out_df)


# ---------------------------------------------------------------------------
def make_profile_df(df: pd.DataFrame, coverage: int) -> pd.DataFrame:
    """ Create profile from selected phages """

    df = df[['kingdom', 'accession']]

    df['coverage'] = coverage

    return df


# ---------------------------------------------------------------------------
def test_make_profile_df() -> None:
    """ Test make_profile_df() """

    in_df = pd.DataFrame(
        [['viruses', 'Viruses', 'Actual', 'phage 1', 'GCF_001', 123],
         ['viruses', 'Viruses', 'Actual', 'phage 2', 'GCF_002', 456],
         ['viruses', 'Viruses', 'Actual', 'phage 3', 'GCF_003', 789],
         ['viruses', 'Viruses', 'Actual', 'phage 4', 'GCF_004', 741],
         ['viruses', 'Viruses', 'Actual', 'phage 5', 'GCF_005', 852]],
        columns=[
            'kingdom', 'superkingdom', 'genus', 'species', 'accession', 'taxid'
        ])

    out_df = pd.DataFrame(
        [['viruses', 'GCF_001', 0.2], ['viruses', 'GCF_002', 30],
         ['viruses', 'GCF_003', 0.2], ['viruses', 'GCF_004', 30],
         ['viruses', 'GCF_005', 0.2]],
        columns=['kingdom', 'accession', 'coverage'])

    assert_frame_equal(make_profile_df(in_df), out_df)


# ---------------------------------------------------------------------------
def make_files_df(df: pd.DataFrame) -> pd.DataFrame:
    """ Create file names of genomes """

    files_df = df[['kingdom', 'accession']]

    files_df.reset_index(inplace=True, drop=True)

    files_df['filename'] = pd.Series(
        map(lambda king, acc: os.path.join(king, acc + '*.fna'),
            files_df['kingdom'], files_df['accession']))

    files_df = files_df[['filename', 'accession']]

    return files_df


# ---------------------------------------------------------------------------
def test_make_files_df() -> None:
    """ Test make_files_df() """

    in_df = pd.DataFrame([['archaea', 'GCF_000006175.1', 30]],
                         columns=['kingdom', 'accession', 'coverage'])

    out_df = pd.DataFrame(
        [['archaea/GCF_000006175.1*.fna', 'GCF_000006175.1']],
        columns=['filename', 'accession'])

    assert_frame_equal(make_files_df(in_df), out_df)


# ---------------------------------------------------------------------------
def make_out_profile_df(df: pd.DataFrame) -> pd.DataFrame:
    """ Create profile of seq IDs and coverages """

    profile_df = df[['accession', 'coverage']]

    return profile_df


# ---------------------------------------------------------------------------
def test_make_out_profile_df() -> None:
    """ Test make_profile_df() """

    in_df = pd.DataFrame([['archaea', 'GCF_000006175.1', 30]],
                         columns=['kingdom', 'accession', 'coverage'])

    out_df = pd.DataFrame([['GCF_000006175.1', 30]],
                          columns=['accession', 'coverage'])

    assert_frame_equal(make_out_profile_df(in_df), out_df)


# ---------------------------------------------------------------------------
def make_filenames(out_dir: str, profile_num: int) -> Tuple[str, str]:
    """ Create names of output files """

    root = 'phage_profile_' + str(profile_num)

    files_output = os.path.join(out_dir, root + '_files.txt')
    profile_output = os.path.join(out_dir, root + '_profile.txt')

    return files_output, profile_output


# ---------------------------------------------------------------------------
def test_make_filenames() -> None:
    """ Test make_filenames() """
    file_names = ('out/phage_profile_1_files.txt',
                  'out/phage_profile_1_profile.txt')
    assert make_filenames('out', 1) == file_names


# ---------------------------------------------------------------------------
if __name__ == '__main__':
    main()
