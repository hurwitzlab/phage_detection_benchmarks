""" Tests """

import os
import platform
import random
import re
import shutil
import string
from subprocess import getstatusoutput

PRG = './contig_filter.py'
RUN = f'python {PRG}' if platform.system() == 'Windows' else PRG
TEST1 = ('./tests/inputs/input1.fasta')


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
def test_no_args() -> None:
    """ Dies on no args """

    rv, out = getstatusoutput(RUN)
    assert rv != 0
    assert re.match("usage", out, re.IGNORECASE)


# --------------------------------------------------
def test_bad_file() -> None:
    """ Dies with nonexistent file """

    rv, out = getstatusoutput(f'{RUN} foo')
    assert rv != 0
    assert out.lower().startswith('usage:')


# --------------------------------------------------
def test_bad_length() -> None:
    """ Dies with bad length """

    # String for length argument
    rv, out = getstatusoutput(f'{RUN} {TEST1} -l foo')
    assert rv != 0
    assert out.lower().startswith('usage:')

    # Fragment length = 0
    rv, out = getstatusoutput(f'{RUN} {TEST1} -l 0')
    assert rv != 0
    assert out.lower().startswith('usage:')


# --------------------------------------------------
def test_okay() -> None:
    """ Runs on good input """

    out_dir = random_string()
    try:
        if os.path.isdir(out_dir):
            shutil.rmtree(out_dir)

        rv, out = getstatusoutput(f'{RUN} {TEST1} -o {out_dir}')

        assert rv == 0
        assert out == (
            f'Wrote 1 sequence (out of 3) to {out_dir}/input1.fasta\n'
            f'Done. Wrote 1 file to {out_dir}.')
        assert os.path.isdir(out_dir)
        out_file = os.path.join(out_dir, 'input1.fasta')
        assert os.path.isfile(out_file)
        assert open(out_file).read().count('>') == 1

    finally:
        if os.path.isdir(out_dir):
            shutil.rmtree(out_dir)


# ---------------------------------------------------------------------------
def random_string() -> str:
    """ Generate a random string """

    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
