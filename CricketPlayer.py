# Imports
import requests
import pandas as pd
from bs4 import BeautifulSoup
import numpy as np

# Define the class for a player
class CricketPlayer:
    def __init__(self, innings_by_innings_link):
        self.link = innings_by_innings_link
        self.soup = BeautifulSoup(requests.get(innings_by_innings_link).text, features="html.parser")
        
    def view_raw_html(self):
        return(self.soup)
    
    def raw_innings(self):
        for caption in self.soup.find_all('caption'):
            if caption.get_text() == 'Innings by innings list':
                main_table = caption.find_parent('table', {'class': 'engineTable'})
                
        columns = [header.get_text() for header in main_table.find('thead').find_all('tr')[0].find_all('th')]
        rows = []

        for innings in [row for row in main_table.find('tbody').find_all('tr')]:
            rows.append([stat.get_text() for stat in innings.find_all('td')])
            
        return(pd.DataFrame(rows, columns=columns))
    
    def innings(self):
        raw_innings = self.raw_innings()
        raw_innings['Opposition'] = raw_innings['Opposition'].str.replace('v ', '')
        raw_innings.replace('-', np.nan, inplace=True)
        raw_innings.columns = raw_innings.columns.str.lower().str.replace(' ', '_')
        raw_innings['is_out'] = raw_innings.score.astype('str').apply(lambda x: False if x in ['nan', 'DNB'] else False if '*' in x else True)
        raw_innings['did_bowl'] = raw_innings.overs.astype('str').apply(lambda x: False if x in ['nan', 'DNB'] else True)
        raw_innings['did_bat'] = raw_innings.score.str.replace('*', '').astype('str').apply(lambda x: True if x.isnumeric() else False)
        raw_innings['score'] = raw_innings['score'].str.replace('*', '')
        return(raw_innings[['inns', 'score', 'did_bat', 'is_out', 'overs', 'conc', 'wkts', 'did_bowl', 'ct', 'st', 'opposition', 'ground', 'start_date']])
    
    def batting_summary(self):
        innings = self.innings()
        total_at_bats = innings.did_bat.sum()
        dismissals = innings.is_out.sum()
        total_runs = innings.score[innings.did_bat].dropna().astype('int').sum()
        return(pd.DataFrame({'Innings': total_at_bats, 
                             'Dismissals': dismissals, 
                             'Total Runs': total_runs, 
                             'Average': round(total_runs/dismissals, 4)}, index=['Overall']))
    
    def rolling_average_innings(self, n_innings):
        innings = self.innings()[self.innings().did_bat].set_index('start_date').loc[:, ['score', 'is_out']]
        innings.index = pd.to_datetime(innings.index)
        innings.score = innings.score.astype('int')
        rolling_innings = innings.rolling(n_innings).sum()
        rolling_innings['average'] = rolling_innings['score'] / rolling_innings['is_out']
        return(rolling_innings)
    
    def rolling_average_matches(self, n_matches):
        matches = self.innings()[self.innings().did_bat].set_index('start_date').loc[:, ['score', 'is_out']]
        matches.score = matches.score.astype('int')
        matches.index = pd.to_datetime(matches.index)
        matches = matches.groupby('start_date').sum()
        rolling_matches = matches.rolling(n_matches).sum()
        rolling_matches['average'] = rolling_matches['score'] / rolling_matches['is_out']
        return(rolling_matches)