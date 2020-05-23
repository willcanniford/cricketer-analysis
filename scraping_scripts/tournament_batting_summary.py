# Imports
import requests
import pandas as pd
from bs4 import BeautifulSoup
import argparse 

a = argparse.ArgumentParser(description='Return batting summary for given tournament ID.')
a.add_argument("--id", 
               action="store", 
               type=str, 
               required=True, 
               help='The ESPN cricinfo tournament ID.')

a.add_argument("--save", 
               action="store", 
               type=bool, 
               required=False, 
               default=False, 
               help='Boolean indicating whether you want to save the result.')

a.add_argument("--save_path", 
               action="store", 
               type=str, 
               required=False, 
               default=False, 
               help="If saving, declare a location to save the results.")


# Define those arguments as variables for use in the script
arguments = a.parse_args()
tournament_id = arguments.id 
save = arguments.save
save_path = arguments.save_path

page_url = 'http://stats.espncricinfo.com/ci/engine/records/batting/most_runs_career.html?id=' + tournament_id + ';type=tournament'

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

# TODO - handle class here the may differ between tournaments - pick the one that contains a player link
for innings in [row for row in table_tbody.find_all('tr', {'class':'data1'})]:
    rows.append([cell.get_text() for cell in innings.find_all('td')])

df = pd.DataFrame(rows, columns=columns).apply(pd.to_numeric, errors='ignore')

if save and save_path:
    df.to_csv(save_path, index=False)
    print('CSV file saved at: ' + save_path)
    print()
    print(pd.read_csv(save_path))
else: 
    print(df)
    