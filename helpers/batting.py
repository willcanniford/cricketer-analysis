import numpy as np

from .scrapers import get_innings_by_innings_stats

default_renames = {"4s": "fours",
                   "6s": "sixes",
                   "sr": "strike_rate",
                   "pos": "position",
                   "bf": "balls_faced"}

default_deletes = ['nan', 'DNB']


def test_innings_by_innings(player_id, column_rename=default_renames, score_deletes=default_deletes):
    raw_table = get_innings_by_innings_stats(player_id, 'Batting', 'Test')
    raw_table.replace('-', np.nan, inplace=True)
    raw_table.columns = raw_table.columns.str.lower().str.replace(' ', '_')

    #  Rename columns
    raw_table.rename(column_rename, axis=1, inplace=True)
    raw_table.runs = raw_table.runs.apply(
        lambda x: np.nan if x in score_deletes else x)

    # Add aggregate columns
    raw_table['did_bat'] = raw_table.runs.str.replace(
        '*', '').astype('str').apply(lambda x: True if x.isnumeric() else False)
    raw_table['is_out'] = raw_table.runs.astype('str').apply(
        lambda x: False if x in score_deletes else False if '*' in x else True)
    raw_table['score'] = raw_table.runs.astype('str').apply(
        lambda x: np.nan if x in score_deletes else x.replace('*', '') if '*' in x else x)

    #  Remove blank columns
    raw_table.drop('', axis=1, inplace=True)

    return raw_table


def odi_innings_by_innings(player_id, column_rename=default_renames, score_deletes=default_deletes):
    raw_table = get_innings_by_innings_stats(player_id, 'Batting', 'ODI')
    raw_table.replace('-', np.nan, inplace=True)
    raw_table.columns = raw_table.columns.str.lower().str.replace(' ', '_')

    #  Rename columns
    raw_table.rename(column_rename, axis=1, inplace=True)
    raw_table.runs = raw_table.runs.apply(
        lambda x: np.nan if x in score_deletes else x)

    # Add aggregate columns
    raw_table['did_bat'] = raw_table.runs.str.replace(
        '*', '').astype('str').apply(lambda x: True if x.isnumeric() else False)
    raw_table['is_out'] = raw_table.runs.astype('str').apply(
        lambda x: False if x in score_deletes else False if '*' in x else True)
    raw_table['score'] = raw_table.runs.astype('str').apply(
        lambda x: np.nan if x in score_deletes else x.replace('*', '') if '*' in x else x)

    #  Remove blank columns
    raw_table.drop('', axis=1, inplace=True)

    return raw_table
