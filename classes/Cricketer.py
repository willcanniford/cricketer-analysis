# Imports
import requests
import pandas as pd
from bs4 import BeautifulSoup
import numpy as np
import re
from .Match import Match


# Define the class for a player
class Cricketer:
    def __init__(self, innings_by_innings_link):
        self.link = innings_by_innings_link
        self.soup = BeautifulSoup(requests.get(innings_by_innings_link).text, features="html.parser")
    
    def raw_innings(self):
        '''Search the raw html and return innings table'''
        for caption in self.soup.find_all('caption'):
            if caption.get_text() == 'Innings by innings list':
                main_table = caption.find_parent('table', {'class': 'engineTable'})
                
        columns = [header.get_text() for header in main_table.find('thead').find_all('tr')[0].find_all('th')]
        rows = []

        for innings in [row for row in main_table.find('tbody').find_all('tr')]:
            rows.append([stat.get_text() for stat in innings.find_all('td')])
            
        return(pd.DataFrame(rows, columns=columns))
    
    def innings(self, include_match_urls = False):
        '''Clean raw_innings() and return pd.DataFrame'''
        raw_innings = self.raw_innings()
        raw_innings['Opposition'] = raw_innings['Opposition'].str.replace('v ', '')
        raw_innings.replace('-', np.nan, inplace=True)
        
        # Clean the column names 
        raw_innings.columns = raw_innings.columns.str.lower().str.replace(' ', '_')
        
        # Create boolean flags for various metrics
        raw_innings['is_out'] = raw_innings.score.astype('str').apply(lambda x: False if x in ['nan', 'DNB'] else False if '*' in x else True)
        raw_innings['did_bowl'] = raw_innings.overs.astype('str').apply(lambda x: False if x in ['nan', 'DNB'] else True)
        raw_innings['did_bat'] = raw_innings.score.str.replace('*', '').astype('str').apply(lambda x: True if x.isnumeric() else False)
        raw_innings['score'] = raw_innings['score'].str.replace('*', '') # Remove the not out flag 
        
        # Grab the main table
        for caption in self.soup.find_all('caption'):
            if caption.get_text() == 'Innings by innings list':
                main_table = caption.find_parent('table', {'class': 'engineTable'})
        
        # Grab the match id from the href 
        raw_innings['match_id'] = [re.compile('match\/([0-9]*).html').search(x.get('href')).group(1) for x in main_table.find_all('a', href = re.compile('.*engine\/match\/.*'))]
        
        # Get the match urls 
        raw_innings['match_url'] = self.match_urls()
        
        # Create the final pd.DataFrame
        raw_innings = raw_innings[['inns', 'score', 'did_bat', 'is_out', 'overs', 'conc', 'wkts', 'did_bowl', 'ct', 'st', 'opposition', 'ground', 'start_date', 'match_id', 'match_url']]
        
        # Conditionall drop the match_url column 
        drop_match_urls = not include_match_urls
        raw_innings.drop('match_url', inplace = drop_match_urls, axis = 1)
        
        return(raw_innings)
    
    def batting_summary(self):
        '''Product summary statistics of entire career'''
        innings = self.innings()
        total_at_bats = innings.did_bat.sum()
        dismissals = innings.is_out.sum()
        total_runs = innings.score[innings.did_bat].dropna().astype('int').sum()
        return(pd.DataFrame({'Innings': total_at_bats, 
                             'Dismissals': dismissals, 
                             'Total Runs': total_runs, 
                             'Average': round(total_runs/dismissals, 4)}, index=['Overall']))
    
    def rolling_average_innings(self, n_innings):
        '''
        Return pd.DataFrame of rolling average at innings level 
        
        Parameters:
        n_innings (int): the size of the rolling innings window
        '''
        innings = self.innings()[self.innings().did_bat].set_index('start_date').loc[:, ['score', 'is_out']]
        innings.index = pd.to_datetime(innings.index)
        innings.score = innings.score.astype('int')
        rolling_innings = innings.rolling(n_innings).sum()
        rolling_innings['average'] = rolling_innings['score'] / rolling_innings['is_out']
        return(rolling_innings)
    
    def rolling_average_matches(self, n_matches):
        '''
        Return pd.DataFrame of rolling average at match level
        
        Parameters: 
        n_matches (int): the size of the rolling match window
        '''
        matches = self.innings()[self.innings().did_bat].set_index('start_date').loc[:, ['score', 'is_out']]
        matches.score = matches.score.astype('int')
        matches.index = pd.to_datetime(matches.index)
        matches = matches.groupby('start_date').sum()
        rolling_matches = matches.rolling(n_matches).sum()
        rolling_matches['average'] = rolling_matches['score'] / rolling_matches['is_out']
        return(rolling_matches)
    
    def accumulative_average(self):
        '''Calculate the average over time'''
        innings = self.innings()[self.innings().did_bat].set_index('start_date').loc[:, ['score', 'is_out']]
        innings.index = pd.to_datetime(innings.index)
        innings.score = innings.score.astype('int')
        innings['total_runs'] = innings.score.cumsum()
        innings['total_dismissals'] = innings.is_out.astype('int').cumsum()
        innings['running_average'] = innings.total_runs / innings.total_dismissals
        return(innings)
    
    def conversion(self):
        '''Calculate fifty/century conversion over time'''
        at_bats = self.innings()[self.innings().did_bat]
        at_bats['fifty'] = at_bats.score.astype('int').between(50,99, inclusive=True)
        at_bats['century'] = at_bats.score.astype('int').ge(100)
        at_bats.set_index('start_date', inplace=True)
        at_bats.index = pd.to_datetime(at_bats.index)
        conversion = at_bats[['fifty', 'century']].astype('int').cumsum()
        conversion['rate'] = conversion['century'] / (conversion['fifty'] + conversion['century'])
        return(conversion)
        
    def yearly_conversion(self):
        '''Calculate fifty/century conversion for every calendar year of the career'''
        at_bats = self.innings()[self.innings().did_bat]
        at_bats['fifty'] = at_bats.score.astype('int').between(50,99, inclusive=True)
        at_bats['century'] = at_bats.score.astype('int').ge(100)
        at_bats.set_index('start_date', inplace=True)
        at_bats.index = pd.to_datetime(at_bats.index)
        yearly = at_bats[['fifty', 'century']].astype('int').resample('A').sum()
        yearly['rate'] = yearly['century'] / (yearly['fifty'] + yearly['century'])
        return(yearly)
    
    def acc_yearly_conversion(self):
        '''Accumulative version of yearly_conversion()'''
        ot = self.yearly_conversion()[['fifty', 'century']].cumsum()
        ot['rate'] = ot['century'] / (ot['fifty'] + ot['century'])
        return(ot)
    
    def match_urls(self):
        '''Find and generate absolute links to all matches'''
        for caption in self.soup.find_all('caption'):
            if caption.get_text() == 'Innings by innings list':
                main_table = caption.find_parent('table', {'class': 'engineTable'})
        
        base_url = 'https://www.espncricinfo.com'
        match_links = [base_url + x.get('href') for x in main_table.find_all('a', href = re.compile('.*engine\/match\/.*'))]
        return(match_links)
    
    def get_test_matches(self):
        '''Create Match objects for every match in the innings by innings list'''
        matches = {}
        
        # Loop through the distinct match urls and save to dictionary
        for match_url in set(self.match_urls()):
            obj = Match(match_url)
            matches[obj.id] = obj
            
        return(matches)