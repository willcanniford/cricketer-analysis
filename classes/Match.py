# Imports
import numpy as np 
import pandas as pd 
import requests
from bs4 import BeautifulSoup
import re 
from .Innings import Innings 


# Define the class that represents a match 
class Match():
    def __init__(self, match_url):
        self.url = match_url
        self.soup = BeautifulSoup(requests.get(self.url).text, features="html.parser")
        self.innings_soup = self.soup.find_all('article', {"class": "sub-module scorecard"})
        self.n_innings = len(self.innings_soup)
        self.result = self.soup.find('span', {'class':'cscore_notes_game'}).text
        
    def first_innings(self):
        '''Get an Innings object for the first innings'''
        try:
            raw_html = self.innings_soup[0]
        except:
            print('No first innings for this match.')
            return
        
        return(Innings(raw_html))
        
    def second_innings(self):
        '''Get an Innings object for the second innings'''
        try:
            raw_html = self.innings_soup[1]
        except:
            print('No second innings for this match.')
            return
        
        return(Innings(raw_html))
        
    def third_innings(self):
        '''Get an Innings object for the third innings'''
        try:
            raw_html = self.innings_soup[2]
        except:
            print('No third innings for this match.')
            return
        
        return(Innings(raw_html))
        
    def fourth_innings(self):
        '''Get an Innings object for the fourth innings'''
        try:
            raw_html = self.innings_soup[3]
        except:
            print('No fourth innings for this match.')
            return
        
        return(Innings(raw_html))