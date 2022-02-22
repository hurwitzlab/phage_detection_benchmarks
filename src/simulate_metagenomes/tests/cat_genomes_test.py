""" Tests """

import os
import random
import re
import shutil
import string
from subprocess import getstatusoutput

PRG = './cat_genomes.py'
INPUT1 = 'tests/inputs/cat_genomes/input_1_files.txt'
REFSEQ = 'tests/inputs/cat_genomes/refseq'


# --------------------------------------------------
def test_exists():
    """ Program exists """

    assert os.path.isfile(PRG)


# --------------------------------------------------
def test_testing_environment():
    """ Test files are in place """

    assert os.path.isfile(INPUT1)
    assert os.path.isdir(REFSEQ)

    for kingdom in ['archaea', 'bacteria', 'fungi', 'viral']:
        kingdom_dir = os.path.join(REFSEQ, kingdom)
        assert os.path.isdir(kingdom_dir)
        assert len(os.listdir(kingdom_dir)) != 0


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

    bad = random_string()

    retval, out = getstatusoutput(f'{PRG} -p {REFSEQ} {bad}')
    assert retval != 0
    assert out.lower().startswith('usage:')
    assert re.search('No such file', out)
    assert re.search(bad, out)


# --------------------------------------------------
def test_missing_parent():
    """ Parent directory doesn't exist """

    bad = random_string()

    retval, out = getstatusoutput(f'{PRG} -p {bad} {INPUT1}')
    assert retval != 0
    assert out.lower().startswith('usage:')
    assert re.search('is not a directory', out)
    assert re.search(bad, out)


# --------------------------------------------------
def test_empty_parent():
    """ Parent directory is empty """

    bad = random_string()

    try:
        if os.path.isdir(bad):
            shutil.rmtree(bad)

        os.mkdir(bad)

        retval, out = getstatusoutput(f'{PRG} -p {bad} {INPUT1}')
        assert retval != 0
        assert out.lower().startswith('usage:')
        assert re.search('is empty', out)
        assert re.search(bad, out)

    finally:
        if os.path.isdir(bad):
            shutil.rmtree(bad)


# --------------------------------------------------
def test_wrong_parent():
    """ Parent directory doesn't lead to genomes """

    retval, out = getstatusoutput(f'{PRG} -p tests {INPUT1}')
    assert retval != 0
    assert re.search('Error:', out)
    assert re.search('"tests"', out)


# --------------------------------------------------
def test_runs_okay():
    """ Runs with good input """

    out_dir = random_string()

    try:
        if os.path.isdir(out_dir):
            shutil.rmtree(out_dir)

        rv, out = getstatusoutput(f'{PRG} -p {REFSEQ} -o {out_dir} {INPUT1}')

        assert rv == 0
        out_file = os.path.join(out_dir, 'input_1_genomes.fasta')
        assert re.search('Done. Concatenated files for 1 profile.', out)
        assert os.path.isdir(out_dir)
        assert os.path.isfile(out_file)
        glob_lines = open(INPUT1).read().count('\n')
        records = open(out_file).read().count('>')
        assert records == glob_lines - 1

    finally:
        if os.path.isdir(out_dir):
            shutil.rmtree(out_dir)


# --------------------------------------------------
def random_string() -> str:
    """ Generate a random string """

    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
