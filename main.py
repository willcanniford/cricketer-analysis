import helpers.batting as bat
import helpers.bowling as bowl
import helpers.scrapers as scrape
import matplotlib.pyplot as plt
import numpy as np

jim_bowling = bowl.test_innings_by_innings(8608, home_or_away=1)
# print(jim_bowling.head())


print(bowl.test_home_or_away(210283))

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
jos = bat.odi_innings_by_innings(308967, home_or_away=2)

batted = jos.runs.notnull()
did_not_bat = jos.runs.isnull()

jos_batted = jos[batted]
# print(jos_batted.head())
