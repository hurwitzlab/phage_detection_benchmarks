""" Tests """

import os
import random
import re
import shutil
from subprocess import getstatusoutput

PRG = './selector.py'
TEST1 = 'tests/inputs/chopped/archaea/5'
TEST2 = 'tests/inputs/chopped/archaea/50'


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
    """ Fails on bad num_frags """

    retval, out = getstatusoutput(f'{PRG} {TEST1} -n foo')
    assert retval != 0
    assert out.lower().startswith('usage:')
    assert re.search('invalid int value: \'foo\'', out)

    bad_num = random.randint(-100, 0)

    retval, out = getstatusoutput(f'{PRG} {TEST1} -n {bad_num}')
    assert retval != 0
    assert out.lower().startswith('usage:')
    assert re.search(r'Number of fragments \(-?\d+\)', out)


# --------------------------------------------------
def test_ok() -> None:
    """ Runs on good input """

    out_dir = 'out_test'
    out_file = os.path.join(out_dir, 'selected_frags.fasta')
    try:
        if os.path.isdir(out_dir):
            shutil.rmtree(out_dir)

        # -n less than number of files
        rv, out = getstatusoutput(f'{PRG} {TEST1} -n 2 -o {out_dir}')

        assert out == (f'Done. Wrote 2 records to {out_file}.')
        assert rv == 0
        assert os.path.isdir(out_dir)
        assert os.path.isfile(out_file)
        assert open(out_file).read().count('>') == 2

        # -n more than number of files, with replacement
        rv, out = getstatusoutput(f'{PRG} {TEST1} -n 20 -o {out_dir} -r')

        assert out == (f'Done. Wrote 20 records to {out_file}.')
        assert rv == 0
        assert os.path.isdir(out_dir)
        assert os.path.isfile(out_file)
        assert open(out_file).read().count('>') == 20

    finally:
        if os.path.isdir(out_dir):
            shutil.rmtree(out_dir)


# --------------------------------------------------
def test_warns_too_many() -> None:
    """ Warns on too large num_frags """

    out_dir = 'out_test'
    out_file = os.path.join(out_dir, 'selected_frags.fasta')
    try:
        if os.path.isdir(out_dir):
            shutil.rmtree(out_dir)

        # No replacement, so number of frags limited to number of files
        rv, out = getstatusoutput(f'{PRG} {TEST1} -n 20 -o {out_dir}')

        assert re.search(r'Number of requested fragments \(\d+\)', out)
        assert rv == 0
        assert os.path.isdir(out_dir)
        assert os.path.isfile(out_file)
        assert open(out_file).read().count('>') == 2

        # With replacement, number of frags limited to all frags in all files
        rv, out = getstatusoutput(f'{PRG} {TEST2} -n 100 -o {out_dir} -r')

        assert re.search(r'Unable to find \d+ unique', out)
        assert rv == 0
        assert os.path.isdir(out_dir)
        assert os.path.isfile(out_file)
        assert open(out_file).read().count('>') == 6

    finally:
        if os.path.isdir(out_dir):
            shutil.rmtree(out_dir)
