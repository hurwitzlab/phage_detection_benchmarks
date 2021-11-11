""" Tests """

import os
import re
import shutil
from subprocess import getstatusoutput
from typing import List

PRG = './fa_to_gb.py'
INPUT1 = 'tests/inputs/input1.fasta'
INPUT2 = 'tests/inputs/input2.fasta'


# --------------------------------------------------
def test_exists():
    """ Program exists """

    assert os.path.isfile(PRG)


# --------------------------------------------------
def test_usage():
    """ Usage """

    for flag in ['-h', '--help']:
        retval, out = getstatusoutput(f'{PRG} {flag}')
        assert retval == 0
        assert out.lower().startswith('usage')


# --------------------------------------------------
def test_bad_file():
    """ Bad input file """

    retval, out = getstatusoutput(f'{PRG} -l 500 -a bacteria shimmy.txt')
    assert retval != 0
    assert out.lower().startswith('usage:')
    assert re.search('No such file', out)


def run(files: List):
    """ Run the program and check it runs well """

    out_dir = 'out_test'

    try:
        if os.path.isdir(out_dir):
            shutil.rmtree(out_dir)

        rv, out = getstatusoutput(f'{PRG} -o {out_dir} {" ".join(files)}')

        assert rv == 0

        plural = 's' if len(files) > 1 else ''
        assert re.search(f'Wrote {len(files)} file{plural} to {out_dir}.', out)

        assert os.path.isdir(out_dir)

        for file in files:
            base, _ = os.path.splitext(os.path.basename(file))
            out_name = base + '.gb'
            out_file = os.path.join(out_dir, out_name)

            assert os.path.isfile(out_file)
            with open(out_file) as fh:
                assert 'LOCUS' in fh.readline()

    finally:
        if os.path.isdir(out_dir):
            shutil.rmtree(out_dir)


# --------------------------------------------------
def test_runs_file1():
    """ Runs with first input file """

    run([INPUT1])


# --------------------------------------------------
def test_runs_file2():
    """ Runs with first input file """

    run([INPUT2])


# --------------------------------------------------
def test_runs_multiple():
    """ Runs with first input file """

    run([INPUT1, INPUT2])
