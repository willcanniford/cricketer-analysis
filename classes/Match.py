# Imports
import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
from .Innings import Innings
import json


# Define the class that represents a match
class Match():
    def __init__(self, match_url):
        self.url = match_url
        self.id = re.compile(r'.*\/([0-9]*).html').search(self.url).group(1)
        self.soup = BeautifulSoup(requests.get(
            self.url).text, features="html.parser")
        self.innings_soup = self.soup.find_all(
            'article', {"class": "sub-module scorecard"})
        self.n_innings = len(self.innings_soup)
        self.result = self.soup.find(
            'span', {'class': 'cscore_notes_game'}).text
        self.details_json = json.loads(
            requests.get(
                'http://www.espncricinfo.com/ci/engine/match/%s.json' %
                self.id).text)

        if self.details_json:
            self.continent = self.details_json['match']['continent_name']
            self.teams = self.details_json['series'][0]['teams']
            self.home_team_id = self.details_json['match']['home_team_id']
            self.away_team_id = self.details_json['match']['away_team_id']
            self.home_team = [
                team for team in self.teams if team['team_id'] == self.home_team_id]
            self.away_team = [
                team for team in self.teams if team['team_id'] == self.away_team_id]
            self.home_team_name = self.home_team[0]['team_name']
            self.away_team_name = self.away_team[0]['team_name']

    def first_innings(self):
        '''Get an Innings object for the first innings'''
        try:
            raw_html = self.innings_soup[0]
        except BaseException:
            print('No first innings for this match.')
            return

        return(Innings(raw_html))

    def second_innings(self):
        '''Get an Innings object for the second innings'''
        try:
            raw_html = self.innings_soup[1]
        except BaseException:
            print('No second innings for this match.')
            return

        return(Innings(raw_html))

    def third_innings(self):
        '''Get an Innings object for the third innings'''
        try:
            raw_html = self.innings_soup[2]
        except BaseException:
            print('No third innings for this match.')
            return

        return(Innings(raw_html))

    def fourth_innings(self):
        '''Get an Innings object for the fourth innings'''
        try:
            raw_html = self.innings_soup[3]
        except BaseException:
            print('No fourth innings for this match.')
            return

        return(Innings(raw_html))

    def select_innings(self, innings_int):
        '''Get an Innings object for a given innings'''
        try:
            raw_html = self.innings_soup[innings_int - 1]
        except BaseException:
            innings_message = 'There is 1 inning available' if self.n_innings == 1 else 'There are %d innings available' % self.n_innings
            print('We could not find that innings for this match. %s.' %
                  innings_message)
            return

        return(Innings(raw_html))
