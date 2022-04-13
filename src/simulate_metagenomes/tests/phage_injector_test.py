""" Tests for phage injector script """

import pandas as pd
from phage_injector import supplement_phage
from pandas.testing import assert_frame_equal


# ---------------------------------------------------------------------------
def test_case1() -> None:
    """
    Phages present
    None have present hosts
    num >= num_pahge
    """

    profile = pd.DataFrame(
        [[0.99, 'bacteria', 'Thermus', 'Thermus thermophilus', 'GCF1', 123],
         [0.0025, 'viral', '', 'Bacillus phage Fah', 'GCF10', 951],
         [0.0075, 'viral', '', 'Salmonella phage g341c', 'GCF7', 147]],
        columns=[
            'rescaled_abundance', 'kingdom', 'genus', 'species', 'accession',
            'taxid'
        ])

    tax = pd.DataFrame(
        [['bacteria', 'Thermus', 'Thermus thermophilus', 'GCF1', 123],
         ['viral', '', 'Salmonella phage g341c', 'GCF7', 147],
         ['viral', '', 'Bacillus phage Fah', 'GCF10', 951]],
        columns=['kingdom', 'genus', 'species', 'accession', 'taxid'])

    out_df = pd.DataFrame(
        [[0.95, 'bacteria', 'Thermus', 'Thermus thermophilus', 'GCF1', 123],
         [0.0125, 'viral', '', 'Bacillus phage Fah', 'GCF10', 951],
         [0.0375, 'viral', '', 'Salmonella phage g341c', 'GCF7', 147]],
        columns=[
            'rescaled_abundance', 'kingdom', 'genus', 'species', 'accession',
            'taxid'
        ])

    assert_frame_equal(supplement_phage(profile, tax, 0.05, 1),
                       out_df,
                       check_dtype=False)


# ---------------------------------------------------------------------------
def test_case2() -> None:
    """
    Phages present
    None have present hosts
    num < num_pahge
    Phage found for hosts
    """

    profile = pd.DataFrame(
        [[0.99, 'bacteria', 'Thermus', 'Thermus thermophilus', 'GCF1', 123],
         [0.0025, 'viral', '', 'Bacillus phage Fah', 'GCF10', 951],
         [0.0075, 'viral', '', 'Salmonella phage g341c', 'GCF7', 147]],
        columns=[
            'rescaled_abundance', 'kingdom', 'genus', 'species', 'accession',
            'taxid'
        ])

    tax = pd.DataFrame(
        [['bacteria', 'Thermus', 'Thermus thermophilus', 'GCF1', 123],
         ['viral', '', 'Salmonella phage g341c', 'GCF7', 147],
         ['viral', '', 'Bacillus phage Fah', 'GCF10', 951],
         ['viral', '', 'Thermus phage TMA', 'GCF9', 369]],
        columns=['kingdom', 'genus', 'species', 'accession', 'taxid'])

    out_df = pd.DataFrame(
        [[0.95, 'bacteria', 'Thermus', 'Thermus thermophilus', 'GCF1', 123],
         [0.0025, 'viral', '', 'Bacillus phage Fah', 'GCF10', 951],
         [0.0075, 'viral', '', 'Salmonella phage g341c', 'GCF7', 147],
         [0.04, 'viral', '', 'Thermus phage TMA', 'GCF9', 369]],
        columns=[
            'rescaled_abundance', 'kingdom', 'genus', 'species', 'accession',
            'taxid'
        ])

    assert_frame_equal(supplement_phage(profile, tax, 0.05, 3),
                       out_df,
                       check_dtype=False)


# ---------------------------------------------------------------------------
def test_case3() -> None:
    """
    Phages present
    None have present hosts
    num < num_pahge
    No phage found for hosts
    """

    profile = pd.DataFrame(
        [[0.99, 'bacteria', 'Thermus', 'Thermus thermophilus', 'GCF1', 123],
         [0.0025, 'viral', '', 'Bacillus phage Fah', 'GCF10', 951],
         [0.0075, 'viral', '', 'Salmonella phage g341c', 'GCF7', 147]],
        columns=[
            'rescaled_abundance', 'kingdom', 'genus', 'species', 'accession',
            'taxid'
        ])

    tax = pd.DataFrame(
        [['bacteria', 'Thermus', 'Thermus thermophilus', 'GCF1', 123],
         ['viral', '', 'Salmonella phage g341c', 'GCF7', 147],
         ['viral', '', 'Bacillus phage Fah', 'GCF10', 951]],
        columns=['kingdom', 'genus', 'species', 'accession', 'taxid'])

    out_df = pd.DataFrame(
        [[0.95, 'bacteria', 'Thermus', 'Thermus thermophilus', 'GCF1', 123],
         [0.0125, 'viral', '', 'Bacillus phage Fah', 'GCF10', 951],
         [0.0375, 'viral', '', 'Salmonella phage g341c', 'GCF7', 147]],
        columns=[
            'rescaled_abundance', 'kingdom', 'genus', 'species', 'accession',
            'taxid'
        ])

    assert_frame_equal(supplement_phage(profile, tax, 0.05, 3),
                       out_df,
                       check_dtype=False)


# ---------------------------------------------------------------------------
def test_case4() -> None:
    """
    Phages present
    All have present hosts
    num >= num_phage
    """

    profile = pd.DataFrame(
        [[0.66, 'bacteria', 'Thermus', 'Thermus thermophilus', 'GCF1', 123],
         [0.33, 'bacteria', 'Salmonella', 'Salmonella enterica', 'GCF2', 456],
         [0.0025, 'viral', '', 'Thermus phage TMA', 'GCF9', 369],
         [0.0075, 'viral', '', 'Salmonella phage g341c', 'GCF7', 147]],
        columns=[
            'rescaled_abundance', 'kingdom', 'genus', 'species', 'accession',
            'taxid'
        ])

    tax = pd.DataFrame(
        [['bacteria', 'Thermus', 'Thermus thermophilus', 'GCF1', 123],
         ['viral', '', 'Salmonella phage g341c', 'GCF7', 147],
         ['viral', '', 'Bacillus phage Fah', 'GCF10', 951]],
        columns=['kingdom', 'genus', 'species', 'accession', 'taxid'])

    out_df = pd.DataFrame([[
        0.63333, 'bacteria', 'Thermus', 'Thermus thermophilus', 'GCF1', 123
    ], [0.31667, 'bacteria', 'Salmonella', 'Salmonella enterica', 'GCF2', 456
        ], [0.03333, 'viral', '', 'Thermus phage TMA', 'GCF9', 369
            ], [0.01667, 'viral', '', 'Salmonella phage g341c', 'GCF7', 147]],
                          columns=[
                              'rescaled_abundance', 'kingdom', 'genus',
                              'species', 'accession', 'taxid'
                          ])

    assert_frame_equal(supplement_phage(profile, tax, 0.05, 1),
                       out_df,
                       check_dtype=False)


# ---------------------------------------------------------------------------
def test_case5() -> None:
    """
    Phages present
    All have present hosts
    num < num_phage
    Phage found for hosts
    """

    profile = pd.DataFrame(
        [[0.66, 'bacteria', 'Thermus', 'Thermus thermophilus', 'GCF1', 123],
         [0.33, 'bacteria', 'Salmonella', 'Salmonella enterica', 'GCF2', 456],
         [0.01, 'viral', '', 'Thermus phage TMA', 'GCF9', 369]],
        columns=[
            'rescaled_abundance', 'kingdom', 'genus', 'species', 'accession',
            'taxid'
        ])

    tax = pd.DataFrame(
        [['bacteria', 'Thermus', 'Thermus thermophilus', 'GCF1', 123],
         ['bacteria', 'Salmonella', 'Salmonella enterica', 'GCF2', 456],
         ['viral', '', 'Thermus phage TMA', 'GCF9', 369],
         ['viral', '', 'Salmonella phage g341c', 'GCF7', 147]],
        columns=['kingdom', 'genus', 'species', 'accession', 'taxid'])

    out_df = pd.DataFrame([[
        0.63333, 'bacteria', 'Thermus', 'Thermus thermophilus', 'GCF1', 123
    ], [0.31667, 'bacteria', 'Salmonella', 'Salmonella enterica', 'GCF2', 456
        ], [0.03333, 'viral', '', 'Thermus phage TMA', 'GCF9', 369
            ], [0.01667, 'viral', '', 'Salmonella phage g341c', 'GCF7', 147]],
                          columns=[
                              'rescaled_abundance', 'kingdom', 'genus',
                              'species', 'accession', 'taxid'
                          ])

    assert_frame_equal(supplement_phage(profile, tax, 0.05, 2),
                       out_df,
                       check_dtype=False)


# ---------------------------------------------------------------------------
def test_case6() -> None:
    """
    Phages present
    All have present hosts
    num < num_phage
    No phage found for hosts
    """

    profile = pd.DataFrame(
        [[0.66, 'bacteria', 'Thermus', 'Thermus thermophilus', 'GCF1', 123],
         [0.33, 'bacteria', 'Salmonella', 'Salmonella enterica', 'GCF2', 456],
         [0.01, 'viral', '', 'Thermus phage TMA', 'GCF9', 369]],
        columns=[
            'rescaled_abundance', 'kingdom', 'genus', 'species', 'accession',
            'taxid'
        ])

    tax = pd.DataFrame(
        [['bacteria', 'Thermus', 'Thermus thermophilus', 'GCF1', 123],
         ['bacteria', 'Salmonella', 'Salmonella enterica', 'GCF2', 456],
         ['viral', '', 'Thermus phage TMA', 'GCF9', 369]],
        columns=['kingdom', 'genus', 'species', 'accession', 'taxid'])

    out_df = pd.DataFrame([[
        0.63333, 'bacteria', 'Thermus', 'Thermus thermophilus', 'GCF1', 123
    ], [0.31667, 'bacteria', 'Salmonella', 'Salmonella enterica', 'GCF2', 456
        ], [0.05, 'viral', '', 'Thermus phage TMA', 'GCF9', 369]],
                          columns=[
                              'rescaled_abundance', 'kingdom', 'genus',
                              'species', 'accession', 'taxid'
                          ])

    assert_frame_equal(supplement_phage(profile, tax, 0.05, 2),
                       out_df,
                       check_dtype=False)


# ---------------------------------------------------------------------------
def test_case7() -> None:
    """
    Phages present
    Some have present hosts
    num < num_phage
    Phages found for hosts
    """

    profile = pd.DataFrame(
        [[0.66, 'bacteria', 'Thermus', 'Thermus thermophilus', 'GCF1', 123],
         [0.33, 'bacteria', 'Salmonella', 'Salmonella enterica', 'GCF2', 456],
         [0.004, 'viral', '', 'Thermus phage TMA', 'GCF9', 369],
         [0.006, 'viral', '', 'Escherichia phage D108', 'GCF6', 963]],
        columns=[
            'rescaled_abundance', 'kingdom', 'genus', 'species', 'accession',
            'taxid'
        ])

    tax = pd.DataFrame(
        [['bacteria', 'Thermus', 'Thermus thermophilus', 'GCF1', 123],
         ['bacteria', 'Salmonella', 'Salmonella enterica', 'GCF2', 456],
         ['viral', '', 'Thermus phage TMA', 'GCF9', 369],
         ['viral', '', 'Escherichia phage D108', 'GCF6', 963],
         ['viral', '', 'Salmonella phage g341c', 'GCF7', 147]],
        columns=['kingdom', 'genus', 'species', 'accession', 'taxid'])

    out_df = pd.DataFrame([[
        0.63333, 'bacteria', 'Thermus', 'Thermus thermophilus', 'GCF1', 123
    ], [
        0.31667, 'bacteria', 'Salmonella', 'Salmonella enterica', 'GCF2', 456
    ], [0.006, 'viral', '', 'Escherichia phage D108', 'GCF6', 963
        ], [0.02933, 'viral', '', 'Thermus phage TMA', 'GCF9', 369
            ], [0.01467, 'viral', '', 'Salmonella phage g341c', 'GCF7', 147]],
                          columns=[
                              'rescaled_abundance', 'kingdom', 'genus',
                              'species', 'accession', 'taxid'
                          ])

    assert_frame_equal(supplement_phage(profile, tax, 0.05, 4),
                       out_df,
                       check_dtype=False)


# ---------------------------------------------------------------------------
def test_case8() -> None:
    """
    Phages present
    Some have present hosts
    num < num_phage
    No phages found for hosts
    """

    profile = pd.DataFrame(
        [[0.66, 'bacteria', 'Thermus', 'Thermus thermophilus', 'GCF1', 123],
         [0.33, 'bacteria', 'Salmonella', 'Salmonella enterica', 'GCF2', 456],
         [0.002, 'viral', '', 'Thermus phage TMA', 'GCF9', 369],
         [0.007, 'viral', '', 'Escherichia phage D108', 'GCF6', 963],
         [0.001, 'viral', '', 'Salmonella phage g341c', 'GCF7', 147]],
        columns=[
            'rescaled_abundance', 'kingdom', 'genus', 'species', 'accession',
            'taxid'
        ])

    tax = pd.DataFrame(
        [['bacteria', 'Thermus', 'Thermus thermophilus', 'GCF1', 123],
         ['bacteria', 'Salmonella', 'Salmonella enterica', 'GCF2', 456],
         ['viral', '', 'Thermus phage TMA', 'GCF9', 369],
         ['viral', '', 'Escherichia phage D108', 'GCF6', 963],
         ['viral', '', 'Salmonella phage g341c', 'GCF7', 147]],
        columns=['kingdom', 'genus', 'species', 'accession', 'taxid'])

    out_df = pd.DataFrame([[
        0.63333, 'bacteria', 'Thermus', 'Thermus thermophilus', 'GCF1', 123
    ], [
        0.31667, 'bacteria', 'Salmonella', 'Salmonella enterica', 'GCF2', 456
    ], [0.007, 'viral', '', 'Escherichia phage D108', 'GCF6', 963
        ], [0.02867, 'viral', '', 'Thermus phage TMA', 'GCF9', 369
            ], [0.01433, 'viral', '', 'Salmonella phage g341c', 'GCF7', 147]],
                          columns=[
                              'rescaled_abundance', 'kingdom', 'genus',
                              'species', 'accession', 'taxid'
                          ])

    assert_frame_equal(supplement_phage(profile, tax, 0.05, 4),
                       out_df,
                       check_dtype=False)


# ---------------------------------------------------------------------------
def test_case9() -> None:
    """
    Phages present
    Some have present hosts
    num >= num_phage
    hosted >= num_phage
    nonhosted < num_phage
    """

    profile = pd.DataFrame(
        [[0.66, 'bacteria', 'Thermus', 'Thermus thermophilus', 'GCF1', 123],
         [0.33, 'bacteria', 'Salmonella', 'Salmonella enterica', 'GCF2', 456],
         [0.002, 'viral', '', 'Thermus phage TMA', 'GCF9', 369],
         [0.007, 'viral', '', 'Escherichia phage D108', 'GCF6', 963],
         [0.001, 'viral', '', 'Salmonella phage g341c', 'GCF7', 147]],
        columns=[
            'rescaled_abundance', 'kingdom', 'genus', 'species', 'accession',
            'taxid'
        ])

    tax = pd.DataFrame(
        [['bacteria', 'Thermus', 'Thermus thermophilus', 'GCF1', 123],
         ['bacteria', 'Salmonella', 'Salmonella enterica', 'GCF2', 456],
         ['viral', '', 'Thermus phage TMA', 'GCF9', 369],
         ['viral', '', 'Escherichia phage D108', 'GCF6', 963],
         ['viral', '', 'Salmonella phage g341c', 'GCF7', 147]],
        columns=['kingdom', 'genus', 'species', 'accession', 'taxid'])

    out_df = pd.DataFrame([[
        0.63333, 'bacteria', 'Thermus', 'Thermus thermophilus', 'GCF1', 123
    ], [
        0.31667, 'bacteria', 'Salmonella', 'Salmonella enterica', 'GCF2', 456
    ], [0.007, 'viral', '', 'Escherichia phage D108', 'GCF6', 963
        ], [0.02867, 'viral', '', 'Thermus phage TMA', 'GCF9', 369
            ], [0.01433, 'viral', '', 'Salmonella phage g341c', 'GCF7', 147]],
                          columns=[
                              'rescaled_abundance', 'kingdom', 'genus',
                              'species', 'accession', 'taxid'
                          ])

    assert_frame_equal(supplement_phage(profile, tax, 0.05, 2),
                       out_df,
                       check_dtype=False)


# ---------------------------------------------------------------------------
def test_case10() -> None:
    """
    Phages present
    Some have present hosts
    num >= num_phage
    hosted < num_phage
    nonhosted >= num_phage
    """

    profile = pd.DataFrame(
        [[0.66, 'bacteria', 'Thermus', 'Thermus thermophilus', 'GCF1', 123],
         [0.33, 'bacteria', 'Borrelia', 'Borellia miyamotoi', 'GCF4', 741],
         [0.002, 'viral', '', 'Thermus phage TMA', 'GCF9', 369],
         [0.007, 'viral', '', 'Escherichia phage D108', 'GCF6', 963],
         [0.001, 'viral', '', 'Salmonella phage g341c', 'GCF7', 147]],
        columns=[
            'rescaled_abundance', 'kingdom', 'genus', 'species', 'accession',
            'taxid'
        ])

    tax = pd.DataFrame(
        [['bacteria', 'Thermus', 'Thermus thermophilus', 'GCF1', 123],
         ['bacteria', 'Borrelia', 'Borellia miyamotoi', 'GCF4', 741],
         ['viral', '', 'Thermus phage TMA', 'GCF9', 369],
         ['viral', '', 'Escherichia phage D108', 'GCF6', 963],
         ['viral', '', 'Salmonella phage g341c', 'GCF7', 147]],
        columns=['kingdom', 'genus', 'species', 'accession', 'taxid'])

    out_df = pd.DataFrame(
        [[0.63333, 'bacteria', 'Thermus', 'Thermus thermophilus', 'GCF1', 123],
         [0.31667, 'bacteria', 'Borrelia', 'Borellia miyamotoi', 'GCF4', 741],
         [0.007, 'viral', '', 'Escherichia phage D108', 'GCF6', 963],
         [0.001, 'viral', '', 'Salmonella phage g341c', 'GCF7', 147],
         [0.042, 'viral', '', 'Thermus phage TMA', 'GCF9', 369]],
        columns=[
            'rescaled_abundance', 'kingdom', 'genus', 'species', 'accession',
            'taxid'
        ])

    assert_frame_equal(supplement_phage(profile, tax, 0.05, 2),
                       out_df,
                       check_dtype=False)


# ---------------------------------------------------------------------------
def test_case11() -> None:
    """
    Phages present
    Some have present hosts
    num >= num_phage
    hosted >= num_phage
    nonhosted >= num_phage
    """

    profile = pd.DataFrame(
        [[0.66, 'bacteria', 'Thermus', 'Thermus thermophilus', 'GCF1', 123],
         [0.33, 'bacteria', 'Borrelia', 'Borellia miyamotoi', 'GCF4', 741],
         [0.002, 'viral', '', 'Thermus phage TMA', 'GCF9', 369],
         [0.007, 'viral', '', 'Escherichia phage D108', 'GCF6', 963],
         [0.001, 'viral', '', 'Salmonella phage g341c', 'GCF7', 147]],
        columns=[
            'rescaled_abundance', 'kingdom', 'genus', 'species', 'accession',
            'taxid'
        ])

    tax = pd.DataFrame(
        [['bacteria', 'Thermus', 'Thermus thermophilus', 'GCF1', 123],
         ['bacteria', 'Borrelia', 'Borellia miyamotoi', 'GCF4', 741],
         ['viral', '', 'Thermus phage TMA', 'GCF9', 369],
         ['viral', '', 'Escherichia phage D108', 'GCF6', 963],
         ['viral', '', 'Salmonella phage g341c', 'GCF7', 147]],
        columns=['kingdom', 'genus', 'species', 'accession', 'taxid'])

    out_df = pd.DataFrame(
        [[0.63333, 'bacteria', 'Thermus', 'Thermus thermophilus', 'GCF1', 123],
         [0.31667, 'bacteria', 'Borrelia', 'Borellia miyamotoi', 'GCF4', 741],
         [0.007, 'viral', '', 'Escherichia phage D108', 'GCF6', 963],
         [0.001, 'viral', '', 'Salmonella phage g341c', 'GCF7', 147],
         [0.042, 'viral', '', 'Thermus phage TMA', 'GCF9', 369]],
        columns=[
            'rescaled_abundance', 'kingdom', 'genus', 'species', 'accession',
            'taxid'
        ])

    assert_frame_equal(supplement_phage(profile, tax, 0.05, 1),
                       out_df,
                       check_dtype=False)


# ---------------------------------------------------------------------------
def test_case12() -> None:
    """
    No phages present
    Phages found for hosts
    """

    profile = pd.DataFrame(
        [[0.8, 'bacteria', 'Thermus', 'Thermus thermophilus', 'GCF1', 123],
         [0.2, 'bacteria', 'Salmonella', 'Salmonella enterica', 'GCF2', 456]],
        columns=[
            'rescaled_abundance', 'kingdom', 'genus', 'species', 'accession',
            'taxid'
        ])

    tax = pd.DataFrame(
        [['bacteria', 'Thermus', 'Thermus thermophilus', 'GCF1', 123],
         ['bacteria', 'Salmonella', 'Salmonella enterica', 'GCF2', 456],
         ['viral', '', 'Thermus phage TMA', 'GCF9', 369],
         ['viral', '', 'Salmonella phage g341c', 'GCF7', 147]],
        columns=['kingdom', 'genus', 'species', 'accession', 'taxid'])

    out_df = pd.DataFrame(
        [[0.76, 'bacteria', 'Thermus', 'Thermus thermophilus', 'GCF1', 123],
         [0.19, 'bacteria', 'Salmonella', 'Salmonella enterica', 'GCF2', 456],
         [0.04, 'viral', '', 'Thermus phage TMA', 'GCF9', 369],
         [0.01, 'viral', '', 'Salmonella phage g341c', 'GCF7', 147]],
        columns=[
            'rescaled_abundance', 'kingdom', 'genus', 'species', 'accession',
            'taxid'
        ])

    assert_frame_equal(supplement_phage(profile, tax, 0.05, 2),
                       out_df,
                       check_dtype=False)


# ---------------------------------------------------------------------------
def test_case13() -> None:
    """
    Multiple hosts for a given phage
    """

    profile = pd.DataFrame(
        [[0.5, 'bacteria', 'Thermus', 'Thermus thermophilus', 'GCF1', 123],
         [0.3, 'bacteria', 'Thermus', 'Thermus oshimai', 'GCF12', 687],
         [0.2, 'bacteria', 'Salmonella', 'Salmonella enterica', 'GCF2', 456]],
        columns=[
            'rescaled_abundance', 'kingdom', 'genus', 'species', 'accession',
            'taxid'
        ])

    tax = pd.DataFrame(
        [['bacteria', 'Thermus', 'Thermus thermophilus', 'GCF1', 123],
         ['bacteria', 'Thermus', 'Thermus oshimai', 'GCF12', 687],
         ['bacteria', 'Salmonella', 'Salmonella enterica', 'GCF2', 456],
         ['viral', '', 'Thermus phage TMA', 'GCF9', 369],
         ['viral', '', 'Salmonella phage g341c', 'GCF7', 147]],
        columns=['kingdom', 'genus', 'species', 'accession', 'taxid'])

    out_df = pd.DataFrame(
        [[0.475, 'bacteria', 'Thermus', 'Thermus thermophilus', 'GCF1', 123],
         [0.285, 'bacteria', 'Thermus', 'Thermus oshimai', 'GCF12', 687],
         [0.19, 'bacteria', 'Salmonella', 'Salmonella enterica', 'GCF2', 456],
         [0.04, 'viral', '', 'Thermus phage TMA', 'GCF9', 369],
         [0.01, 'viral', '', 'Salmonella phage g341c', 'GCF7', 147]],
        columns=[
            'rescaled_abundance', 'kingdom', 'genus', 'species', 'accession',
            'taxid'
        ])

    assert_frame_equal(supplement_phage(profile, tax, 0.05, 2),
                       out_df,
                       check_dtype=False)


# ---------------------------------------------------------------------------
def test_case14() -> None:
    """
    Multiple hosts for multiple phages
    """

    profile = pd.DataFrame([
        [0.33, 'bacteria', 'Thermus', 'Thermus thermophilus', 'GCF1', 123],
        [0.33, 'bacteria', 'Thermus', 'Thermus oshimai', 'GCF12', 687],
        [0.33, 'bacteria', 'Salmonella', 'Salmonella enteric', 'GCF2', 456],
        [0.005, 'viral', '', 'Thermus phage phiYS40', 'GCF5', 852],
        [0.005, 'viral', '', 'Thermus phage TMA', 'GCF9', 369],
    ],
                           columns=[
                               'rescaled_abundance', 'kingdom', 'genus',
                               'species', 'accession', 'taxid'
                           ])

    tax = pd.DataFrame(
        [['bacteria', 'Thermus', 'Thermus thermophilus', 'GCF1', 123],
         ['bacteria', 'Thermus', 'Thermus oshimai', 'GCF12', 687],
         ['viral', '', 'Thermus phage phiYS40', 'GCF5', 852],
         ['viral', '', 'Thermus phage TMA', 'GCF9', 369],
         ['viral', '', 'Salmonella phage g341c', 'GCF7', 147]],
        columns=['kingdom', 'genus', 'species', 'accession', 'taxid'])

    out_df = pd.DataFrame([
        [0.31667, 'bacteria', 'Thermus', 'Thermus thermophilus', 'GCF1', 123],
        [0.31667, 'bacteria', 'Thermus', 'Thermus oshimai', 'GCF12', 687],
        [0.31667, 'bacteria', 'Salmonella', 'Salmonella enteric', 'GCF2', 456],
        [0.01667, 'viral', '', 'Thermus phage phiYS40', 'GCF5', 852],
        [0.01667, 'viral', '', 'Thermus phage TMA', 'GCF9', 369],
        [0.01667, 'viral', '', 'Salmonella phage g341c', 'GCF7', 147]
    ],
                          columns=[
                              'rescaled_abundance', 'kingdom', 'genus',
                              'species', 'accession', 'taxid'
                          ])

    assert_frame_equal(supplement_phage(profile, tax, 0.05, 3),
                       out_df,
                       check_dtype=False)


# ---------------------------------------------------------------------------
def test_case15() -> None:
    """
    Do not allow partial match to host genus
    """

    profile = pd.DataFrame([
        [0.33, 'bacteria', 'Thermus', 'Thermus thermophilus', 'GCF1', 123],
        [0.33, 'bacteria', 'Thermus', 'Thermus oshimai', 'GCF12', 687],
        [0.33, 'bacteria', 'Salmonella', 'Salmonella enteric', 'GCF2', 456],
        [0.004, 'viral', '', 'Bacthermus phage phiYS40', 'GCF5', 852],
        [0.002, 'viral', '', 'Salmonella phage g341c', 'GCF7', 147],
        [0.004, 'viral', '', 'Thermus phage TMA', 'GCF9', 369],
    ],
                           columns=[
                               'rescaled_abundance', 'kingdom', 'genus',
                               'species', 'accession', 'taxid'
                           ])

    tax = pd.DataFrame(
        [['bacteria', 'Thermus', 'Thermus thermophilus', 'GCF1', 123],
         ['bacteria', 'Thermus', 'Thermus oshimai', 'GCF12', 687],
         ['viral', '', 'Thermus phage phiYS40', 'GCF5', 852],
         ['viral', '', 'Thermus phage TMA', 'GCF9', 369],
         ['viral', '', 'Salmonella phage g341c', 'GCF7', 147]],
        columns=['kingdom', 'genus', 'species', 'accession', 'taxid'])

    out_df = pd.DataFrame([
        [0.31667, 'bacteria', 'Thermus', 'Thermus thermophilus', 'GCF1', 123],
        [0.31667, 'bacteria', 'Thermus', 'Thermus oshimai', 'GCF12', 687],
        [0.31667, 'bacteria', 'Salmonella', 'Salmonella enteric', 'GCF2', 456],
        [0.004, 'viral', '', 'Bacthermus phage phiYS40', 'GCF5', 852],
        [0.01533, 'viral', '', 'Salmonella phage g341c', 'GCF7', 147],
        [0.03067, 'viral', '', 'Thermus phage TMA', 'GCF9', 369]
    ],
                          columns=[
                              'rescaled_abundance', 'kingdom', 'genus',
                              'species', 'accession', 'taxid'
                          ])

    assert_frame_equal(supplement_phage(profile, tax, 0.05, 3),
                       out_df,
                       check_dtype=False)
