""" Tests """

import os
from subprocess import getstatusoutput

PRG = './genome_selector.py'


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
def test_ok():
    """ OK """

    retval, out = getstatusoutput(f'{PRG} ')
    assert retval == 0
    assert out.splitlines()[-1] == 'positional = "foo"'
