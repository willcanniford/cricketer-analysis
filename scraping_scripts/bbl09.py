# Imports
import requests
import pandas as pd
from bs4 import BeautifulSoup

page_url = 'http://stats.espncricinfo.com/ci/engine/records/batting/most_runs_career.html?id=13207;type=tournament'

page_soup = BeautifulSoup(requests.get(page_url).text, features="html.parser")

# Find main table
table_caption = 'Most runs'

for caption in page_soup.find_all('caption'):
    if caption.get_text() == table_caption:
        table = caption.find_parent(
            'table', {'class': 'engineTable'})

# Get column names
table_thead = table.find('thead').find_all('tr')[0]
columns = [header.get_text() for header in table_thead.find_all('th')]

# Loop through rows
table_tbody = table.find('tbody')
rows = []

# BBL summary - you have to remove some lines that just contain the team
for innings in [row for row in table_tbody.find_all('tr', {'class':'data2'})]:
    rows.append([cell.get_text() for cell in innings.find_all('td')])

df = pd.DataFrame(rows, columns=columns).apply(pd.to_numeric, errors='ignore')

filepath = '../data/bbl09_raw.csv'
df.to_csv(filepath, index=False)

# Print to show that the data has been saved properly
print(pd.read_csv(filepath))