""" Tests """

import os
import random
import re
import shutil
from subprocess import getstatusoutput

PRG = './genome_selector.py'
TEST1 = 'tests/inputs/genomes/non_viral'
TEST2 = 'tests/inputs/genomes/viral'


# --------------------------------------------------
def test_exists() -> None:
    """ Program exists """

    assert os.path.isfile(PRG)


# --------------------------------------------------
def test_usage() -> None:
    """ Usage """

    for flag in ['-h', '--help']:
        retval, out = getstatusoutput(f'{PRG} {flag}')
        assert retval == 0
        assert out.lower().startswith('usage')


# --------------------------------------------------
def test_no_input() -> None:
    """ Fails on missing input directory """

    retval, out = getstatusoutput(f'{PRG}')
    assert retval != 0
    assert out.lower().startswith('usage:')
    assert re.search('required: dir', out)


# --------------------------------------------------
def test_bad_input() -> None:
    """ Fails on bad input directory """

    retval, out = getstatusoutput(f'{PRG} gargle')
    assert retval != 0
    assert out.lower().startswith('usage:')
    assert re.search('directory "gargle" does not exist', out)


# --------------------------------------------------
def test_bad_number() -> None:
    """ Fails on bad num_genomes """

    retval, out = getstatusoutput(f'{PRG} {TEST1} -n foo')
    assert retval != 0
    assert out.lower().startswith('usage:')
    assert re.search('invalid int value: \'foo\'', out)

    bad_num = random.randint(-100, 0)

    retval, out = getstatusoutput(f'{PRG} {TEST1} -n {bad_num}')
    assert retval != 0
    assert out.lower().startswith('usage:')
    assert re.search(r'Number of genomes \(-?\d+\)', out)


# --------------------------------------------------
def test_ok() -> None:
    """ Runs on good input """

    out_dir = 'out_test'
    out_fasta = os.path.join(out_dir, 'selected_genomes.fasta')
    out_txt = os.path.join(out_dir, 'selected_genome_files.txt')
    try:
        if os.path.isdir(out_dir):
            shutil.rmtree(out_dir)

        # -n less than number of files
        rv, out = getstatusoutput(f'{PRG} {TEST1} -n 2 -o {out_dir}')

        assert out == (f'Done. Wrote 2 records to {out_fasta}.')
        assert rv == 0
        assert os.path.isdir(out_dir)
        assert os.path.isfile(out_fasta)
        assert os.path.isfile(out_txt)
        assert open(out_fasta).read().count('>') == 2
        assert open(out_txt).read().count('\n') == 2

    finally:
        if os.path.isdir(out_dir):
            shutil.rmtree(out_dir)


# --------------------------------------------------
def test_warns_too_many() -> None:
    """ Warns on too large num """

    out_dir = 'out_test'
    out_fasta = os.path.join(out_dir, 'selected_genomes.fasta')
    out_txt = os.path.join(out_dir, 'selected_genome_files.txt')
    try:
        if os.path.isdir(out_dir):
            shutil.rmtree(out_dir)

        # No replacement, so number of genomes limited to number of files
        rv, out = getstatusoutput(f'{PRG} {TEST1} -n 20 -o {out_dir}')

        assert re.search(r'Number of requested genomes \(\d+\)', out)
        assert rv == 0
        assert os.path.isdir(out_dir)
        assert os.path.isfile(out_fasta)
        assert os.path.isfile(out_txt)
        assert open(out_fasta).read().count('>') == 6
        assert open(out_txt).read().count('\n') == 6

    finally:
        if os.path.isdir(out_dir):
            shutil.rmtree(out_dir)
