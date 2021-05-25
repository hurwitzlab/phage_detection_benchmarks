""" Tests """

from subprocess import getstatusoutput
import platform
import os
import re

PRG = './chopper.py'
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

    rv, out = getstatusoutput(f'{RUN} {TEST1} -l foo')
    assert rv != 0
    assert out.lower().startswith('usage:')

    rv, out = getstatusoutput(f'{RUN} {TEST1} -l 0')
    assert rv != 0
    assert out.lower().startswith('usage:')

    rv, out = getstatusoutput(f'{RUN} {TEST1} -l 6400')
    assert rv != 0
    assert out.lower().startswith('error:')

# --------------------------------------------------
def test_bad_overlap() -> None:
    """ Dies with bad overlap """

    rv, out = getstatusoutput(f'{RUN} {TEST1} -v foo')
    assert rv != 0
    assert out.lower().startswith('usage:')

    rv, out = getstatusoutput(f'{RUN} {TEST1} -l 200 -v 250')
    assert rv != 0
    assert out.lower().startswith('usage:')

    rv, out = getstatusoutput(f'{RUN} {TEST1} -l 3300 -v 100')
    assert rv != 0
    assert out.lower().startswith('error:')