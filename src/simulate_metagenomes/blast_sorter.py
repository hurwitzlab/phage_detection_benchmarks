"""
Functions for assigning taxonomy to contigs based on BLAST results
"""

from typing import List, Tuple

import numpy as np
import pandas as pd
from pandas.testing import assert_frame_equal


# --------------------------------------------------
def make_raw_df(rows: List[List]) -> pd.DataFrame:
    """ Make a parsed BLAST df using input rows """

    cols = [
        'query_id', 'hit_id', 'e_val', 'query_length', 'alignment_length',
        'start', 'end'
    ]

    return pd.DataFrame(rows, columns=cols)


# --------------------------------------------------
def test_make_raw_df() -> None:
    """ Test make_raw_df() """

    rows = [['k1_1', 'GCF_001', 0, 535, 535, 1, 535],
            ['k1_2', 'GCF_002', 0, 501, 497, 5, 501]]

    out_df = pd.DataFrame([['k1_1', 'GCF_001', 0, 535, 535, 1, 535],
                           ['k1_2', 'GCF_002', 0, 501, 497, 5, 501]],
                          columns=[
                              'query_id', 'hit_id', 'e_val', 'query_length',
                              'alignment_length', 'start', 'end'
                          ])

    assert_frame_equal(make_raw_df(rows), out_df)


# --------------------------------------------------
def make_sorted_df(rows: List[List]) -> pd.DataFrame:
    """ Make a sorted df using input rows """

    cols = [
        'query_id', 'hit_id', 'e_val', 'query_length', 'alignment_length',
        'start', 'end', 'origin'
    ]

    return pd.DataFrame(rows, columns=cols)


# --------------------------------------------------
def test_make_sorted_df() -> None:
    """ Test make_sorted_df() """

    rows = [['k1_1', 'GCF_001', 0, 535, 535, 1, 535, 'single'],
            ['k1_2', 'GCF_002', 0, 501, 497, 5, 501, 'chimera']]

    out_df = pd.DataFrame(
        [['k1_1', 'GCF_001', 0, 535, 535, 1, 535, 'single'],
         ['k1_2', 'GCF_002', 0, 501, 497, 5, 501, 'chimera']],
        columns=[
            'query_id', 'hit_id', 'e_val', 'query_length', 'alignment_length',
            'start', 'end', 'origin'
        ])

    assert_frame_equal(make_sorted_df(rows), out_df)


# --------------------------------------------------
def get_coverages(starts: List[int], ends: List[int]) -> List[Tuple[int, int]]:
    """ Find regions that were aligned """

    coverages = [(1, 1)]

    # Iterate through all regions with hits
    for (start, end) in zip(starts, ends):

        # Check if current hit region overlaps a previous one
        overlapping = [
            cov_start <= start <= cov_end for (cov_start, cov_end) in coverages
        ]

        # If there is overlap, merge the regions
        if any(overlapping):

            # Get index of previous region that has overlap with current
            i = int(np.where(overlapping)[0])
            (cov_start, cov_end) = coverages[i]

            # Expand coverage region end position
            coverages[i] = (cov_start, max(end, cov_end))
        else:
            # If no overlap, just add the current hit region
            coverages.append((start, end))

    if (1, 1) in coverages:
        coverages.remove((1, 1))

    return coverages


# --------------------------------------------------
def test_get_coverages() -> None:
    """ Test get_coverages() """

    assert get_coverages([2, 3], [5, 6]) == [(2, 6)]
    assert get_coverages([2, 10], [10, 20]) == [(2, 20)]
    assert get_coverages([1, 20], [10, 30]) == [(1, 10), (20, 30)]


# --------------------------------------------------
def merge_same_adjacent(df: pd.DataFrame) -> pd.DataFrame:
    """
    Check if adjacent distinct hit regions align to same genome
    If so, merge those regions
    """

    out_df = pd.DataFrame()
    for i in range(1, len(df)):
        if df['hit_id'][i] == df['hit_id'][i - 1]:
            start = df['start'][i - 1]
            end = df['end'][i]
            e_val = max(df['e_val'][i], df['e_val'][i - 1])
            merged_hit = make_sorted_df([[
                df['query_id'][i], df['hit_id'][i], e_val,
                df['query_length'][i], end - start + 1, start, end, 'chimera'
            ]])
            df.iloc[i] = merged_hit.iloc[0]

            if i != len(df) - 1:
                if df['hit_id'][i] == df['hit_id'][i + 1]:
                    continue
            out_df = pd.concat([out_df, merged_hit])
        else:
            if i == 1:
                out_df = pd.concat([out_df, df.iloc[[0]]])
            out_df = pd.concat([out_df, df.iloc[[i]]])

    out_df = out_df.reset_index(drop=True)

    if len(out_df) == 1:
        out_df['origin'] = 'single'

    return out_df


# --------------------------------------------------
def test_merge_same_adjacent() -> None:
    """ Test merge_same_adjacent() """

    in_df = make_sorted_df(
        [['k1_1', 'GCF_001', 0.05, 1000, 500, 1, 500, 'chimera'],
         ['k1_1', 'GCF_001', 0, 1000, 50, 601, 650, 'chimera'],
         ['k1_1', 'GCF_001', 0, 1000, 100, 701, 800, 'chimera']])

    # Coverage of adjacent same-hit regions spans length of both
    # Take larger e-val of adjacent hits (shouldn't be used later)
    out_df = make_sorted_df(
        [['k1_1', 'GCF_001', 0.05, 1000, 800, 1, 800, 'single']])

    assert_frame_equal(merge_same_adjacent(in_df), out_df, check_dtype=False)

    in_df = make_sorted_df(
        [['k1_1', 'GCF_001', 0.05, 1000, 500, 1, 500, 'chimera'],
         ['k1_1', 'GCF_001', 0, 1000, 100, 701, 800, 'chimera'],
         ['k1_1', 'GCF_002', 0, 1000, 100, 901, 1000, 'chimera']])

    out_df = make_sorted_df(
        [['k1_1', 'GCF_001', 0.05, 1000, 800, 1, 800, 'chimera'],
         ['k1_1', 'GCF_002', 0, 1000, 100, 901, 1000, 'chimera']])

    assert_frame_equal(merge_same_adjacent(in_df), out_df, check_dtype=False)


# --------------------------------------------------
def assign_tax(df: pd.DataFrame) -> pd.DataFrame:
    """ Assign taxonomy for a single contig """

    # Single hit
    if len(df.index) == 1:
        df['origin'] = 'single'
        return df

    # Sort by e_val, check for full length hit, return first one
    df = df.sort_values(by='e_val', ascending=True)
    for _, hit in df.iterrows():
        if hit['query_length'] == hit['alignment_length']:
            hit['origin'] = 'single'
            out_df = make_sorted_df([list(hit)])
            return out_df

    # Check for hit longer than full length, return first one
    for _, hit in df.iterrows():
        if hit['query_length'] < hit['alignment_length']:
            hit['origin'] = 'single'
            out_df = make_sorted_df([list(hit)])
            return out_df

    # Check if all hits are overlapping
    start_sorted_df = df.sort_values(by='start', ascending=True)
    coverages = get_coverages(start_sorted_df['start'], start_sorted_df['end'])

    # All hits are overlapping
    if len(coverages) == 1:
        df = df.sort_values(by=['e_val', 'alignment_length'],
                            ascending=[True, False])
        df = df.head(1)
        df['origin'] = 'single'
        return df

    # Not all hits are overlapping
    out_df = pd.DataFrame()
    for start, end in coverages:
        df['origin'] = 'chimera'
        hits = df[(df['start'] >= start) & (df['end'] <= end)]
        hits = hits.sort_values(by=['e_val', 'alignment_length'],
                                ascending=[True, False])
        best_hit = hits.head(1)
        out_df = pd.concat([out_df, best_hit])

    out_df = out_df.reset_index(drop=True)

    # Merge adjacent hit regions aligning to same genome
    out_df = merge_same_adjacent(out_df)

    return out_df


# --------------------------------------------------
def test_single_hit() -> None:
    """ Single BLAST hit """

    in_df = make_raw_df([['k1_1', 'GCF_001', 0, 535, 535, 1, 535]])

    out_df = make_sorted_df(
        [['k1_1', 'GCF_001', 0, 535, 535, 1, 535, 'single']])

    assert_frame_equal(assign_tax(in_df), out_df, check_dtype=False)


# --------------------------------------------------
def test_perfect_full_hits() -> None:
    """ Multiple e_val=0 full length hits """

    in_df = make_raw_df([['k1_1', 'GCF_001', 0, 535, 535, 1, 535],
                         ['k1_1', 'GCF_002', 0, 535, 535, 1, 535]])

    out_df = make_sorted_df(
        [['k1_1', 'GCF_001', 0, 535, 535, 1, 535, 'single']])

    assert_frame_equal(assign_tax(in_df), out_df, check_dtype=False)


# --------------------------------------------------
def test_various_full_hits() -> None:
    """ Multiple full length hits, varying e_val """

    in_df = make_raw_df([['k1_1', 'GCF_001', 1.16E-28, 535, 535, 1, 535],
                         ['k1_1', 'GCF_002', 0, 535, 535, 1, 535]])

    out_df = make_sorted_df(
        [['k1_1', 'GCF_002', 0, 535, 535, 1, 535, 'single']])

    assert_frame_equal(assign_tax(in_df), out_df, check_dtype=False)


# --------------------------------------------------
def test_longer_than_query() -> None:
    """
    Alignment is longer than query
    """

    in_df = make_raw_df([['k1_1', 'GCF_001', 0, 570, 417, 1, 416],
                         ['k1_1', 'GCF_002', 0, 570, 571, 1, 570]])

    out_df = make_sorted_df(
        [['k1_1', 'GCF_002', 0, 570, 571, 1, 570, 'single']])

    assert_frame_equal(assign_tax(in_df), out_df, check_dtype=False)


# --------------------------------------------------
def test_no_full_hits() -> None:
    """
    No full hits; all hits are overlapping
    Prioritize e_val then length
    """

    in_df = make_raw_df([['k1_1', 'GCF_001', 0, 570, 417, 1, 416],
                         ['k1_1', 'GCF_002', 0, 570, 405, 1, 404],
                         ['k1_1', 'GCF_003', 0.05, 570, 500, 1, 499]])

    out_df = make_sorted_df(
        [['k1_1', 'GCF_001', 0, 570, 417, 1, 416, 'single']])

    assert_frame_equal(assign_tax(in_df), out_df, check_dtype=False)


# --------------------------------------------------
def test_single_but_separate() -> None:
    """
    Distinct hit regions
    Single origin, not chimeric
    """

    in_df = make_raw_df([['k1_1', 'GCF_001', 0, 500, 200, 1, 199],
                         ['k1_1', 'GCF_001', 0, 500, 200, 3, 201],
                         ['k1_1', 'GCF_001', 0, 500, 200, 301, 500],
                         ['k1_1', 'GCF_001', 0.05, 500, 250, 251, 500]])

    out_df = make_sorted_df(
        [['k1_1', 'GCF_001', 0, 500, 500, 1, 500, 'single']])

    assert_frame_equal(assign_tax(in_df), out_df, check_dtype=False)


# --------------------------------------------------
def test_chimera() -> None:
    """
    Distinct regions with hits
    For each region with overlapping hits,
        prioritize e_val then length
    """

    in_df = make_raw_df([['k1_1', 'GCF_001', 0, 500, 200, 1, 199],
                         ['k1_1', 'GCF_002', 0, 500, 200, 3, 201],
                         ['k1_1', 'GCF_003', 0, 500, 200, 301, 500],
                         ['k1_1', 'GCF_004', 0.05, 500, 250, 251, 500]])

    out_df = make_sorted_df(
        [['k1_1', 'GCF_001', 0, 500, 200, 1, 199, 'chimera'],
         ['k1_1', 'GCF_003', 0, 500, 200, 301, 500, 'chimera']])

    assert_frame_equal(assign_tax(in_df), out_df, check_dtype=False)


# --------------------------------------------------
def test_separate_and_chimera() -> None:
    """
    Distinct hit regions
    Some same origin
    Others different origin
    """

    in_df = make_raw_df([['k1_1', 'GCF_001', 0, 1000, 200, 1, 199],
                         ['k1_1', 'GCF_001', 0, 1000, 200, 3, 201],
                         ['k1_1', 'GCF_001', 0, 1000, 200, 301, 500],
                         ['k1_1', 'GCF_001', 0.05, 1000, 250, 251, 500],
                         ['k1_1', 'GCF_002', 0, 1000, 100, 701, 800],
                         ['k1_1', 'GCF_001', 0, 1000, 100, 901, 1000]])

    out_df = make_sorted_df(
        [['k1_1', 'GCF_001', 0, 1000, 500, 1, 500, 'chimera'],
         ['k1_1', 'GCF_002', 0, 1000, 100, 701, 800, 'chimera'],
         ['k1_1', 'GCF_001', 0, 1000, 100, 901, 1000, 'chimera']])

    assert_frame_equal(assign_tax(in_df), out_df, check_dtype=False)