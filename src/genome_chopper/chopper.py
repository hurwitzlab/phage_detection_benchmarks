#!/usr/bin/env python3
"""
Author : Kenneth Schackart <schackartk1@gmail.com>
Date   : 2021-05-25
Purpose: Chop a genome into simulated contigs
"""

import argparse
import os
import sys
from typing import List, NamedTuple, TextIO
from Bio import SeqIO  # , SeqFeature
# from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord


class Args(NamedTuple):
    """ Command-line arguments """
    genome: List[TextIO]
    out_dir: str
    length: int
    overlap: int


# --------------------------------------------------
def get_args() -> Args:
    """ Get command-line arguments """

    parser = argparse.ArgumentParser(
        description='Chop a genome into simulated contigs',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('genome',
                        metavar='FILE',
                        help='Input DNA file(s), each with only 1 record',
                        type=argparse.FileType('rt'),
                        nargs='+')

    parser.add_argument('-o',
                        '--out_dir',
                        help='Output directory',
                        metavar='DIR',
                        type=str,
                        default='out')

    parser.add_argument('-l',
                        '--length',
                        help='Segment length (b)',
                        metavar='INT',
                        type=int,
                        default='100')

    parser.add_argument('-v',
                        '--overlap',
                        help='Overlap length (b)',
                        metavar='INT',
                        type=int,
                        default='10')

    args = parser.parse_args()

    if args.length <= 0:
        parser.error(f'length "{args.length}" must be greater than 0')

    if args.overlap > args.length:
        parser.error(f'overlap "{args.overlap}"'
                     f' cannot be greater than length "{args.length}"')

    return Args(args.genome, args.out_dir, args.length, args.overlap)


# --------------------------------------------------
def warn(msg) -> None:
    """ Print a message to STDERR """
    print(msg, file=sys.stderr)


# --------------------------------------------------
def die(msg='Fatal error') -> None:
    """ warn() and exit with error """
    warn(msg)
    sys.exit(1)


# --------------------------------------------------
def main() -> None:
    """ The good stuff """

    args = get_args()
    files = args.genome
    out_dir = args.out_dir
    length = args.length
    overlap = args.overlap

    if not os.path.isdir(out_dir):
        os.makedirs(out_dir)

    for fh in files:
        seq_record = SeqIO.read(fh, "fasta")

        seq_len = len(seq_record)
        min_overlap = 2*length - seq_len

        if length >= seq_len:
            die(f'Error: length "{length}" greater than'
                f' sequence ({seq_record.id}) length ({seq_len})')
        elif overlap < min_overlap:
            die(f'Error: overlap "{overlap}" less than minimum overlap:'
                f' {min_overlap} \n\tminimum overlap =  2 * length - seq_len'
                f' (2*{length}-{seq_len}={min_overlap})')

        print(f'Sequence id is: {seq_record}')


# --------------------------------------------------
def chop(in_record: SeqRecord, frag: int, overlap: int) -> SeqRecord:
    """ Chop sequence from seq_record """

    starts, stops = get_positions(len(in_record.seq), frag, overlap)

    for start, stop in zip(starts, stops):
        frag = in_record.seq[start, stop]


# --------------------------------------------------
def get_positions(length: int, frag: int, overlap: int) -> List:
    """ Get starting and stopping positions """

    starts = [0]
    stops = [frag-1]

    stop = stops[-1]
    while stop < length - 1:
        start = starts[-1] + frag - overlap
        stop = start + frag - 1

        if stop <= length - 1:
            starts.append(start)
            stops.append(stop)

    return (starts, stops)


# --------------------------------------------------
def test_get_positions():
    """ Test get_positions """

    assert get_positions(4, 2, 1) == ([0, 1, 2], [1, 2, 3])
    assert get_positions(4, 2, 0) == ([0, 2], [1, 3])
    assert get_positions(4, 3, 2) == ([0, 1], [2, 3])
    assert get_positions(5, 4, 3) == ([0, 1], [3, 4])
    assert get_positions(5, 3, 2) == ([0, 1, 2], [2, 3, 4])
    assert get_positions(5, 3, 1) == ([0, 2], [2, 4])
    assert get_positions(5, 2, 1) == ([0, 1, 2, 3], [1, 2, 3, 4])
    assert get_positions(5, 2, 0) == ([0, 2], [1, 3])


# --------------------------------------------------
def find_gc(seq: str) -> float:
    """ Calculate GC Content """

    return (seq.upper().count('C') + seq.upper().count('G')
            ) * 100 / len(seq) if seq else 0


# --------------------------------------------------
def test_find_gc():
    """ Test find_gc """

    assert find_gc('') == 0.
    assert find_gc('C') == 100.
    assert find_gc('G') == 100.
    assert find_gc('A') == 0.
    assert find_gc('T') == 0.
    assert find_gc('CGCG') == 100.
    assert find_gc('ATAT') == 0.
    assert find_gc('ATGC') == 50.


# --------------------------------------------------
if __name__ == '__main__':
    main()
