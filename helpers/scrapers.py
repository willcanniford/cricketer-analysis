# Imports
import pandas as pd
import requests
from bs4 import BeautifulSoup


def parse_statistics_table(url, table_caption):
    """
    Scrape a given table via a caption and store using pandas

    Parameters
    ----------
    url: str
        URL link where the table is found
    table_caption: str
        HTML caption associated with the table of interest

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

    return df


def get_innings_by_innings_stats(player_id, stats_type):
    """
    Return a cleaned version of stats tables for a player

    Parameters
    ----------
    player_id: int
        The ESPN id for the given cricketer
    stats_type: str
        "Batting" or "Bowling" indicating which stats you require

    Returns
        pandas.DataFrame
    -------

    """
    if stats_type == 'Batting':
        table_url = f'http://stats.espncricinfo.com/ci/engine/player/{player_id}.html?class=1;template=results;type=batting' \
                    f';view=innings'

    elif stats_type == 'Bowling':
        table_url = f'http://stats.espncricinfo.com/ci/engine/player/{player_id}.html?class=1;template=results;type=bowling;view=innings'

    return parse_statistics_table(url=table_url, table_caption='Innings by innings list')
