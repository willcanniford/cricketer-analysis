import re

import numpy as np
import pandas as pd

from .scrapers import get_innings_by_innings_stats

default_renames = {"mdns": "maidens",
                   "wkts": "wickets",
                   "econ": "economy",
                   "pos": "position",
                   "inns": "innings"}

default_deletes = ['nan', 'DNB', 'TDNB']


def total_balls(overs_str, str_ignore=['DNB', 'TDNB'], ignore_value=0):
    """
    Calculate total balls bowled from overs formatting

    Parameters
    ----------
    overs_str: string
        Overs bowled in traditional format overs.balls
    str_ignore: list
        Strings to ignore and return 0 - indicators that the player didn't bowl
    ignore_value: int
        Value to input for strings matched into str_ignore

    Returns
    -------
    int:
        The number of balls bowled as an int
    """
    if overs_str in str_ignore:
        return ignore_value

    grouping_re = re.compile(r'^([0-9]*)\.([0-5]*)$').search(overs_str)

    if grouping_re is None:
        return int(overs_str) * 6
    else:
        overs = int(grouping_re.group(1)) * 6
        balls = int(grouping_re.group(2))
        return overs + balls


def test_innings_by_innings(player_id, column_rename=default_renames, score_deletes=default_deletes, home_or_away=-1):
    """
    Return the test innings by innings for a given player

    Parameters
    ----------
    player_id: int
        Player ID for cricketer from ESPNcricinfo
    column_rename: dict
        Rename columns old: new
    score_deletes: list
        Values to represent null
    home_or_away: int
        Value to limit to either home or away matches

    Returns
    -------
    pandas.DataFrame
        Test innings DataFrame scraped from site
    """
    raw_table = get_innings_by_innings_stats(player_id, 'Bowling', 'Test', home_or_away)

    if raw_table is None:
        return None

    raw_table.replace('-', np.nan, inplace=True)
    raw_table.columns = raw_table.columns.str.lower().str.replace(' ', '_')

    #  Rename columns
    raw_table.rename(column_rename, axis=1, inplace=True)
    raw_table.runs = raw_table.runs.apply(
        lambda x: np.nan if x in score_deletes else x)

    raw_table['total_balls'] = raw_table.overs.astype(str).apply(total_balls)

    #  Remove blank columns
    raw_table.drop('', axis=1, inplace=True)

    return raw_table


def test_home_or_away(player_id):
    """
    Get the test bowling innings for a given player with column indicating home/away/neutral
    Parameters
    ----------
    player_id: int
        Player ID for cricketer from ESPNcricinfo

    Returns
    -------
    pandas.DataFrame
        Test innings DataFrame scraped from site with additional home/away/neutral column
    """
    home = test_innings_by_innings(player_id, home_or_away=1)
    away = test_innings_by_innings(player_id, home_or_away=2)
    neutral = test_innings_by_innings(player_id, home_or_away=3)

    return pd.concat([home, away, neutral])
