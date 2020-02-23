# Imports
import requests
import pandas as pd
from bs4 import BeautifulSoup

page_url = 'http://stats.espncricinfo.com/ci/engine/records/bowling/most_wickets_career.html?id=12357;type=tournament'

# Build the soup object
page_soup = BeautifulSoup(requests.get(page_url).text,
                                features="html.parser")

# Find main table
table_caption = 'Most wickets'

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
filepath = '../data/world_cup_bowling_raw.csv'
df.to_csv(filepath, index=False)

# Print to show that the data has been saved properly
print(pd.read_csv(filepath))
