#!/usr/bin/env python3
"""
Author : Kenneth Schackart <schackartk1@gmail.com>
Date   : 2022-03-09
Purpose: Get lengths of all contigs
"""

import argparse
import io
import os
from typing import NamedTuple, TextIO

from Bio import SeqIO


class Args(NamedTuple):
    """ Command-line arguments """
    contigs: TextIO
    filename: str
    outdir: str


# --------------------------------------------------
def get_args() -> Args:
    """ Get command-line arguments """

    parser = argparse.ArgumentParser(
        description='Get lengths of all contigs',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('contigs',
                        metavar='FILE',
                        type=argparse.FileType('rt'),
                        help='Assembled contigs FASTA file')

    parser.add_argument('-f',
                        '--filename',
                        metavar='NAME',
                        type=str,
                        help='Output filename',
                        default='contig_summary.csv')

    parser.add_argument('-o',
                        '--outdir',
                        metavar='DIR',
                        type=str,
                        help='Output directory',
                        default='out')

    args = parser.parse_args()

    return Args(args.contigs, args.filename, args.outdir)


# --------------------------------------------------
def main() -> None:
    """ We're jammin'in the name of the Lord """

    args = get_args()
    in_fh = args.contigs

    if not os.path.isdir(args.outdir):
        os.mkdir(args.outdir)

    out_file = make_filename(args.outdir, args.filename)

    with open(out_file, 'wt') as out_fh:
        summarize_contigs(in_fh, out_fh)

    print(f'Done. Wrote output to {out_file}')


# --------------------------------------------------
def make_filename(out_dir: str, filename: str) -> str:
    """ Create output file name """

    _, ext = os.path.splitext(filename)
    if not ext:
        filename = filename + '.csv'

    return os.path.join(out_dir, filename)


# --------------------------------------------------
def test_make_filenames() -> None:
    """ Test make_filenames() """

    # Explicit filename with extension
    assert make_filename('out',
                         'contig_summary.csv') == 'out/contig_summary.csv'

    # Assume filename extension
    assert make_filename('out', 'contig_summary') == 'out/contig_summary.csv'


# --------------------------------------------------
def summarize_contigs(in_fh: TextIO, out_fh: TextIO) -> None:
    """ Output the length of each contig """

    out_fh.write('contig_id,length\n')

    for contig in SeqIO.parse(in_fh, 'fasta'):
        out_fh.write(f'{contig.id},{len(contig.seq)}\n')


# --------------------------------------------------
def test_summarize_contigs() -> None:
    """ Test summarize_contigs() """

    example_contigs = io.StringIO('>k141_451933 flag=1 multi=1.0000 len=16\n'
                                  'ATGCATGCATGCATGC\n'
                                  '>k141_55624 flag=1 multi=1.0000 len=10\n'
                                  'ATGCATGCAT\n')

    expected_out = io.StringIO('contig_id,length\n'
                               'k141_451933,16\n'
                               'k141_55624,10\n')

    out_fh = io.StringIO('')

    summarize_contigs(example_contigs, out_fh)

    out_fh.seek(0)

    assert out_fh.read() == expected_out.read()


# --------------------------------------------------
if __name__ == '__main__':
    main()
