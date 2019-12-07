# Imports
import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt
import requests
from bs4 import BeautifulSoup
import re 


class Innings():
    def __init__(self, raw_html):
        self.raw_html = raw_html
        self.title = raw_html.find('h2').text
        self.total = raw_html.find('div', {"class": "scorecard-section batsmen"}).find_all('div', {'class':'wrap total'})[0].find_all('div')[1].text
        
    def batting(self):
        '''Using a raw scorecard tab, find the batting details'''
        batsmen_rows = self.raw_html.find('div', {"class": "scorecard-section batsmen"}).find_all('div', {"class": "flex-row"})

        # Loop through all the rows, and keep only those that contain batting information
        batting = []    
        for i in batsmen_rows:
            details = i.find('div', {"class": "wrap batsmen"})
            if details != None:
                batting.append(details)

        # Create a pandas DataFrame and add column names 
        inningsdf = pd.DataFrame([self.clean_batting_row(i) for i in batting])
        
        # Scorecards can contain an extra column: minutes
        if len(inningsdf.columns) == 8: 
            summary_columns = ['batsman', 'how_out', 'runs', 
                             'balls_faced', 'minutes', 'fours', 'sixes', 
                             'strike_rate']
        else:
            summary_columns = ['batsman', 'how_out', 'runs', 
                             'balls_faced', 'fours', 'sixes', 
                             'strike_rate']
            
        inningsdf.columns = summary_columns
        
        # Generate batting position as the index
        inningsdf.index = inningsdf.index + 1
        
        # Add some flags about the players 
        inningsdf['is_out'] = inningsdf['how_out'].str.lower() != 'not out'
        inningsdf['is_keeper'] = inningsdf['batsman'].str.contains('†')
        inningsdf['is_captain'] = inningsdf['batsman'].str.contains('\(c\)')
        
        # Clean the visual indicators of captaincy and wicket keeper from name column
        inningsdf['batsman'] = inningsdf['batsman'].str.replace('†', '')
        inningsdf['batsman'] = inningsdf['batsman'].str.replace('\(c\)', '')
        
        return(inningsdf)
    
    def clean_batting_row(self, row):
        clean = [row.find('div', {"class": "cell batsmen"}).text]
        clean.append(row.find('div', {"class":"cell commentary"}).text)
        clean = clean + [x.text for x in row.find_all('div', {"class": "cell runs"})]
        return(clean)
    
    def split_fow(self, row):
        fow_re = re.compile('^([0-9]*)\-([0-9]*) (.*)$').search(row)
        wickets = fow_re.group(1)
        runs = fow_re.group(2)
        batsman = fow_re.group(3)
        return([wickets, runs, batsman])
    
    def fall_of_wickets(self):
        dnb_rows = [x.find('div', {"class": "wrap dnb"}) for x in self.raw_html.find('div', {"class": "scorecard-section batsmen"}).find_all('div', {"class": "flex-row"}) if x.find('div', {"class": "wrap dnb"}) != None] 
        
        # Specify that we want the fall of wickets row and not the did not bat list
        fall_of_wickets = [x.text for x in dnb_rows if x.text.find('Fall of wickets') != -1][0]
        clean_fow = fall_of_wickets.replace('Fall of wickets: ', '').split('), ')
        cleaner_fow = [x.replace('(', '').replace(')', '').split(', ') for x in clean_fow]
        fow_df = pd.DataFrame([self.split_fow(x[0]) for x in cleaner_fow], columns = ['wicket', 'runs', 'out_batsman'])
        fow_df['overs'] = [x[1].replace(' ov', '') for x in cleaner_fow]
        fow_df['partnership'] =  fow_df['runs'].astype(int) - fow_df['runs'].astype(int).shift(1)
        fow_df['partnership'] = fow_df['partnership'].fillna(fow_df.loc[0, 'runs'])
        return(fow_df)
    
    def total_balls(self, overs):
        '''Calculate total balls bowled from overs'''
        grouping_re = re.compile('^([0-9]*)\.([0-5]*)$').search(overs)
        if grouping_re == None:
            return(int(overs) * 6)
        else: 
            overs = int(grouping_re.group(1)) * 6
            balls = int(grouping_re.group(2))
            return(overs + balls)
    
    def bowling(self):
        '''Show the bowling figures for the innings'''
        bowling_section = self.raw_html.find('div', {'class':'scorecard-section bowling'})
        bowling_headers = [x.text for x in bowling_section.find('thead').find_all('th')]
        bowling_body = pd.DataFrame([[y.text for y in x.find_all('td')] for x in bowling_section.find('tbody').find_all('tr')])
        bowling_body.columns = bowling_headers
        bowling_body.drop('', inplace=True, axis=1)
        bowling_body['total_balls'] = bowling_body.O.apply(self.total_balls)
        bowling_body['strike_rate'] = bowling_body.total_balls / bowling_body.W.astype(int)
        # Check the calculated economy against the scraped
        bowling_body['economy'] = bowling_body.R.astype(int) / bowling_body.total_balls * 6 
        return(bowling_body)