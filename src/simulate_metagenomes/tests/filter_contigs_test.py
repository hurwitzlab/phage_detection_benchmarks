""" Tests """

import os
import random
import re
import shutil
import string
from subprocess import getstatusoutput

PRG = './filter_contigs.py'
INPUT = 'tests/inputs/filter_contigs/final.contigs.fa'


# --------------------------------------------------
def test_exists() -> None:
    """ Program exists """

    assert os.path.isfile(PRG)


# --------------------------------------------------
def test_testing_environment() -> None:
    """ Test files are in place """

    assert os.path.isfile(INPUT)


# --------------------------------------------------
def test_usage() -> None:
    """ Usage """

    for flag in ['-h', '--help']:
        retval, out = getstatusoutput(f'{PRG} {flag}')
        assert retval == 0
        assert out.lower().startswith('usage')


# --------------------------------------------------
def test_bad_file() -> None:
    """ Run with a bad input file """

    bad = random_string()

    retval, out = getstatusoutput(f'{PRG} -l 300 {bad}')
    assert retval != 0
    assert out.lower().startswith('usage:')
    assert re.search('No such file', out)


# --------------------------------------------------
def run(length: int, tol: float, exp: int) -> None:
    """ Run the program """

    out_dir = random_string()

    try:
        if os.path.isdir(out_dir):
            shutil.rmtree(out_dir)

        rv, out = getstatusoutput(f'{PRG} -o {out_dir} -l {length} '
                                  f'-t {tol} {INPUT}')

        assert rv == 0
        out_file = os.path.join(out_dir, 'filtered_contigs.fa')
        assert re.search(f'Done. Wrote output to {out_file}', out)
        assert os.path.isdir(out_dir)
        assert os.path.isfile(out_file)
        out_contigs = open(out_file).read().count('>')
        assert out_contigs == exp

    finally:
        if os.path.isdir(out_dir):
            shutil.rmtree(out_dir)


# --------------------------------------------------
def test_runs_okay() -> None:
    """ Runs with valid input """

    run(300, 0., 5)
    run(300, 0.05, 2)


# --------------------------------------------------
def random_string() -> str:
    """ Generate a random string """

    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
