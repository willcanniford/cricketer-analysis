import numpy as np

from .scrapers import get_innings_by_innings_stats

default_renames = {"4s": "fours",
                   "6s": "sixes",
                   "sr": "strike_rate",
                   "pos": "position",
                   "bf": "balls_faced"}

default_deletes = ['nan', 'DNB', 'TDNB']


def test_innings_by_innings(player_id, column_rename=default_renames, score_deletes=default_deletes, home_or_away=-1):
    raw_table = get_innings_by_innings_stats(player_id, 'Batting', 'Test', home_or_away)
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
    raw_table['is_fifty'] = raw_table.score.astype('str').apply(
        lambda x: 50 <= int(x) < 100 if x.isdigit() else False)
    raw_table['is_hundred'] = raw_table.score.astype('str').apply(
        lambda x: int(x) >= 100 if x.isdigit() else False)

    #  Remove blank columns
    raw_table.drop('', axis=1, inplace=True)

    return raw_table


def odi_innings_by_innings(player_id, column_rename=default_renames, score_deletes=default_deletes, home_or_away=-1):
    raw_table = get_innings_by_innings_stats(player_id, 'Batting', 'ODI', home_or_away)
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
    raw_table['is_fifty'] = raw_table.score.astype('str').apply(
        lambda x: 50 <= int(x) < 100 if x.isdigit() else False)
    raw_table['is_hundred'] = raw_table.score.astype('str').apply(
        lambda x: int(x) >= 100 if x.isdigit() else False)

    #  Remove blank columns
    raw_table.drop('', axis=1, inplace=True)

    return raw_table


def summarise(innings_by_innings_table):
    did_bat = innings_by_innings_table[innings_by_innings_table.did_bat]
    scores = did_bat.score.astype(int)

    summary = {
        "matches": len(innings_by_innings_table.index),
        "innings": sum(innings_by_innings_table.did_bat),
        "runs": sum(scores),
        "high_score": max(scores),
        "balls_faced": sum(did_bat.balls_faced.astype(int)),
        "50s": sum(innings_by_innings_table.is_fifty),
        "100s": sum(innings_by_innings_table.is_hundred),
        "fours": sum(did_bat.fours.astype(int)),
        "sixes": sum(did_bat.sixes.astype(int))
    }

    return summary
