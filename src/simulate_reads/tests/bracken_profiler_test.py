""" Tests """

import os
import random
import re
import string
from subprocess import getstatusoutput

PRG = "./bracken_profiler.py"
INPUT1 = "tests/inputs/bracken_profiler/input_1.txt"
INPUT2 = "tests/inputs/bracken_profiler/input_1.txt"
TAX = "tests/inputs/bracken_profiler/input_1.txt"


# --------------------------------------------------
def test_exists():
    """Program exists"""

    assert os.path.isfile(PRG)


# --------------------------------------------------
def test_testing_environment():
    """Test files are in place"""

    assert os.path.isfile(INPUT1)
    assert os.path.isfile(INPUT2)
    assert os.path.isfile(TAX)


# --------------------------------------------------
def test_usage():
    """Usage"""

    for flag in ["-h", "--help"]:
        retval, out = getstatusoutput(f"{PRG} {flag}")
        assert retval == 0
        assert out.lower().startswith("usage")


# --------------------------------------------------
def test_bad_file():
    """Bad input file"""

    bad = random_string()

    retval, out = getstatusoutput(f"{PRG} -t {TAX} {bad}")
    assert retval != 0
    assert out.lower().startswith("usage:")
    assert re.search("No such file", out)
    assert re.search(bad, out)


# --------------------------------------------------
def test_bad_taxonomy_file():
    """Bad input file"""

    bad = random_string()

    retval, out = getstatusoutput(f"{PRG} -t {bad} {INPUT1}")
    assert retval != 0
    assert out.lower().startswith("usage:")
    assert re.search("No such file", out)
    assert re.search(bad, out)


# --------------------------------------------------
def random_string() -> str:
    """Generate a random string"""

    return "".join(random.choices(string.ascii_uppercase + string.digits, k=5))
