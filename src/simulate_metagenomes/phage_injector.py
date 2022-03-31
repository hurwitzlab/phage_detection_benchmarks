"""
Author : Kenneth Schackart <schackartk1@gmail.com>
Date   : 2022-03-31
Purpose: Provide fucntions to increase pahge content of profile
"""

import pandas as pd
from pandas.testing import assert_frame_equal
from typing import List, Tuple

pd.options.mode.chained_assignment = None


# ---------------------------------------------------------------------------
def rescale_abundances(col: pd.Series, total: float = 1) -> pd.Series:
    """ Rescale abundances to add to total """

    rescale_factor = total / col.sum()

    rescaled = rescale_factor * col

    rescaled = rescaled.round(5)

    return rescaled


# ---------------------------------------------------------------------------
def test_rescale_abundances() -> None:
    """ Test rescale_abundances() """

    example_col = pd.Series([0.5, 0.3])
    rescaled_col = pd.Series([0.625, 0.375])

    assert rescale_abundances(example_col).equals(rescaled_col)

    example_col = pd.Series([0.5, 0.5])
    rescaled_col = pd.Series([0.475, 0.475])

    assert rescale_abundances(example_col, 0.95).equals(rescaled_col)


# ---------------------------------------------------------------------------
def get_phage_content(df: pd.DataFrame) -> float:
    """ Sum fraction total reads of phage """

    phages = get_phages(df)

    phage_content = phages.rescaled_abundance.sum()

    return phage_content


# ---------------------------------------------------------------------------
def test_get_phage_content() -> None:
    """ Test get_phage_content() """

    in_df = pd.DataFrame([[
        0.00103, 'viral', 'Bellamyvirus', 'Synechococcus phage S-SM2',
        'GCF_000890815.1', 444860
    ], [
        0.00007, 'viral', '', 'Cyanophage S-RIM32', 'GCF_001754165.1', 1278479
    ],
                          [
                              0.00002, 'bacteria', 'Troponema',
                              'Treponema phagedenis', 'GCF_008152505.1', 162
                          ]],
                         columns=[
                             'rescaled_abundance', 'kingdom', 'genus',
                             'species', 'accession', 'taxid'
                         ])

    phage_content = 0.0011

    assert get_phage_content(in_df) == phage_content


# ---------------------------------------------------------------------------
def get_phages(df: pd.DataFrame) -> pd.DataFrame:
    """ Filter dataframe for phages"""

    viruses = df[df.kingdom == 'viral']

    phages = viruses[viruses.species.str.contains('phage',
                                                  regex=True,
                                                  case=False)]

    return phages


# ---------------------------------------------------------------------------
def test_get_phages() -> None:
    """ Test get_phages() """

    in_df = pd.DataFrame([[
        0.00103, 'viral', 'Bellamyvirus', 'Synechococcus phage S-SM2',
        'GCF_000890815.1', 444860
    ], [
        0.00007, 'viral', '', 'Cyanophage S-RIM32', 'GCF_001754165.1', 1278479
    ],
                          [
                              0.00002, 'bacteria', 'Troponema',
                              'Treponema phagedenis', 'GCF_008152505.1', 162
                          ]],
                         columns=[
                             'fraction_total_reads', 'kingdom', 'genus',
                             'species', 'accession', 'taxid'
                         ])

    out_df = pd.DataFrame([[
        0.00103, 'viral', 'Bellamyvirus', 'Synechococcus phage S-SM2',
        'GCF_000890815.1', 444860
    ], [
        0.00007, 'viral', '', 'Cyanophage S-RIM32', 'GCF_001754165.1', 1278479
    ]],
                          columns=[
                              'fraction_total_reads', 'kingdom', 'genus',
                              'species', 'accession', 'taxid'
                          ])

    assert_frame_equal(get_phages(in_df), out_df)


# ---------------------------------------------------------------------------
def anti_join_profiles(df: pd.DataFrame,
                       exclude_df: pd.DataFrame) -> pd.DataFrame:
    """ Get all rows in `df` not in `exclude df` """

    df = df[pd.merge(df,
                     exclude_df,
                     how='outer',
                     left_on='taxid',
                     right_on='taxid',
                     indicator=True)['_merge'] == 'left_only']

    return df


# ---------------------------------------------------------------------------
def get_phage_from_hosts(phages: pd.DataFrame, nonviral: pd.DataFrame,
                         num_phage: int,
                         all_phage: pd.DataFrame) -> List[Tuple[str, str]]:
    """
    Retrieve phages corresponging to nonviral hosts
    
    Parameters:
    `phages`: Phages in profile
    `nonviral`: Nonviral portion of profile
    `num_phage`: Minimum number of phages in profile
    `all_phage`: All phages in local database

    Return:
    List of tuples with (host_taxid, phage_taxid)
    """

    # Cannot use dict since neither host nor phage are always unique
    host_phage = []
    n_phage = len(phages)

    for _, organism in nonviral.iterrows():

        genus = organism['genus'].lower()

        # First, check if host's phage is already present in profile
        matches = phages['species'].str.lower().str.contains(genus)
        if any(matches):
            phage_matches = phages[matches]
            for _, phage_match in phage_matches.iterrows():
                host_phage.append((organism['taxid'], phage_match['taxid']))
            continue

        if n_phage >= num_phage:
            break

        # Now search for phages matching host in all phages
        matches = all_phage['species'].str.lower().str.contains(genus)
        if any(matches):
            phage_matches = all_phage[matches]
            phage_match = phage_matches.iloc[0]
            host_phage.append((organism['taxid'], phage_match['taxid']))
            n_phage += 1

    return host_phage


# ---------------------------------------------------------------------------
def add_host_phages(phages: pd.DataFrame, host_phage: List[Tuple[str, str]],
                    nonviral: pd.DataFrame,
                    all_phage: pd.DataFrame) -> pd.DataFrame:
    """
    Add phages corresponsing to hosts and columns about host
    
    Parameters:
    `phages`: Phages in profile
    `host_phage`: List of tuples with (host_taxid, phage_taxid)

    Return:
    Updated `phages` df, with new phages and columns "host_abundance" and "host_taxid
    """

    phages['host_abundance'] = ''
    phages['host_taxid'] = ''

    for host, phage in host_phage:

        if phage not in phages['taxid'].values:
            phage_entry = all_phage[all_phage['taxid'] == phage]

            phages = pd.concat([phages, phage_entry])

        host_entry = nonviral[nonviral['taxid'] == host]

        host_abundance = host_entry['abundance'].iloc[0]

        phages['host_abundance'][phages['taxid'] == phage] = host_abundance
        phages['host_taxid'][phages['taxid'] == phage] = host

    return phages


# ---------------------------------------------------------------------------
def supplement_phage(profile: pd.DataFrame, tax: pd.DataFrame,
                     phage_content: float, num_phage: int) -> pd.DataFrame:
    """ Add more phage to profile """

    profile = profile.rename(columns={'rescaled_abundance': 'abundance'})

    profile_phage = get_phages(profile)

    profile_non_phage = anti_join_profiles(profile, profile_phage)

    profile_non_phage['abundance'] = rescale_abundances(
        profile_non_phage['abundance'], 1 - phage_content)

    profile_non_viral = profile_non_phage[
        profile_non_phage['kingdom'] != 'viral']

    all_phage = get_phages(tax)

    host_phage = get_phage_from_hosts(profile_phage, profile_non_viral,
                                      num_phage, all_phage)

    profile_phage = add_host_phages(profile_phage, host_phage,
                                    profile_non_viral, all_phage)

    non_hosted = profile_phage[profile_phage['host_abundance'] == '']
    hosted = profile_phage[profile_phage['host_abundance'] != '']

    host_counts = hosted.groupby(['host_taxid'])['host_abundance'].count()
    host_abundances = hosted.drop_duplicates('host_taxid')
    total_host_abundance = host_abundances['host_abundance'].sum()

    non_hosted_abundance = non_hosted['abundance'].sum()
    non_hosted_count = non_hosted['abundance'].count()
    if non_hosted_count >= num_phage:
        non_hosted['abundance'] = rescale_abundances(non_hosted['abundance'],
                                                     phage_content)

    remaining_abundance = phage_content - non_hosted_abundance

    abundance_by_host = remaining_abundance * host_abundances[
        'host_abundance'].values / total_host_abundance / host_counts.values

    new_abundances = dict(zip(host_abundances['host_taxid'],
                              abundance_by_host))

    hosted['abundance'] = hosted['host_taxid'].map(new_abundances.get).round(5)

    hosted = hosted.drop(['host_abundance', 'host_taxid'], axis='columns')
    non_hosted = non_hosted.drop(['host_abundance', 'host_taxid'],
                                 axis='columns')

    new_profile = pd.concat([profile_non_phage, non_hosted, hosted])

    new_profile = new_profile.rename(
        columns={'abundance': 'rescaled_abundance'})

    new_profile = new_profile.reset_index(drop=True)

    return new_profile


# ---------------------------------------------------------------------------
def test_supplement_phage() -> None:
    """ Test supplement_phage() """

    profile = pd.DataFrame(
        [[0.4, 'bacteria', 'Thermus', 'Thermus thermophilus', 'GCF1', 123],
         [0.3, 'bacteria', 'Salmonella', 'Salmonella enterica', 'GCF2', 456],
         [0.2, 'bacteria', 'Escherichia', 'Escherichia coli', 'GCF3', 789],
         [0.09, 'bacteria', 'Borrelia', 'Borellia miyamotoi', 'GCF4', 741],
         [0.005, 'viral', '', 'Thermus phage phiYS40', 'GCF5', 852],
         [0.004, 'viral', '', 'Thermus phage TMA', 'GCF9', 369],
         [0.001, 'viral', '', 'Bacillus phage Fah', 'GCF10', 951]],
        columns=[
            'rescaled_abundance', 'kingdom', 'genus', 'species', 'accession',
            'taxid'
        ])

    tax = pd.DataFrame(
        [['bacteria', 'Thermus', 'Thermus thermophilus', 'GCF1', 123],
         ['bacteria', 'Salmonella', 'Salmonella enterica', 'GCF2', 456],
         ['bacteria', 'Escherichia', 'Escherichia coli', 'GCF3', 789],
         ['viral', '', 'Thermus phage phiYS40', 'GCF5', 852],
         ['viral', '', 'Thermus phage TMA', 'GCF9', 369],
         ['viral', '', 'Escherichia phage D108', 'GCF6', 963],
         ['viral', '', 'Salmonella phage g341c', 'GCF7', 147],
         ['viral', '', 'Salmonella phage ST64B', 'GCF8', 258],
         ['viral', '', 'Bacillus phage Fah', 'GCF10', 951]],
        columns=['kingdom', 'genus', 'species', 'accession', 'taxid'])

    # Other abundances are rescaled to 1 - phage_content
    # Phages matching bacterial genuses are added
    # Only 1 phage per bacteria is added even if multiple matches
    # If phage already has match to current bacteria, keep it
    #    and rescale as below
    #    If mulitple phages already present for host, split the scaling evenly
    # The phage_content split among phages is the same proportion as
    #    the bacteria they represent
    out_df = pd.DataFrame(
        [[0.38384, 'bacteria', 'Thermus', 'Thermus thermophilus', 'GCF1', 123],
         [
             0.28788, 'bacteria', 'Salmonella', 'Salmonella enterica', 'GCF2',
             456
         ],
         [0.19192, 'bacteria', 'Escherichia', 'Escherichia coli', 'GCF3', 789],
         [0.08636, 'bacteria', 'Borrelia', 'Borellia miyamotoi', 'GCF4', 741],
         [0.00100, 'viral', '', 'Bacillus phage Fah', 'GCF10', 951],
         [0.01089, 'viral', '', 'Thermus phage phiYS40', 'GCF5', 852],
         [0.01089, 'viral', '', 'Thermus phage TMA', 'GCF9', 369],
         [0.01633, 'viral', '', 'Salmonella phage g341c', 'GCF7', 147],
         [0.01089, 'viral', '', 'Escherichia phage D108', 'GCF6', 963]],
        columns=[
            'rescaled_abundance', 'kingdom', 'genus', 'species', 'accession',
            'taxid'
        ])

    assert_frame_equal(supplement_phage(profile, tax, 0.05, 10), out_df)

    # Minimum number of phage less than current number, just boost proportion
    out_df = pd.DataFrame([[
        0.38384, 'bacteria', 'Thermus', 'Thermus thermophilus', 'GCF1', 123
    ], [0.28788, 'bacteria', 'Salmonella', 'Salmonella enterica', 'GCF2', 456
        ], [
            0.19192, 'bacteria', 'Escherichia', 'Escherichia coli', 'GCF3', 789
        ], [
            0.08636, 'bacteria', 'Borrelia', 'Borellia miyamotoi', 'GCF4', 741
        ], [0.00100, 'viral', '', 'Bacillus phage Fah', 'GCF10', 951
            ], [0.0245, 'viral', '', 'Thermus phage phiYS40', 'GCF5', 852
                ], [0.0245, 'viral', '', 'Thermus phage TMA', 'GCF9', 369]],
                          columns=[
                              'rescaled_abundance', 'kingdom', 'genus',
                              'species', 'accession', 'taxid'
                          ])

    assert_frame_equal(supplement_phage(profile, tax, 0.05, 2), out_df)

    # Need to add some phage but not all available
    out_df = pd.DataFrame(
        [[0.38384, 'bacteria', 'Thermus', 'Thermus thermophilus', 'GCF1', 123],
         [
             0.28788, 'bacteria', 'Salmonella', 'Salmonella enterica', 'GCF2',
             456
         ],
         [0.19192, 'bacteria', 'Escherichia', 'Escherichia coli', 'GCF3', 789],
         [0.08636, 'bacteria', 'Borrelia', 'Borellia miyamotoi', 'GCF4', 741],
         [0.00100, 'viral', '', 'Bacillus phage Fah', 'GCF10', 951],
         [0.01400, 'viral', '', 'Thermus phage phiYS40', 'GCF5', 852],
         [0.01400, 'viral', '', 'Thermus phage TMA', 'GCF9', 369],
         [0.02100, 'viral', '', 'Salmonella phage g341c', 'GCF7', 147]],
        columns=[
            'rescaled_abundance', 'kingdom', 'genus', 'species', 'accession',
            'taxid'
        ])

    assert_frame_equal(supplement_phage(profile, tax, 0.05, 4), out_df)

    # Number phages already met, but no host to determine scaling
    profile = pd.DataFrame(
        [[0.7, 'bacteria', 'Salmonella', 'Salmonella enterica', 'GCF2', 456],
         [0.2, 'bacteria', 'Escherichia', 'Escherichia coli', 'GCF3', 789],
         [0.09, 'bacteria', 'Borrelia', 'Borellia miyamotoi', 'GCF4', 741],
         [0.005, 'viral', '', 'Thermus phage phiYS40', 'GCF5', 852],
         [0.004, 'viral', '', 'Thermus phage TMA', 'GCF9', 369],
         [0.001, 'viral', '', 'Bacillus phage Fah', 'GCF10', 951]],
        columns=[
            'rescaled_abundance', 'kingdom', 'genus', 'species', 'accession',
            'taxid'
        ])

    out_df = pd.DataFrame([[
        0.67172, 'bacteria', 'Salmonella', 'Salmonella enterica', 'GCF2', 456
    ], [0.19192, 'bacteria', 'Escherichia', 'Escherichia coli', 'GCF3', 789
        ], [
            0.08636, 'bacteria', 'Borrelia', 'Borellia miyamotoi', 'GCF4', 741
        ], [0.025, 'viral', '', 'Thermus phage phiYS40', 'GCF5', 852
            ], [0.02, 'viral', '', 'Thermus phage TMA', 'GCF9', 369
                ], [0.005, 'viral', '', 'Bacillus phage Fah', 'GCF10', 951]],
                          columns=[
                              'rescaled_abundance', 'kingdom', 'genus',
                              'species', 'accession', 'taxid'
                          ])

    assert_frame_equal(supplement_phage(profile, tax, 0.05, 3),
                       out_df,
                       check_dtype=False)
