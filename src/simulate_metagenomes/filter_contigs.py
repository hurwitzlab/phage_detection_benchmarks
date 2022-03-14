#!/usr/bin/env python3
"""
Author : Kenneth Schackart <schackartk1@gmail.com>
Date   : 2022-03-09
Purpose: Filter contigs by length
"""

import argparse
import io
import os
from typing import NamedTuple, TextIO, Tuple

from Bio import SeqIO


class Args(NamedTuple):
    """ Command-line arguments """
    contigs: TextIO
    read_length: int
    tolerance: float
    filename: str
    outdir: str


# --------------------------------------------------
def get_args() -> Args:
    """ Get command-line arguments """

    parser = argparse.ArgumentParser(
        description='Filter out contigs that are single reads',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('contigs',
                        metavar='FILE',
                        type=argparse.FileType('rt'),
                        help='Assembled contigs FASTA file')

    parser.add_argument('-l',
                        '--read_length',
                        metavar='LENGTH',
                        type=int,
                        help='Nominal simulated read length (nt)')

    parser.add_argument('-t',
                        '--tolerance',
                        metavar='PCT',
                        type=float,
                        help='Length tolerance: length>-l*(-t+1)',
                        default=0.05)

    parser.add_argument('-f',
                        '--filename',
                        metavar='NAME',
                        type=str,
                        help='Output filename',
                        default='filtered_contigs.fa')

    parser.add_argument('-o',
                        '--outdir',
                        metavar='DIR',
                        type=str,
                        help='Output directory',
                        default='out')

    args = parser.parse_args()

    # If tolerance greater than 1, assume it is a percentage
    if args.tolerance >= 1:
        args.tolerance = args.tolerance / 100

    return Args(args.contigs, args.read_length, args.tolerance, args.filename,
                args.outdir)


# --------------------------------------------------
def main() -> None:
    """ We're jammin'in the name of the Lord """

    args = get_args()
    in_fh = args.contigs
    length = args.read_length
    tolerance = args.tolerance

    if not os.path.isdir(args.outdir):
        os.mkdir(args.outdir)

    length_thresh = calc_length_thresh(length, tolerance)

    out_file = make_filename(args.outdir, args.filename)

    with open(out_file, 'wt') as out_fh:
        kept, total = filter_contigs(in_fh, length_thresh, out_fh)

    print(f'Done. Wrote output to {out_file}\n'
          f'{kept} of {total} contigs retained'
          f' with length >= {int(length_thresh)} nt.')


# --------------------------------------------------
def calc_length_thresh(length: int, tolerance: float) -> float:
    """ Calculate length threshold from nominal read length and tolerance """

    return length * (1 + tolerance)


# --------------------------------------------------
def test_calc_length_thresh() -> None:
    """ Test calc_length_thresh() """

    assert calc_length_thresh(300, 0.) == 300.
    assert calc_length_thresh(300, 0.05) == 315.
    assert calc_length_thresh(125, 0.05) == 131.25


# --------------------------------------------------
def make_filename(out_dir: str, filename: str) -> str:
    """ Create output file name """

    _, ext = os.path.splitext(filename)
    if not ext:
        filename = filename + '.fa'

    return os.path.join(out_dir, filename)


# --------------------------------------------------
def test_make_filenames() -> None:
    """ Test make_filenames() """

    # Explicit filename with extension
    assert make_filename('out',
                         'profile_1_miseq.fa') == 'out/profile_1_miseq.fa'
    assert make_filename(
        'out', 'profile_1_miseq.fasta') == 'out/profile_1_miseq.fasta'

    # Assume filename extension
    assert make_filename('out', 'profile_1_miseq') == 'out/profile_1_miseq.fa'


# --------------------------------------------------
def filter_contigs(in_fh: TextIO, thresh: float,
                   out_fh: TextIO) -> Tuple[int, int]:
    """ Filter contigs in file by length threshold """

    num_kept = 0
    i = 0
    for i, contig in enumerate(SeqIO.parse(in_fh, 'fasta'), start=1):
        if len(contig.seq) >= thresh:
            num_kept += 1
            SeqIO.write(contig, out_fh, 'fasta')

    return num_kept, i


# --------------------------------------------------
def test_filter_contigs() -> None:
    """ Test filter_contigs() """

    example_contigs = io.StringIO('>k141_451933 flag=1 multi=1.0000 len=16\n'
                                  'ATGCATGCATGCATGC\n'
                                  '>k141_55624 flag=1 multi=1.0000 len=10\n'
                                  'ATGCATGCAT\n')

    expected_out = io.StringIO('>k141_451933 flag=1 multi=1.0000 len=16\n'
                               'ATGCATGCATGCATGC\n')

    out_fh = io.StringIO('')

    filter_contigs(example_contigs, 16, out_fh)

    out_fh.seek(0)

    assert out_fh.read() == expected_out.read()


# --------------------------------------------------
if __name__ == '__main__':
    main()
