#!/usr/bin/env python3
"""
Author : Kenneth Schackart <schackartk1@gmail.com>
Date   : 2021-05-25
Purpose: Chop a genome into simulated contigs
"""

import argparse
import os
import sys
from typing import List, NamedTuple, TextIO, TypedDict
from Bio import SeqIO
# from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord


class Args(NamedTuple):
    """ Command-line arguments """
    genome: List[TextIO]
    out_dir: str
    length: int
    overlap: int


# --------------------------------------------------
class SeqAnnotations(TypedDict):
    """ SeqRecord Annotations """
    parent_id: str
    parent_name: str
    frag_start: int
    frag_end: int
    gc_pct: float


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

        frag_recs = chop(seq_record, length, overlap)

        out_file_base = os.path.splitext(os.path.basename(fh.name))[0]
        out_file_fa = os.path.join(out_dir,  out_file_base + '_frags.fasta')
        out_file_tsv = os.path.join(out_dir,  out_file_base + '_frags.tsv')

        n_rec = SeqIO.write(frag_recs, out_file_fa, "fasta")

        write_annotations(frag_recs, out_file_tsv)

        print(f'Done. Wrote {n_rec} records to "{out_file_fa}".')


# --------------------------------------------------
def chop(record: SeqRecord, frag_len: int, overlap: int) -> List[SeqRecord]:
    """ Chop sequence from record """

    starts, stops = get_positions(len(record.seq), frag_len, overlap)

    frag_recs = []
    n_frag = 0

    for start, stop in zip(starts, stops):
        n_frag += 1
        frag = record.seq[start: stop]

        frag_annotations = SeqAnnotations(parent_id=record.id,
                                          parent_name=record.description,
                                          frag_start=start + 1,
                                          frag_end=stop + 1,
                                          gc_pct=find_gc(frag)
                                          )

        frag_rec = SeqRecord(frag, id=f'{record.id}_frag{n_frag}',
                             description=f'Fragment {n_frag}'
                                         f' of {record. description}',
                                         annotations=frag_annotations
                             )

        frag_recs.append(frag_rec)

    return frag_recs


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
def write_annotations(frag_recs, out_file):
    """ Write fragment annotations to .tsv """

    with open(out_file, 'wt') as out_fh:
        print('id\tparent_id\tparent_name\tfrag_start\tfrag_end\tgc_pct',
              file=out_fh)

        for rec in frag_recs:
            print(rec.id, *rec.annotations.values(),
                  sep='\t', file=out_fh)

        out_fh.close()


# --------------------------------------------------
if __name__ == '__main__':
    main()
