import helpers.batting as bat
import helpers.scrapers as scrape

batting = scrape.get_innings_by_innings_stats(519082, 'Batting')

# Columns to keep
# How to format each column

schema = {
    'original_name': 'Runs',
    'new_name': 'runs',
    'data_type': 'int',
    'regex_clean': '',
    "na_values": ['DNB']
}

innings = bat.test_innings_by_innings(519082)

print(innings)
