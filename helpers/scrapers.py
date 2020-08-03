# Imports
import pandas as pd
import requests
from bs4 import BeautifulSoup


def parse_statistics_table(url, table_caption, home_away=-1):
    """
    Scrape a given table via a caption and store using pandas

    Parameters
    ----------
    url: str
        URL link where the table is found
    table_caption: str
        HTML caption associated with the table of interest
    home_away: int
        1, 2, 3 indicates whether you should filter the final table
        1 = home, 2 = away, 3 = neutral venue

    Returns
    -------
    pandas.DataFrame
        HTML table as a pandas.DataFrame
    """
    page_soup = BeautifulSoup(requests.get(url).text,
                              features="html.parser")

    # Find main table
    for caption in page_soup.find_all('caption'):
        if caption.get_text() == table_caption:
            table = caption.find_parent(
                'table', {'class': 'engineTable'})

    # Isolate the column names <thead>
    table_thead = table.find('thead').find_all('tr')[0]
    columns = [x.get_text() for x in table_thead.find_all('th')]

    # Find and store each row
    rows = []

    for innings in [row for row in table.find('tbody').find_all('tr')]:
        rows.append([stat.get_text() for stat in innings.find_all('td')])

    # Create pandas data frame and save to csv
    df = pd.DataFrame(rows, columns=columns).apply(pd.to_numeric, errors='ignore')

    if home_away != -1:
        df['home_or_away'] = "Home" if home_away == 1 else "Away" if home_away == 2 else "Neutral"

    return df


def get_innings_by_innings_stats(player_id, stats_type, match_format="Test", home_away=-1):
    """
    Return a cleaned version of stats tables for a player

    Parameters
    ----------
    player_id: int
        The ESPN id for the given cricketer
    stats_type: str
        "Batting" or "Bowling" indicating which stats you require
    match_format: str
        "Test" or "ODI" for the format of interest
    home_away: int
        1, 2, 3 indicates whether you should filter the final table
        1 = home, 2 = away, 3 = neutral venue

    Returns
    -------
    pandas.DataFrame
        HTML table as a pandas.DataFrame
    """
    if match_format == "Test":
        url_class = 1
    elif match_format == "ODI":
        url_class = 2

    if home_away == -1:
        home_or_away = ""
    else:
        home_or_away = f"home_or_away={home_away};"

    if stats_type == 'Batting':
        table_url = f'http://stats.espncricinfo.com/ci/engine/player/{player_id}.html?class={url_class};{home_or_away}template=results;type=batting;view=innings'

    elif stats_type == 'Bowling':
        table_url = f'http://stats.espncricinfo.com/ci/engine/player/{player_id}.html?class={url_class};{home_or_away}template=results;type=bowling;view=innings'

    return parse_statistics_table(url=table_url, table_caption='Innings by innings list', home_away=home_away)
